INSERT INTO "public"."VantagePoint_Data"("vpid", "vpaddr", "rcid", "timestamp", "valid", "unknown", "invalid")
VALUES(%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (vpid, vpaddr, rcid, "timestamp")
DO UPDATE SET
    valid = EXCLUDED.valid,
    unknown = EXCLUDED.unknown,
    invalid = EXCLUDED.invalid
;
