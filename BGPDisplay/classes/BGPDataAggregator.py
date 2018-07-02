from collections import defaultdict, Counter
from datetime import datetime, timezone
import os

from _pybgpstream import BGPStream, BGPRecord
from rtrlib import RTRManager

from .helper.db_connector import PostgresConnector as DBConnector
from .helper.named_tuples import RouteCollectorMeta, Route
from .helper.functions import *


class BGPDataAggregator(object):
    """docstring for BGPDataAggregator"""

    def __init__(
        self,
        filters={"collector": ["rrc00"]},
        rpki_validator="rpki-validator.realmv6.org:8282",
        settings_file="../settings.json",
    ):
        self.stream = BGPStream()
        self.filters = filters
        self.route_table = dict()
        self.i = 0

        self.metadata_vp = dict()
        self.metadata_rc = dict()
        self.peers = Counter()
        self.prefix4 = Counter()
        self.prefix6 = Counter()

        start_timestamp = get_push_timestamp(datetime.now(timezone.utc))

        for filter_type, filter_array in filters.items():
            for filter_value in filter_array:
                self.stream.add_filter(filter_type, filter_value)

        for collector in filters["collector"]:
            self.route_table[collector] = defaultdict(dict)
            self.metadata_vp[collector] = defaultdict(list)
            self.metadata_rc[collector] = RouteCollectorMeta(None, 0, 0, 0, 0)
            self.peers[collector] = defaultdict(int)
            self.prefix4[collector] = defaultdict(int)
            self.prefix6[collector] = defaultdict(int)

        settings = get_settings(settings_file)
        settings["db"]["password"] = os.environ["PGPASS"]

        self.db = DBConnector(settings["db"])

        rpki = rpki_validator.split(":")
        self.mgr = RTRManager(rpki[0], rpki[1])
        self.mgr.start()

        self.start_collecting(start_timestamp)

    def __del__(self):
        if self.mgr.is_synced():
            self.mgr.stop()

    def push_data(self, timestamp):
        self.db.update_vp_meta(self.metadata_vp)
        for rc in self.metadata_rc.keys():
            self.metadata_rc[rc] = RouteCollectorMeta(
                rc,
                timestamp,
                len(self.peers[rc].keys()),
                len(self.prefix4[rc]),
                len(self.prefix6[rc]),
            )
        self.db.update_rc_meta(self.metadata_rc)

    def start_collecting(self, start_timestamp, end_timestamp=0):
        self.stream.add_interval_filter(start_timestamp, end_timestamp)
        print("Start BGPStream:", start_timestamp, end_timestamp)
        next_timestamp = get_timestamp_now(5)
        self.stream.start()
        rec = BGPRecord()
        while(self.stream.get_next_record(rec)):
            if rec.status == "valid":
                if rec.time >= next_timestamp:
                    self.push_data(next_timestamp)
                    next_timestamp += 300

                elem = rec.get_next_elem()
                while elem:
                    origin_asn = ""
                    if elem.type is "R" or elem.type is "A":
                        origin_asn = elem.fields["as-path"].split(" ")[-1]

                    try:
                        origin_asn = int(origin_asn)
                    except ValueError:
                        elem = rec.get_next_elem()
                        continue

                    prefix = elem.fields["prefix"]
                    ip, mask_len = split_prefix(prefix)

                    # Check if v4 or v6
                    is_v4 = check_ipv4(ip)

                    validated = self.mgr.validate(origin_asn, ip, mask_len)
                    old_elem = self.route_table[rec.collector][
                        (elem.peer_asn, elem.peer_address)
                    ].get(prefix)
                    if elem.type is "R" or elem.type is "A":
                        self.route_table[rec.collector][
                            (elem.peer_asn, elem.peer_address)
                        ][prefix] = Route(
                            origin_asn,
                            rec.collector,
                            prefix,
                            is_v4,
                            validated.state.value,
                        )

                        if old_elem:
                            if old_elem.type != validated.state.value:
                                """Make use of the fact that:
                                    0: valid in enum
                                    1: unknown in enum
                                    2: invalid in enum
                                We designed the namedtuple the way to represent
                                that. So valid is a pos 3 and so on.
                                """
                                self.metadata_vp[rec.collector][elem.peer_asn][
                                    3 + old_elem.type
                                ] -= 1
                                self.metadata_vp[rec.collector][elem.peer_asn][
                                    3 + validated.state.value
                                ] += 1
                        else:
                            if not self.metadata_vp[rec.collector].get(elem.peer_asn):
                                """Init the metadata-entry if it not exists already"""
                                self.metadata_vp[rec.collector][elem.peer_asn] = [
                                    elem.peer_asn,
                                    rec.collector,
                                    next_timestamp,
                                    0,
                                    0,
                                    0,
                                ]

                            # Update the VantagePoint Metadate the same way like above.
                            self.metadata_vp[rec.collector][elem.peer_asn][
                                3 + validated.state.value
                            ] += 1
                            self.metadata_vp[rec.collector][elem.peer_asn][2] = next_timestamp

                            self.peers[rec.collector][elem.peer_asn] += 1

                            if is_v4:
                                self.prefix4[rec.collector][prefix] += 1
                            else:
                                self.prefix6[rec.collector][prefix] += 1

                    elif elem.type is "W":
                        if old_elem:

                            # Reduce the number of IPv4/v6 Addresses for this prefix
                            if is_v4:
                                self.prefix4[rec.collector][prefix] -= 1
                                if self.prefix4[rec.collector][prefix] == 0:
                                    del (self.prefix4[rec.collector][prefix])
                            else:
                                self.prefix6[rec.collector][prefix] -= 1
                                if self.prefix6[rec.collector][prefix] == 0:
                                    del (self.prefix4[rec.collector][prefix])

                            # Reduce number of prefixes belonging to this ASN
                            self.peers[rec.collector][elem.peer_asn] -= 1
                            if self.peers[rec.collector][elem.peer_asn] == 0:
                                del (self.prefix4[rec.collector][prefix])

                            # Update the metadata valid/unknown/invalid count
                            self.metadata_vp[rec.collector][elem.peer_asn][
                                3 + old_elem.type
                            ] -= 1

                            # Update the metadata timestamp
                            self.metadata_vp[rec.collector][elem.peer_asn][2] = next_timestamp

                            # Remove the entry from the route_table
                            self.route_table[rec.collector][
                                (elem.peer_asn, elem.peer_address)
                            ].pop(prefix, None)

                        else:
                            # !!TODO: write log about that!
                            pass

                    elem = rec.get_next_elem()
