const blessed = require('blessed'),
      contrib = require('blessed-contrib'),
      moment = require('moment'),
      numeral = require('numeral');

const screen = blessed.screen();
const grid = new contrib.grid({rows: 9, cols: 3, screen: screen});

const apiData = require('./data');

moment.locale('de');

numeral.register('locale', 'de', {
  delimiters: {
    thousands: '.',
    decimal: ','
  }
});
numeral.locale('de');

// announced prefixes

const prefixesChart = grid.set(0, 0, 4, 2, contrib.line, {
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

const validatedPrefixesChart = grid.set(4, 0, 4, 2, contrib.stackedBar, {
  label: 'RPKI-validierte Präfixe (in Prozent)',
  barWidth: 4,
  barSpacing: 15,
  xOffset: 0,
  // height: "40%",
  // width: "100%",
  barBgColor: ['green', 'red']
});

// information

const informationBox = grid.set(0, 2, 4, 1, blessed.box, {
  label: 'Allgemeines',
  padding: 1
});

// statistics

const statisticsTable = grid.set(4, 2, 4, 1, contrib.table, {
  label: 'Statistik und Informationen',
  interactive: false,
  fg: 'white',
  width: '100%',
  height: '100%',
  border: {type: "line", fg: "cyan"},
  columnSpacing: 5, //in chars
  columnWidth: [25, 25], /*in chars*/
});

// RC selector

const maxRCNumber = process.env.MAX_RC_NUMBER || 0;
const selectorCommands = {};

for (var i = 0; i <= maxRCNumber; i++) {
  const rrcId = 'rrc' + (i < 10 ? '0' : '') + i;
  selectorCommands[rrcId] = {
    callback: function () {
      selectedRC = rrcId;
      updateData();
    }
  };
  selectorCommands['Nach Vantage Point filtern'] = {
    callback: function () {
      vpSelector.show();
      vpSelector.focus();
    }
  };
}

const rcSelector = grid.set(8, 0, 1, 3, blessed.listbar, {
  label: 'Perspektive des folgenden Route Collectors anzeigen',
  commands: selectorCommands,
  autoCommandKeys: true,
  style: {
    selected: {
      fg: 'white',
      bg: 'magenta',
    }
  }
});

// VP selector

const vpSelector = blessed.list({
  parent: screen,
  hidden: true,
  label: 'Vantage Point auswählen',
  tags: true,
  top: 'center',
  left: 'center',
  width: '30%',
  height: '70%',
  border: 'line',
  shadow: true,
  keys: true,
  style: {
    selected: {
      fg: 'white',
      bg: 'magenta',
    }
  }
});

vpSelector.on('select', function (_, vpIndex) {
  vpSelector.hide();
  selectedVPIndex = vpIndex;
  updateData();
})

vpSelector.key(['escape'], function () {
  vpSelector.hide();
  screen.render();
});

screen.key(['escape', 'q', 'C-c'], function (_, key) {
  if (key.name !== 'escape' || !vpSelector.focused) {
    return process.exit(0);
  }
});

screen.render();


var selectedRC = 'rrc00';
var selectedVPIndex;
var updateTimer;

function getFormattedTime(timestamp) {
  return moment.unix(timestamp).format('LT');
}

function updateData() {
  apiData.getDataForRC(selectedRC).then(function (data) {
    var times = [];
    var prefixData = [];
    var minY = 0;
    data.rc.snapshots.forEach(function (row) {
      times.push(getFormattedTime(row.timestamp));
      prefixData.push(row.announcedPrefixes);
      minY = Math.min(minY, row.announcedPrefixes);
    });

    prefixesChart.options.minY = minY;
    prefixesChart.setData([
      {
        title: '',
        x: times,
        y: prefixData
      }
    ]);


    times = [];
    prefixData = [];
    var vpData;
    data.vp.snapshots.forEach(function (row) {
      times.push(getFormattedTime(row.timestamp));
      var data = row.accumulated;
      if (selectedVPIndex) {
        vpData = row.vps[Object.keys(row.vps)[selectedVPIndex]];
        data = vpData.stats;
      }
      prefixData.push([
        Math.round(data.validRatio), Math.round(data.invalidRatio)
      ]);
    });

    validatedPrefixesChart.setData({
      barCategory: times,
      stackedCategory: ['Gültig', 'Ungültig'],
      data: prefixData
    });


    const [stats] = data.rc.snapshots.slice(-1);
    var rows = [
      [`{bold}Daten für ${selectedRC}`],
      ['Anzahl Peers:', numeral(stats.peers).format()],
      ['Bekannte Präfixe:', numeral(stats.prefix).format()],
      ['Davon IPv6:', numeral(stats.prefix6).format()],
      ['Davon IPv4:', numeral(stats.prefix4).format()]
    ];

    if (selectedVPIndex) {
      rows.push(['']);
      rows.push([`{bold}Daten für ${vpData.as}: ${vpData.address}`]);
      rows.push(['Gültige Präfixe:', numeral(vpData.stats.valid).format()]);
      rows.push(['Ungültige Präfixe:', numeral(vpData.stats.invalid).format()]);
      rows.push(['Nicht validierte Präfixe:', numeral(vpData.stats.unknown).format()]);
    }

    rows.push(['']);
    rows.push(['Letztes Update:', moment.unix(stats.timestamp).format('DD. MMM YYYY, HH:mm')]);

    statisticsTable.setData({
      headers: [],
      data: rows
    });


    const [snapshot] = data.vp.snapshots.slice(-1);
    vpSelector.clearItems();
    for (const vpId in snapshot.vps) {
      const vp = snapshot.vps[vpId];
      vpSelector.addItem(`{bold}${vp.as}{/bold}: ${vp.address}`);
    }


    screen.render();

    clearTimeout(updateTimer);
    updateTimer = setTimeout(updateData, 300000);
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
