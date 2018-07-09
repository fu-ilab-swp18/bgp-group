SELECT DISTINCT ON("vpid", "vpaddr", "rcid") "vpid", "vpaddr", "rcid", "timestamp", "valid", "unknown", "invalid"
FROM "VantagePoint_Data"
WHERE "rcid" IN %(rc_tuple)s
    AND "vpid" IN %(vp_tuple)s
    AND "timestamp" BETWEEN %(start)s AND %(stop)s
ORDER BY timestamp;
