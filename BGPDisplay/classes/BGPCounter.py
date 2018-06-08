from collections import Counter, defaultdict
from datetime import datetime, timezone

from _pybgpstream import BGPStream, BGPRecord
from rtrlib import RTRManager

from .helper.db_connector import SQLiteConnector as DBConnector
from .helper.dataTuples import VantagePointMeta, RouteCollectorMeta, Route


class BGPCounter(object):
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

        self.counter = Counter()

        start_timestamp = self.get_push_timestamp(datetime.now(timezone.utc))
        # self.start_collecting(start_timestamp, int(datetime.now(timezone.utc).strftime("%s")))
        self.start_collecting(start_timestamp, start_timestamp)

    def __del__(self):
        if self.mgr.is_synced():
            self.mgr.stop()

    def get_push_timestamp(self, start_time):
        hours = [0, 8, 16, 24]
        # get closest push
        for i in range(0, len(hours)):
            if hours[i + 1] > start_time.hour:
                break

        start_time = start_time.replace(hour=hours[i], minute=0, second=0, microsecond=0)

        return int(start_time.timestamp())

    def start_collecting(self, start_timestamp, end_timestamp=0):
        self.stream.add_interval_filter(start_timestamp, end_timestamp)
        print("Start BGPStream:", start_timestamp, end_timestamp)
        self.stream.start()
        rec = BGPRecord()
        act_dump = "unknown"
        while(self.stream.get_next_record(rec)):
            self.i += 1
            if self.i % 10000 == 0:
                print(self.i)
            if rec.status == "valid":
                if(act_dump != rec.dump_position):
                    act_dump = rec.dump_position
                    print('Dump Position:', rec.dump_position)
                elem = rec.get_next_elem()
                while(elem):

                    self.counter.update(elem.type)

                    elem = rec.get_next_elem()

        print(self.counter)
