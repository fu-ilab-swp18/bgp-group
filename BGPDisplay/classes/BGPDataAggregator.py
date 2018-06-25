from collections import defaultdict
from datetime import datetime, timezone

from _pybgpstream import BGPStream, BGPRecord
from rtrlib import RTRManager

from .helper.db_connector import SQLiteConnector as DBConnector
from .helper.named_tuples import VantagePointMeta, RouteCollectorMeta, Route
from .helper.functions import get_push_timestamp, split_prefix


class BGPDataAggregator(object):
    """docstring for BGPDataAggregator"""

    def __init__(self, filters={'collector': ['rrc00']}, rpki_validator="rpki-validator.realmv6.org:8282", db="metasnap.db"):
        self.stream = BGPStream()
        self.filters = filters
        self.route_table = dict()
        self.i = 0

        for filter_type, filter_array in filters.items():
            for filter_value in filter_array:
                self.stream.add_filter(filter_type, filter_value)

        for collector in filters['collector']:
            self.route_table[collector] = defaultdict(dict)

        # self.db = DBConnector(db, read_only=False)

        rpki = rpki_validator.split(":")
        self.mgr = RTRManager(rpki[0], rpki[1])
        self.mgr.start()

        start_timestamp = get_push_timestamp(datetime.now(timezone.utc))
        self.start_collecting(start_timestamp, start_timestamp)

    def __del__(self):
        if self.mgr.is_synced():
            self.mgr.stop()

    def start_collecting(self, start_timestamp, end_timestamp=0):
        self.stream.add_interval_filter(start_timestamp, end_timestamp)
        print("Start BGPStream:", start_timestamp, end_timestamp)
        self.stream.start()
        rec = BGPRecord()
        while(self.stream.get_next_record(rec)):
            if rec.status == "valid":
                self.i += 1
                if self.i % 10000 == 0:
                    print(self.i)

                elem = rec.get_next_elem()
                while(elem):
                    origin_asn = None
                    if elem.type is 'R' or elem.type is 'A':
                        origin_asn = elem.fields['as-path'].split(' ')[-1]

                    try:
                        origin_asn = int(origin_asn)
                    except ValueError:
                        elem = rec.get_next_elem()
                        continue

                    prefix = elem.fields['prefix']
                    (ip, mask_len) = split_prefix(prefix)

                    #!TODO Check if v4 or v6

                    validated = self.mgr.validate(origin_asn, ip, mask_len)

                    if elem.type is 'R' or elem.type is 'A':
                        self.route_table[rec.collector][(elem.peer_asn, elem.peer_address)][prefix] = Route(
                            origin_asn, rec.collector, prefix, validated.state)
                    elif elem.type is 'W':
                        self.route_table[rec.collector][(
                            elem.peer_asn, elem.peer_address)].pop(prefix, None)

                    elem = rec.get_next_elem()

        for rc in self.route_table:
            print(rc, len(rc))
