var blessed = require('blessed'),
    contrib = require('blessed-contrib');

var screen = blessed.screen();
var grid = new contrib.grid({rows: 2, cols: 3, screen: screen});

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

prefixesChart.setData([
  {
    title: '',
    x: ['- 5 min', '- 10 min', '- 20 min', '- 30 min'],
    y: [7, -5, 5, 10]
  }
]);

// validated prefixes

var validatedPrefixesChart = grid.set(1, 0, 1, 2, contrib.stackedBar, {
  label: 'RPKI-validierte Präfixe',
  // barWidth: 4,
  barSpacing: 15,
  xOffset: 0,
  // maxValue: 15,
  // height: "40%",
  // width: "100%",
  barBgColor: ['yellow', 'green', 'red']
});

validatedPrefixesChart.setData({
  barCategory: ['- 5 min', '- 10 min', '- 20 min', '- 30 min'],
  stackedCategory: ['Unbekannt', 'Gültig', 'Ungültig'],
  data: [
    [7, 7, 5],
    [8, 2, 0],
    [0, 0, 0],
    [2, 3, 2]
  ]
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
  columnWidth: [20, 30], /*in chars*/
});

statisticsTable.setData({
  headers: [],
  data: [
    ['Standort des RC:', 'DE-CIX Frankfurt'],
    ['Anzahl Routen:', 5],
    ['Updates pro Minute:', 3]
  ]
});

screen.render();
