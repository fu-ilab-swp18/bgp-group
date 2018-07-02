INSERT INTO "public"."RouteCollector_Metadata"("rcid", "timestamp", "peers", "prefix4", "prefix6")
VALUES(%s, %s, %s, %s, %s)
ON CONFLICT (rcid, "timestamp")
DO UPDATE SET
    peers = EXCLUDED.peers,
    prefix4 = EXCLUDED.prefix4,
    prefix6 = EXCLUDED.prefix6
;
