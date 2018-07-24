const blessed = require('blessed'),
      contrib = require('blessed-contrib'),
      moment = require('moment'),
      numeral = require('numeral');

const screen = blessed.screen();
const grid = new contrib.grid({rows: 9, cols: 3, screen: screen});

const apiData = require('./data');

const highlightBgColor = 'magenta';
const highlightFgColor = 'white';

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
  xPadding: 10,
  yPadding: 15,
  style: {
    line: highlightBgColor,
    text: highlightFgColor,
    baseline: 'yellow'
  },
  xLabelPadding: 5,
  yLabelPadding: 5,
  showLegend: true,
  wholeNumbersOnly: false
});

// validated prefixes

const validatedPrefixesChart = grid.set(4, 0, 4, 2, contrib.stackedBar, {
  label: 'RPKI-validierte Präfixe (in Prozent)',
  xPadding: 10,
  yPadding: 15,
  barWidth: 6,
  barSpacing: 15,
  xOffset: 5,
  barBgColor: ['green', 'red']
});

// information

const informationBox = grid.set(0, 2, 4, 1, blessed.box, {
  label: 'Allgemeines',
  padding: 2,
  tags: true
});

// statistics

const statisticsTableRC = grid.set(4, 2, 2, 1, contrib.table, {
  label: 'Statistik und Informationen für den Route Collector',
  interactive: false,
  fg: 'white',
  width: '100%',
  height: '100%',
  columnSpacing: 5,
  columnWidth: [30, 25],
});

const statisticsTableVP = grid.set(6, 2, 2, 1, contrib.table, {
  interactive: false,
  fg: 'white',
  width: '100%',
  height: '100%',
  columnSpacing: 5,
  columnWidth: [30, 25],
});

// RC selector

const maxRCNumber = process.env.MAX_RC_NUMBER || 0;
const selectorCommands = {};

for (var i = 0; i <= maxRCNumber; i++) {
  const rrcId = 'rrc' + (i < 10 ? '0' : '') + i;
  selectorCommands[rrcId] = {
    callback: function () {
      selectedVP = null;
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
      fg: highlightFgColor,
      bg: highlightBgColor,
    }
  }
});

// VP selector

const vpSelector = contrib.table({
  parent: screen,
  hidden: true,
  label: 'Vantage Point auswählen',
  tags: true,
  top: 'center',
  left: 'center',
  width: '30%',
  height: '70%',
  columnWidth: [10, 45],
  border: {
    type: 'line',
    fg: 'yellow'
  },
  shadow: true,
  fg: 'white',
  keys: true,
  selectedFg: highlightFgColor,
  selectedBg: highlightBgColor
});

vpSelector.rows.on('select', function (row) {
  const parts = row.content.split(/\s+/);

  if (parts[0] === 'alle') {
    selectedVP = null;
  } else {
    selectedVP = {
      as: parts[0],
      address: parts[1]
    };
  }
  vpSelector.hide();
  updateData();
})

vpSelector.rows.key(['escape'], function () {
  vpSelector.hide();
  screen.render();
});

screen.key(['escape', 'q', 'C-c'], function (_, key) {
  if (key.name !== 'escape' || !vpSelector.rows.focused || vpSelector.hidden) {
    return process.exit(0);
  }
});

screen.render();


