var blessed = require('blessed'),
    contrib = require('blessed-contrib'),
    moment = require('moment');

var screen = blessed.screen();
var grid = new contrib.grid({rows: 2, cols: 3, screen: screen});

var apiData = require('./data');

// announced prefixes

var prefixesChart = grid.set(0, 0, 1, 2, contrib.line, {
  label: 'Annoncierte Präfixe',
  style: {
    line: 'yellow',
    text: 'white',
    baseline: 'black'
  },
  xLabelPadding: 3,
  xPadding: 5,
  showLegend: true,
  wholeNumbersOnly: false
});

// validated prefixes

var validatedPrefixesChart = grid.set(1, 0, 1, 2, contrib.stackedBar, {
  label: 'RPKI-validierte Präfixe',
  barWidth: 4,
  barSpacing: 15,
  xOffset: 0,
  // height: "40%",
  // width: "100%",
  barBgColor: ['green', 'red']
});

// information

var informationBox = grid.set(0, 2, 1, 1, blessed.box, {
  label: 'Allgemeines',
  content: 'Was ist BGP?\nDas Border Gateway Protocol (BGP) ist das im Internet eingesetzte Routingprotokoll und verbindet autonome Systeme (AS) miteinander. Diese autonomen Systeme werden in der Regel von Internetdienstanbietern gebildet. BGP wird allgemein als Exterior-Gateway-Protokoll (EGP) und Pfadvektorprotokoll bezeichnet und verwendet für Routing-Entscheidungen sowohl strategische wie auch technisch-metrische Kriterien, wobei in der Praxis meist betriebswirtschaftliche Aspekte berücksichtigt werden.'
});

// statistics

var statisticsTable = grid.set(1, 2, 1, 1, contrib.table, {
  label: 'Statistik und Informationen',
  interactive: false,
  fg: 'white',
  width: '100%',
  height: '100%',
  border: {type: "line", fg: "cyan"},
  columnSpacing: 5, //in chars
  columnWidth: [25, 25], /*in chars*/
});

screen.render();


var selectedRC = 'rrc00';

function getTimeDifference(timestamp) {
  return moment.unix(timestamp).fromNow();
}

function updateData() {
  apiData.getDataForRC(selectedRC).then(function (data) {
    var times = [];
    var prefixData = [];
    data.rc.snapshots.forEach(function (row) {
      times.push(getTimeDifference(row.timestamp));
      prefixData.push(row.announcedPrefixes);
    });

    prefixesChart.setData([
      {
        title: '',
        x: times,
        y: prefixData
      }
    ]);


    times = [];
    prefixData = [];
    data.vp.snapshots.forEach(function (row) {
      times.push(getTimeDifference(row.timestamp));
      prefixData.push([row.valid, row.invalid]);
    });

    validatedPrefixesChart.setData({
      barCategory: times,
      stackedCategory: ['Gültig', 'Ungültig'],
      data: prefixData
    });


    const [stats] = data.rc.snapshots.slice(-1);

    statisticsTable.setData({
      headers: [],
      data: [
        ['ID des Route Collectors:', selectedRC],
        ['Standort des RC:', 'DE-CIX Frankfurt'],
        ['Anzahl Peers:', stats.peers],
        ['Bekannte Präfixe:', stats.prefix],
        ['Davon IPv6:', stats.prefix6],
        ['Davon IPv4:', stats.prefix4],
        ['Letztes Update:', moment.unix(stats.timestamp).format("DD. MMM YYYY, HH:mm")]
      ]
    });

    screen.render();

    setTimeout(updateData, 300000);
  });
}

updateData();
