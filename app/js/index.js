//const GoldenLayout = require('imports?React=react&ReactDOM=react-dom!golden-layout')
import GoldenLayout from 'golden-layout'
const jquery = require('jquery')
import React from 'react'
import ReactDOM from 'react-dom'
import Highcharts from 'highcharts'

module.hot.accept();

Highcharts.theme = {
  "colors": ["#2A9BE6", "#C23C2A", "#FFFFFF", "#979797", "#FBB829"],
  "chart": {
    "backgroundColor": "#242F39",
    "style": {
      "color": "white"
    }
  },
  "legend": {
    "enabled": true,
    "align": "right",
    "verticalAlign": "bottom",
    "itemStyle": {
      "color": "#C0C0C0"
    },
    "itemHoverStyle": {
      "color": "#C0C0C0"
    },
    "itemHiddenStyle": {
      "color": "#444444"
    }
  },
  "title": {
    "text": {},
    "style": {
      "color": "#FFFFFF"
    }
  },
  "tooltip": {
    "backgroundColor": "#1C242D",
    "borderColor": "#1C242D",
    "borderWidth": 1,
    "borderRadius": 0,
    "style": {
      "color": "#FFFFFF"
    }
  },
  "subtitle": {
    "style": {
      "color": "#666666"
    }
  },
  "xAxis": {
    "gridLineColor": "#2E3740",
    "gridLineWidth": 1,
    "labels": {
      "style": {
        "color": "#525252"
      }
    },
    "lineColor": "#2E3740",
    "tickColor": "#2E3740",
    "title": {
      "style": {
        "color": "#FFFFFF"
      },
      "text": {}
    }
  },
  "yAxis": {
    "gridLineColor": "#2E3740",
    "gridLineWidth": 1,
    "labels": {
      "style": {
        "color": "#525252"
      },
      "lineColor": "#2E3740",
      "tickColor": "#2E3740",
      "title": {
        "style": {
          "color": "#FFFFFF"
        },
        "text": {}
      }
    }
  }
}
Highcharts.setOptions(Highcharts.theme);


var toneHist = {
  chart: {
    type: 'column'
  },
  title: {
    text: 'Average Tone Distribution'
  },
  xAxis: {
    gridLineWidth: 1
  },
  yAxis: {
    title: {
      text: 'Count'
    }
  },
  plotOptions: {
    column: {
      groupPadding: 0,
      pointPadding: 0,
      borderWidth: 0.9
    }
  },
  series: [{
    name: 'Histogram',
    pointPadding: 0,
    groupPadding: 0,
    pointPlacement: 'between'
  }],
  jsonURL: "http://localhost:9000/api/toneHistData"
};

var pieChart = {
  chart: {
    type: 'pie'
  },
  title: {
    text: 'Conflict Types - QuadClass'
  },
  tooltip: {
    pointFormat: '{point.desc}: <b>{point.percentage:.1f}%</b>'
  },
  plotOptions: {
    pie: {
      allowPointSelect: true,
      cursor: 'pointer',
      dataLabels: {
        enabled: true,
        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
        style: {
          color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
        }
      }
    }
  },
  series: [{
    name: 'Brands',
    colorByPoint: true
  }],
  jsonURL: "http://localhost:9000/api/quadPiData"
};

var config = {
    content: [{
        type: 'row',
        content: [{
            type: 'component',
            componentName: 'graph',
            componentState: {
              options: toneHist
            }
          },
          {
            type: 'column',
            content: [{
                type: 'component',
                componentName: 'graph',
                componentState: {
                  options: pieChart
                }},
                {
                type: 'component',
                componentName: 'list',
                componentState: {
                  jsonURL:'http://localhost:9000/api/toneListData'
                }
                }]
            }
          ]
        }]
    };

    var myLayout = new GoldenLayout(config, $('#layoutContainer'));

    var graphComponent = function(container, state) {
      this._highChartsConfig = state.options
      this._highChartsConfig.chart.renderTo = container.getElement()[0];
      this._container = container;
      this._state = state;
      this._chart = null;

      this._container.setTitle('Chart for ' + state.companyName);
      this._container.on('open', this._createChart.bind(this));
    };

    graphComponent.prototype._createChart = function() {
      console.log("open")
      this._chart = new Highcharts.Chart(this._highChartsConfig);
      this._update();
      this._bindContainerEvents();
    };

    graphComponent.prototype._update = function() {
      $.getJSON(this._state.options.jsonURL, (function(json) {
        this._jsonData = json;
        this._chart.series[0].setData(this._jsonData);
        /*this._chart.addSeries({
          colorByPoint: false,
          name: 'Histogram',
          data: (this._jsonData),
          pointPadding: 0,
          groupPadding: 0,
          pointPlacement: 'between'
        })*/
        console.log(this._chart);

      }).bind(this));
    };

    graphComponent.prototype._bindContainerEvents = function() {
      this._container.on('resize', this._setSize.bind(this));
      this._container.on('destroy', this._chart.destroy.bind(this._chart));
    };

    graphComponent.prototype._setSize = function() {
      this._chart.setSize(this._container.width, this._container.height);
    };

    var listComponent = function(container, state) {
      this._container = container;
      container.getElement().html("<ul class='ulist'></ul>");
      console.log(container.getElement().children())
      this._state = state;
      this._container.on('open', this._createList.bind(this));
    };

    listComponent.prototype._createList = function() {
      console.log("open")
      this._update();
    };

    listComponent.prototype._update = function() {
      $.getJSON(this._state.jsonURL, (function(json) {
        this._jsonData = json;
        for (var i =0; i<json.length; i++) {
          this._container.getElement().children().append("<li class='list'>" + json[i] + "</li>")
          console.log(json[i])
        }
        /*this._chart.addSeries({
          colorByPoint: false,
          name: 'Histogram',
          data: (this._jsonData),
          pointPadding: 0,
          groupPadding: 0,
          pointPlacement: 'between'
        })*/
        console.log(this._chart);

      }).bind(this));
    };

    myLayout.registerComponent('list', listComponent);
    myLayout.registerComponent('graph', graphComponent);
    myLayout.init();

    //TODO: updating
    /*
    var updateGraphs = function(){
      var components = myLayout.root
      console.log(components)
      for (var i =0; i<components.length;i++) {
        console.log(components[i])
      }
    }
    updateGraphs();*/

    $(window).resize(function() {
      myLayout.updateSize()
    })