var selectedRC = 'rrc00';
var selectedVP;
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
    var vpStats;
    data.vp.snapshots.forEach(function (row) {
      times.push(getFormattedTime(row.timestamp));
      var hasData = true;
      if (selectedVP) {
        var vpsRow = row.vps[`${selectedVP.as}|${selectedVP.address}`];
        if (vpsRow) {
          vpData = vpsRow;
          vpStats = row;
        } else {
          hasData = false;
        }
      } else {
        vpData = row.accumulated;
        vpStats = row;
      }
      if (hasData) {
        prefixData.push([
          Math.round(vpData.stats.validRatio), Math.round(vpData.stats.invalidRatio)
        ]);
      }
    });

    validatedPrefixesChart.setData({
      barCategory: times,
      stackedCategory: ['Gültig', 'Ungültig'],
      data: prefixData
    });


    const [stats] = data.rc.snapshots.slice(-1);
    statisticsTableRC.setData({
      headers: [],
      data: [
        ['ID:', `{bold}{${highlightBgColor}-fg}${selectedRC}`],
        ['Anzahl Peers:', numeral(stats.peers).format()],
        ['Bekannte Präfixe:', numeral(stats.prefix).format()],
        ['Davon IPv6:', numeral(stats.prefix6).format()],
        ['Davon IPv4:', numeral(stats.prefix4).format()],
        ['Letztes Update:', moment.unix(stats.timestamp).format('DD. MMM YYYY, HH:mm')]
      ]
    });


    const rows = [];
    if (selectedVP) {
      rows.push(['AS-Nummer:', `{bold}{${highlightBgColor}-fg}${vpData.as}`]);
      rows.push(['IP-Adresse des Routers:', `{bold}${vpData.address}`]);
      statisticsTableVP.setLabel('Daten für den Vantage Point');
    } else {
      statisticsTableVP.setLabel('Daten akkumuliert über alle Vantage Points dieses Route Collectors');
    }
    rows.push(['Gültige Präfixe:', numeral(vpData.stats.valid).format()]);
    rows.push(['Ungültige Präfixe:', numeral(vpData.stats.invalid).format()]);
    rows.push(['Nicht validierte Präfixe:', numeral(vpData.stats.unknown).format()]);
    rows.push(['Letztes Update:', moment.unix(vpStats.timestamp).format('DD. MMM YYYY, HH:mm')]);

    statisticsTableVP.setData({
      headers: [],
      data: rows
    });


    const [snapshot] = data.vp.snapshots.slice(-1);
    const vpSelectorData = {
      headers: ['AS-Nummer', 'IP-Adresse des Routers'],
      data: [['alle', '']]
    };
    for (const vpId in snapshot.vps) {
      const vp = snapshot.vps[vpId];
      vpSelectorData.data.push([vp.as, vp.address]);
    }
    vpSelector.setData(vpSelectorData);


    screen.render();

    clearTimeout(updateTimer);
    updateTimer = setTimeout(updateData, 300000);
  });
}

var currentInformationSlide = 0;
const informationSlides = [];

function addInformationSlide(title, content) {
  informationSlides.push(`{center}{bold}{${highlightBgColor}-fg}${title}{/${highlightBgColor}-fg}{/bold}{/center}\n\n${content}`);
}

addInformationSlide('Was ist BGP?', 'Das {bold}Border Gateway Protocol (BGP){/bold} ist das im Internet eingesetzte Routingprotokoll und verbindet autonome Systeme (AS) miteinander. Diese autonomen Systeme werden in der Regel von Internetdienstanbietern gebildet. BGP wird allgemein als Exterior-Gateway-Protokoll (EGP) und Pfadvektorprotokoll bezeichnet und verwendet für Routing-Entscheidungen sowohl strategische wie auch technisch-metrische Kriterien, wobei in der Praxis meist betriebswirtschaftliche Aspekte berücksichtigt werden.');
addInformationSlide('Was ist RPKI?', 'Die {bold}Resource Public Key Infrastructure (RPKI){/bold}, auch bekannt als Resource Certification, ist ein spezialisiertes Public-Key-Framework, das zur Absicherung der Internet-Routing-Infrastruktur eingesetzt wird. Es prüft und beglaubigt die Authentizität von annoncierten Präfixen. Diese Ergebnisse werden von zentralen Cache-Servern für Router bereitgestellt.');
addInformationSlide('Was ist ein AS?', 'Ein autonomes System (AS) ist laut klassischer Definition eine Menge von Routern (die mehrere Netzwerke verbinden) mit einem gemeinsamen inneren Gateway-Protokoll (IGP) und gemeinsamen Metriken, die bestimmen, wie Pakete innerhalb eines AS vermittelt werden, unter einer einzigen technischen Verwaltung.');

function updateInformationBox() {
  informationBox.setContent(informationSlides[currentInformationSlide]);
  currentInformationSlide = ++currentInformationSlide % informationSlides.length;
  screen.render();

  setTimeout(updateInformationBox, 10000);
}

updateData();
updateInformationBox();
