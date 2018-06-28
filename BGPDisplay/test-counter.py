import pickle

from datetime import datetime, timezone


peers, prefix4, prefix6 = pickle.load(open("rc_data.p", "rb"))

print(peers)

for rc, peer in peers.items():
    rc_meta = (rc, int(datetime.now(timezone.utc).timestamp()), len(peer.keys()), len(prefix4[rc]), len(prefix6[rc]))

    print(rc_meta)
