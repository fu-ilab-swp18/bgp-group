import time
import psycopg2
import pickle

from classes import BGPLocalAggregator

t = time.time()
test = BGPLocalAggregator()
print('Elapsed Time:', time.time() - t )


pickle.dump(test.metadata_vp, open("test.p", "wb"))

print(test.metadata_vp['rrc00'])
