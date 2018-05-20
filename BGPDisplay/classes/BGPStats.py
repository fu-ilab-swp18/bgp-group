import time
import logging

from _pybgpstream import BGPStream, BGPRecord, BGPElem
from rtrlib import RTRManager, register_pfx_update_callback, register_spki_update_callback

# from helper.bgp_extensions import split_path

class BGPStats(object):
    """docstring for bgpStats"""
    def __init__(self, route_collector="rrc00", rpki_validator="rpki-validator.realmv6.org:8282"):
        
        print(__name__)
        logger = logging.getLogger('rtrlib')
        print(logger)

        logger.setLevel(logging.DEBUG)
        print(logger)

        self.rc = route_collector

        rpki = rpki_validator.split(":")
        self.mgr = RTRManager(rpki[0],rpki[1])

        self._start_rtr_manager()

        self.stream = BGPStream()
        self.rec = BGPRecord()



    def _start_rtr_manager(self):
        self.mgr.start()
        while not self.mgr.is_synced():
            sleep(0.2)
            if status.error:
                print("Connection error")
                exit()

    def start_stream(self, intervall, route_collector=""):
        if route_collector == "":
            route_collector = self.rc
        self.stream.add_filter('collector', route_collector)
        if intervall is null:
            self.stream.set_live_mode()
        else:
            self.stream.add_interval_filter(intervall[0],intervall[1])
        self.stream.start()


    def get_records(self):
        while(self.stream.get_next_record(self.rec)):
            # Print the self.record information only if it is not a valid self.record
            if self.rec.status != "valid":
                print(self.rec.project, self.rec.collector, self.rec.type, self.rec.time, self.rec.status)
            else:
                elem = self.rec.get_next_elem()
                while(elem):
                    # Print self.record and elem information
                    print(self.rec.project, self.rec.collector, self.rec.type, self.rec.time, self.rec.status)
                    print(elem.type, elem.peer_address, elem.peer_asn, elem.fields)
                    prefix = elem.fields["prefix"].split('/')
                    # result = mgr.validate((int) elem.fields["as-path"].split(" ")[-1], prefix[0], prefix[1])
                    elem = self.rec.get_next_elem()
