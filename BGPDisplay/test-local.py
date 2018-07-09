import time
import psycopg2
import pickle

from classes import BGPLocalAggregator

t = time.time()
test = BGPLocalAggregator()
print('Elapsed Time:', time.time() - t)


pickle.dump(test.metadata_vp, open("test.p", "wb"))

pickle.dump((test.peers, test.prefix4, test.prefix6), open("rc_data.p", "wb"))

print(test.metadata_vp['rrc00'])

print(test.peers)

print(test.prefix4)
print(test.prefix6)
