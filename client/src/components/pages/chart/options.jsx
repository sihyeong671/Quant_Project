
  export const priceOptions = ({data}) => {
    
  return {
      rangeSelector: {
        selected: 1
      },

      legend: {
        enabled: true
      },

      title: {
        text: 'Stock Chart'
      },

      yAxis: {
        title: {
          text: "stock price"
        },
        plotLines: [{
          value: 0,
          width: 2,
          color: "silver"
        }]
      },

      xAxis: {
        title: {
          text: "date"
        }
      },
      chart: {
        type: 'line'
      },
      series: data,
      plotOption:{
        series: {
          showInNavigator: true
        }
      },

      tooltip: {
        split: true,
        valueDecimals: 2
      },

      rangeSelector: {
        verticalAlign: 'top',
        x: 0,
        y: 0
      }
  }
}


export const pbrOptions = ({data}) => {

  return {
    rangeSelector: {
      selected: 1
    },

    legend: {
      enabled: true
    },

    title: {
      text: 'Stock Chart'
    },

    yAxis: {
      title: {
        text: "stock price"
      },
      plotLines: [{
        value: 0,
        width: 2,
        color: "silver"
      }]
    },

    xAxis: {
      title: {
        text: "date"
      }
    },
    chart: {
      type: 'line'
    },
    series: data,
    plotOption:{
      series: {
        showInNavigator: true
      }
    },

    tooltip: {
      split: true,
      valueDecimals: 2
    },

    rangeSelector: {
      verticalAlign: 'top',
      x: 0,
      y: 0
    }
  }
}

export const perOptions = {}

export const roeOptions = (data) => {

  return{
    chart: {
        type: 'column'
    },
    title: {
        text: 'Chart'
    },
    xAxis: {
      categories: []
    },
    yAxis: {
        min: 0,
        title: {
          text: 'ROE'
        }
    },
    tooltip: {
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
    series: []
  }
}

export const roaOptions = {}


