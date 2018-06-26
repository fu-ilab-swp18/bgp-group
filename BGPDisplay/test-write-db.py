import pickle
import psycopg2
from datetime import datetime, timezone


def get_timestamp_now():
    return int(datetime.now(timezone.utc).timestamp())


vp_meta = pickle.load(open("test.p", "rb"))

conn = psycopg2.connect("dbname='bgp' user='bgp' host='pg.a0s.de' password='pool-specter'")
cur = conn.cursor()

sql = 'INSERT INTO "public"."VantagePoint_Metadata"("vpid", "rcid", "timestamp", "valid", "unknown", "invalid") VALUES(%s, %s, %s, %s, %s, %s)'

for rc, peers in vp_meta.items():
    for vp, peer in peers.items():
        cur.execute(sql, peer)

conn.commit()
cur.close()
conn.close()
