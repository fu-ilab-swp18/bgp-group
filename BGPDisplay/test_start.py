from classes import BGPDataAggregator

import time

t = time.time()

test = BGPDataAggregator()
print('Elapsed Time:', time.time() - t )
print(test.metadata_vp['rrc00'])
