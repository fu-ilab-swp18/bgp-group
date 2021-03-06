import json
import os
import pickle
import psycopg2
from datetime import datetime, timezone


def get_timestamp_now():
    return int(datetime.now(timezone.utc).timestamp())


vp_meta = pickle.load(open("test.p", "rb"))
rc_peers, prefix4, prefix6 = pickle.load(open("rc_data.p", "rb"))

password = os.environ['PGPASS']
settings = {}
with open('settings.json') as f:
    settings = json.load(f)

db = settings['db']

conn = psycopg2.connect(
    dbname=db['name'],
    user=db['user'],
    host=db['host'],
    password=password)

cur = conn.cursor()

sql = 'INSERT INTO "public"."VantagePoint_Metadata"("vpid", "rcid", "timestamp", "valid", "unknown", "invalid") VALUES(%s, %s, %s, %s, %s, %s)'
sql_rc = 'INSERT INTO "public"."RouteCollector_Metadata"("rcid", "timestamp", "peers", "prefix4", "prefix6") VALUES(%s, %s, %s, %s, %s)'

for rc, peers in vp_meta.items():
    for vp, peer in peers.items():
        cur.execute(sql, peer)

    cur.execute(sql_rc, (rc, int(datetime.now(timezone.utc).timestamp()), len(rc_peers[rc].keys()), len(prefix4[rc]), len(prefix6[rc])))

conn.commit()
cur.close()
conn.close()
