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

function setValidationRatio(data) {
  const validated = data.valid + data.invalid;
  data.validRatio = data.valid / validated * 100;
  data.invalidRatio = data.invalid / validated * 100;
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
      newSnapshot.accumulated = {
        valid: 0,
        invalid: 0,
        unknown: 0
      }
      newSnapshot.vps = {};

      for (const as in snapshot) {
        const addresses = snapshot[as];
        for (const address in addresses) {
          const stats = addresses[address];
          setValidationRatio(stats);
          newSnapshot.vps[`${as}:${address}`] = {
            as: as,
            address: address,
            stats: stats
          }

          newSnapshot.accumulated.valid += stats.valid;
          newSnapshot.accumulated.invalid += stats.invalid;
          newSnapshot.accumulated.unknown += stats.unknown;
        }
      }

      setValidationRatio(newSnapshot.accumulated);
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
