from datetime import datetime

from _pybgpstream import BGPStream, BGPRecord, BGPElem
from rtrlib import RTRManager, register_pfx_update_callback, register_spki_update_callback

from helper.db_connector import SQLiteConnector as DBConnector


class BGPDataAggregator(object):
    """docstring for BGPDataAggregator"""

    def __init__(self, route_collector="rrc00", rpki_validator="rpki-validator.realmv6.org:8282"):
        self.rc = route_collector

        rpki = rpki_validator.split(":")
        self.mgr = RTRManager(rpki[0], rpki[1])

        # self._start_rtr_manager()

        self.stream = BGPStream()
        self.rec = BGPRecord()

    def __del__(self):
        if self.mgr.is_synced():
            self.mgr.stop()

    def _start_rtr_manager(self):
        self.mgr.start()
        while not self.mgr.is_synced():
            sleep(0.2)
            if status.error:
                print("Connection error")
                exit()
