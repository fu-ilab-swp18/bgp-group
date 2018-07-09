SELECT rcid, ROUND(timestamp / ${timestampInterval}) * ${timestampInterval} AS timestamp,
               SUM(valid) AS valid, SUM(invalid) AS invalid, SUM(unknown) AS unknown
FROM "VantagePoint_Metadata"
GROUP BY rcid, ROUND(timestamp / ${timestampInterval})
ORDER BY timestamp
LIMIT 7;
