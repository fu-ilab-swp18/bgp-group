const request = require('request-promise-native');

var host = 'localhost:5000';
var tls = false;

function setHost(h) {
  host = h;
}

function toggleTLS(t) {
  tls = !!t;
}

function requestData(path) {
  const baseUrl = `http${tls ? 's' : ''}://${host}`;
  return request.get({
    baseUrl: baseUrl,
    uri: path,
    json: true
  });
}

function requestWithRCAndTimestamp(basePath, rc, timestamp, filter) {
  var path = `/${basePath}/${rc}`;
  if (filter) {
    path += `/${filter}`;
  }
  path += `/${timestamp ? timestamp : 'latest'}`;
  return requestData(path).then(function (res) {
    return {
      snapshot: res.data[rc],
      timeslot: res.timeslot
    };
  });
}

function getRCData(rc, timestamp) {
  return requestWithRCAndTimestamp('rc_data', rc, timestamp);
}

function getVPData(rc, vp, timestamp) {
  return requestWithRCAndTimestamp('vp_data', rc, timestamp, vp || 'all');
}

module.exports = {
  setHost: setHost,
  toggleTLS: toggleTLS,
  getRCData: getRCData,
  getVPData: getVPData
};
