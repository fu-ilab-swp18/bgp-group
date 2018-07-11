var blessed = require('blessed'),
    contrib = require('blessed-contrib'),
    moment = require('moment'),
    numeral = require('numeral');

var screen = blessed.screen();
var grid = new contrib.grid({rows: 2, cols: 3, screen: screen});

var apiData = require('./data');

moment.locale('de');

numeral.register('locale', 'de', {
  delimiters: {
    thousands: '.',
    decimal: ','
  }
});
numeral.locale('de');

// announced prefixes

var prefixesChart = grid.set(0, 0, 1, 2, contrib.line, {
  label: 'Neu annoncierte Präfixe',
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
  label: 'RPKI-validierte Präfixe (in Prozent)',
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
  padding: 1
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
      prefixData.push([
        Math.round(row.validRatio), Math.round(row.invalidRatio)
      ]);
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
        ['Anzahl Peers:', numeral(stats.peers).format()],
        ['Bekannte Präfixe:', numeral(stats.prefix).format()],
        ['Davon IPv6:', numeral(stats.prefix6).format()],
        ['Davon IPv4:', numeral(stats.prefix4).format()],
        ['Letztes Update:', moment.unix(stats.timestamp).format("DD. MMM YYYY, HH:mm")]
      ]
    });

    screen.render();

    setTimeout(updateData, 300000);
  });
}

var currentInformationSlide = 0;
const informationSlides = [
  'Was ist BGP?\nDas Border Gateway Protocol (BGP) ist das im Internet eingesetzte Routingprotokoll und verbindet autonome Systeme (AS) miteinander. Diese autonomen Systeme werden in der Regel von Internetdienstanbietern gebildet. BGP wird allgemein als Exterior-Gateway-Protokoll (EGP) und Pfadvektorprotokoll bezeichnet und verwendet für Routing-Entscheidungen sowohl strategische wie auch technisch-metrische Kriterien, wobei in der Praxis meist betriebswirtschaftliche Aspekte berücksichtigt werden.',
  'Was ist RPKI?\nResource Public Key Infrastructure (RPKI), also known as Resource Certification, is a specialized public key infrastructure (PKI) framework designed to secure the Internet\'s routing infrastructure.',
  'Was ist ein AS?\nEin autonomes System (AS) ist laut klassischer Definition eine Menge von Routern (die mehrere Netzwerke verbinden) mit einem gemeinsamen inneren Gateway-Protokoll (IGP) und gemeinsamen Metriken, die bestimmen, wie Pakete innerhalb eines AS vermittelt werden, unter einer einzigen technischen Verwaltung.'
];

function updateInformationBox() {
  informationBox.setContent(informationSlides[currentInformationSlide]);
  currentInformationSlide = ++currentInformationSlide % informationSlides.length;
  screen.render();

  setTimeout(updateInformationBox, 10000);
}

updateData();
updateInformationBox();
