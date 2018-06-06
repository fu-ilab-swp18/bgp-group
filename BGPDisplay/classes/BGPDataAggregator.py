import ipaddress

from datetime import datetime

from _pybgpstream import BGPStream, BGPRecord, BGPElem
from rtrlib import RTRManager, register_pfx_update_callback, register_spki_update_callback

from .helper.db_connector import SQLiteConnector as DBConnector
from .helper.dataTuples import VantagePointMeta, RouteCollectorMeta, Route


class BGPDataAggregator(object):
    """docstring for BGPDataAggregator"""

    def __init__(self, filters={'collector': ['rrc00']}, rpki_validator="rpki-validator.realmv6.org:8282", db="metasnap.db"):
        self.stream = BGPStream()
        self.filters = filters

        for filter_type, filter_array in filters.items():
            for filter_value in filter_array:
                self.stream.add_filter(filter_type, filter_value)

        rpki = rpki_validator.split(":")
        self.mgr = RTRManager(rpki[0], rpki[1])
        self.mgr.start()

        self.db = DBConnector(db, read_only=False)
        self.route_table = dict()

        start_timestamp = self.get_push_timestamp(datetime.utcnow())
        self.start_collecting(start_timestamp)

    def __del__(self):
        if self.mgr.is_synced():
            self.mgr.stop()

    def get_push_timestamp(start_time):
        hours = [0, 8, 16, 24]
        # get closest push
        for i in range(0, len(hours)):
            if hours[i + 1] > start_time.hour:
                break

        start_time = start_time.replace(
            hour=12, minute=0, second=0, microsecond=0)

        return int(start_time.strftime("%s"))

    def start_collecting(self, start_timestamp, end_timestamp=0):
        self.stream.add_interval_filter(start_timestamp, end_timestamp)
        rec = BGPRecord()
        while(self.stream.get_next_record(rec)):
            if rec.status == "valid":
                elem = self.rec.get_next_elem()
                while(elem):
                    asn = elem.fields['as-path'].split(' ')[-1]
                    prefix = ipaddress.ip_interface(elem.fields['prefix'])
                    ip = prefix.ip.compressed()
                    mask_len = prefix.with_prefixlen.split('/')[1]

                    validated = self.mgr.validate(asn, ip, mask_len)

                    self.route_table[rec.collector][asn][prefix] = Route(
                        vantage_point, rec.collector, prefix, (prefix.version is 4), validated.state)
