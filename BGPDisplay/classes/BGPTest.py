from datetime import datetime

from _pybgpstream import BGPStream, BGPRecord, BGPElem
from rtrlib import RTRManager, register_pfx_update_callback, register_spki_update_callback

# from helper.bgp_extensions import split_path


class BGPTest(object):

    def __init__(self, route_collector="rrc00", rpki_validator="rpki-validator.realmv6.org:8282"):
        self.rc = route_collector

        rpki = rpki_validator.split(":")
        self.mgr = RTRManager(rpki[0], rpki[1])

        # self._start_rtr_manager()

        self.stream = BGPStream()
        self.rec = BGPRecord()

    def _start_rtr_manager(self):
        self.mgr.start()
        while not self.mgr.is_synced():
            sleep(0.2)
            if status.error:
                print("Connection error")
                exit()

    def start_stream(self, start_time=None, end_time=0, route_collector=""):
        """ Starts the
        """

        if route_collector == "":
            route_collector = self.rc
        self.stream.add_filter('collector', route_collector)
        self.stream.add_filter('record-type', 'ribs')

        if (start_time is None) or not isinstance(start_time, datetime):
            start_time = datetime.utcnow()

        if isinstance(end_time, datetime):
            end = int(end_time.strftime("%s"))
        else:
            end = 0

        start = int(datetime.utcnow().strftime("%s"))
        print(start)

        self.stream.add_interval_filter(start, 0)
        # print('Start stream with', start_time, end_time)
        self.stream.start()

    def get_records(self):
        while(self.stream.get_next_record(self.rec)):

            # Print the self.record information only if it is not a valid self.record
            if self.rec.status != "valid":
                pass
            else:
                elem = self.rec.get_next_elem()
                while(elem):
                    # Print self.record and elem information
                    print(self.rec.project, self.rec.collector,
                          self.rec.type, self.rec.time, self.rec.status)
                    print(elem.type, elem.peer_address,
                          elem.peer_asn, elem.fields)
                    # prefix = elem.fields["prefix"].split('/')
                    # result = mgr.validate((int) elem.fields["as-path"].split(" ")[-1], prefix[0], prefix[1])
                    elem = self.rec.get_next_elem()

        print("done.")
