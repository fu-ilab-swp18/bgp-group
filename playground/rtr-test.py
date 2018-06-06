from rtrlib import RTRManager, PfxvState

def callback(pfx_record, data):
    print(pfx_record)

mgr = RTRManager('rpki-validator.realmv6.org', 8282)
mgr.start()
result = mgr.validate(55803, '223.25.52.0', 23)

mgr.for_each_ipv4_record(callback, None)

mgr.stop()

print('\n--', result)
