SELECT DISTINCT ON ("rcid") "rcid", "timestamp", "peers", "prefix4", "prefix6"
FROM "RouteCollector_Metadata"
WHERE "rcid" IN %(rc_tuple)s
ORDER BY rcid, timestamp;
