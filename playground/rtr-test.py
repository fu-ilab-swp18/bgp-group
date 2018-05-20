from rtrlib import RTRManager, PfxvState

mgr = RTRManager('rpki-validator.realmv6.org', 8282)
mgr.start()
result = mgr.validate(12345, '10.10.0.0', 24)

print('\n \n', result, '\n \n');

if result == PfxvState.valid:
    print('Prefix Valid')
elif result == PfxvState.invalid:
    print('Prefix Invalid')
elif result == PfxvState.not_found:
    print('Prefix not found')
else:
    print('Invalid response')

mgr.stop()