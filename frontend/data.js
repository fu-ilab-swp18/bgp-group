const api = require('./api');
const moment = require('moment');

const maxInitialSnapshots = 7;
const snapshotInterval = 300;

var rcDataCache = {};

function getCachedDataForRC(rc) {
  rcDataCache[rc] = rcDataCache[rc] || {
    rc: {
      initialized: false,
      snapshots: [],
      lastTimestamp: null
    },
    vp: {
      initialized: false,
      snapshots: [],
      lastTimestamp: null
    }
  };
  return rcDataCache[rc];
}

function prepareAndPushTimestamp(response, dataCache, processCallback) {
  var snapshot = response.snapshot;

  if (!snapshot || Object.values(snapshot).length < 1 ||
    (!dataCache.initialized && dataCache.snapshots.length >= maxInitialSnapshots)) {
    if (!dataCache.initialized) {
      dataCache.initialized = true;
      dataCache.lastTimestamp = moment().unix();
    }
    return true;
  }

  var newSnapshot = { timestamp: response.timeslot.start };
  processCallback(snapshot, newSnapshot);

  if (dataCache.initialized) {
    dataCache.snapshots.push(newSnapshot);
  } else {
    dataCache.snapshots.unshift(newSnapshot);
  }

  if (dataCache.initialized) {
    dataCache.lastTimestamp = response.timeslot.stop;
  } else {
    dataCache.lastTimestamp = response.timeslot.start - snapshotInterval;
  }
}

function getDataForRCFromLastTimestamp(rc) {
  const dataCache = getCachedDataForRC(rc).rc;

  return api.getRCData(rc, dataCache.lastTimestamp).then(function (res) {

    const abort = prepareAndPushTimestamp(res, dataCache, function (snapshot, newSnapshot) {
      newSnapshot.peers = snapshot.peers;
      newSnapshot.prefix6 = snapshot.prefix6;
      newSnapshot.prefix4 = snapshot.prefix4;
      newSnapshot.prefix = snapshot.prefix6 + snapshot.prefix4;
      newSnapshot.announcedPrefixes = 0;
      if (dataCache.snapshots.length > 0) {
        if (dataCache.initialized) {
          const [lastSnapshot] = dataCache.snapshots.slice(-1);
          newSnapshot.announcedPrefixes = snapshot.prefix - lastSnapshot.prefix;
        } else {
          const lastSnapshot = dataCache.snapshots[0];
          lastSnapshot.announcedPrefixes = lastSnapshot.prefix - newSnapshot.prefix;
        }
      }
    });

    if (abort) {
      return;
    }

    return getDataForRCFromLastTimestamp(rc);
  });
}

function getDataForVPFromLastTimestamp(rc) {
  const dataCache = getCachedDataForRC(rc).vp;

  return api.getVPData(rc, null, dataCache.lastTimestamp).then(function (res) {

    const abort = prepareAndPushTimestamp(res, dataCache, function (snapshot, newSnapshot) {
      newSnapshot.valid = 0;
      newSnapshot.invalid = 0;
      newSnapshot.unknown = 0;

      for (const prefixes of Object.values(snapshot)) {
        for (const stats of Object.values(prefixes)) {
          newSnapshot.valid += stats.valid;
          newSnapshot.invalid += stats.invalid;
          newSnapshot.unknown += stats.unknown;
        }
      }

      const validated = newSnapshot.valid + newSnapshot.invalid;
      newSnapshot.validRatio = newSnapshot.valid / validated * 100;
      newSnapshot.invalidRatio = newSnapshot.invalid / validated * 100;
    });

    if (abort) {
      return;
    }

    return getDataForVPFromLastTimestamp(rc);
  });
}

function getDataForRC(rc) {
  return getDataForRCFromLastTimestamp(rc)
    .then(getDataForVPFromLastTimestamp(rc))
    .then(function () {
      return getCachedDataForRC(rc);
    })

    .catch(function (err) {
      console.error(err.stack);
    });
}

module.exports = {
  getDataForRC: getDataForRC
};
