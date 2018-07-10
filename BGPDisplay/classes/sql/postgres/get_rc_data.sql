SELECT *
FROM "RouteCollector_Metadata"
WHERE "rcid" IN %(rc_tuple)s
    AND "timestamp" BETWEEN %(start)s AND %(stop)s
ORDER BY "timestamp" DESC;
