CREATE TABLE IF NOT EXISTS vantagepoint_metadata (
   vpid TEXT NOT NULL,
   rcid TEXT NOT NULL,
   timestamp INTEGER NOT NULL,
   valid INTEGER,
   invalid INTEGER,
   unknown INTEGER,
   PRIMARY KEY (vpid, rcid, timestamp)
);

CREATE TABLE IF NOT EXISTS routecollector_metadata (
   rcid TEXT NOT NULL,
   timestamp INTEGER NOT NULL,
   rcloc TEXT NOT NULL,
   peers INTEGER,
   prefix4 INTEGER,
   prefix6 INTEGER,
   unknown INTEGER,
   PRIMARY KEY (rcid, timestamp)
);
