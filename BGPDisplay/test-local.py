import time

from classes import BGPLocalAggregator

t = time.time()
test = BGPLocalAggregator()
print('Elapsed Time:', time.time() - t )
print(test.metadata_vp['rrc00'])
