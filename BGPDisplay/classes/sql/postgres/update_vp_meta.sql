INSERT INTO "public"."VantagePoint_Metadata"("vpid", "rcid", "timestamp", "valid", "unknown", "invalid")
VALUES(%s, %s, %s, %s, %s, %s)
ON CONFLICT (vpid, rcid, "timestamp")
DO UPDATE SET
    valid = EXCLUDED.valid,
    unknown = EXCLUDED.unknown,
    invalid = EXCLUDED.invalid
;
