SELECT "timestamp"
FROM "VantagePoint_Data"
WHERE "rcid" IN %(rc_tuple)s
    AND "vpid" IN %(vp_tuple)s
ORDER BY "timestamp" DESC
LIMIT 1;
