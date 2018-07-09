var pg = require('pg');
var fs = require("fs");
var path = require("path");

var settings_path = path.join(__dirname, '..', 'settings.json');
var settings = JSON.parse(fs.readFileSync(settings_path, 'utf-8'));

var db = settings.db;
db.password = process.env.PGPASS

var client = new pg.Client({
  host: db.host,
  user: db.user,
  database: db.name,
  password: db.password
});

var timestampInterval = 300;

function init() {
  if (!process.env.PGPASS) {
    throw new Error('Please set the password for the database first. PGPASS=foo');
  }
  return client.connect();
}

function getData() {
  var data = {
    rc: {},
    vp: {}
  };

  return client.query(' \
      SELECT * \
      FROM "RouteCollector_Metadata" \
      ORDER BY timestamp \
      LIMIT 8 \
    ')
    .then(function (res) {
      res.rows.forEach(function (row) {
        var rc = data.rc[row.rcid] = data.rc[row.rcid] || [];
        row.prefix = row.prefix6 + row.prefix4;
        if (rc.length === 0) {
          row.announcedPrefixes = 0;
        } else {
          var lastSnapshot = rc[rc.length-1];
          row.announcedPrefixes = row.prefix - lastSnapshot.prefix;
        }
        data.rc[row.rcid].push(row);
      });

      return client.query(` \
        SELECT rcid, ROUND(timestamp / ${timestampInterval}) * ${timestampInterval} AS timestamp, \
               SUM(valid) AS valid, SUM(invalid) AS invalid, SUM(unknown) AS unknown \
        FROM "VantagePoint_Metadata" \
        GROUP BY rcid, ROUND(timestamp / ${timestampInterval}) \
        ORDER BY timestamp \
        LIMIT 7 \
      `);
    })

    .then(function (res) {
      res.rows.forEach(function (row) {
        data.vp[row.rcid] = data.vp[row.rcid] || [];
        row.valid = parseInt(row.valid);
        row.invalid = parseInt(row.invalid);
        row.unknown = parseInt(row.unknown);
        data.vp[row.rcid].push(row);
      });

      return data;
    })

    .catch(function (err) {
      console.error(err.stack);
    });
}

module.exports = {
  init: init,
  getData: getData
};
