import time


from _pybgpstream import BGPStream, BGPRecord, BGPElem
from rtrlib import RTRManager, register_pfx_update_callback, register_spki_update_callback

from .helper.bgp_extension import split_path

mgr = RTRManager(
    "rpki-validator.realmv6.org",
	8282
)

mgr.start()
while not mgr.is_synced():
    sleep(0.2)
    if status.error:
        print("Connection error")
        exit()

# Create a new bgpstream instance and a reusable bgprecord instance
stream = BGPStream()
rec = BGPRecord()

# Consider RIPE RRC 10 only
stream.add_filter('collector','route-views2')

# Consider this time interval:
# Sat Aug  1 08:20:11 UTC 2015

# now = int(time.time())

stream.add_interval_filter(1438417216,1438417216)

# Start the stream
stream.start()

# Get next record
while(stream.get_next_record(rec)):
    # Print the record information only if it is not a valid record
    if rec.status != "valid":
        print(rec.project, rec.collector, rec.type, rec.time, rec.status)
    else:
        elem = rec.get_next_elem()
        while(elem):
            # Print record and elem information
            print(rec.project, rec.collector, rec.type, rec.time, rec.status)
            print(elem.type, elem.peer_address, elem.peer_asn, elem.fields)
            prefix = elem.fields["prefix"].split('/')
            result = mgr.validate((int) elem.fields["as-path"].split(" ")[-1], prefix[0], prefix[1])
            elem = rec.get_next_elem()
