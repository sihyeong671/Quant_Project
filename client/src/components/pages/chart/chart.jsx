import React, { useState, useRef, useEffect } from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import HighchartsReact from 'highcharts-react-official';
import HighStock from 'highcharts/highstock';


import Search from '../../../containers/search/search';

import {Loading} from '../../../utils/utils'

import './assets/css/style.scss';


function getCode(list){
  return list.map(corp => corp.code);
}

function Chart(props){

  console.log("Chart rendering");
  
  const [isLoading, setIsLoading] = useState(false);

  let stockData = [];
  for(const [key, value] of Object.entries(props.chart)){
    let tmp = {
      name: '',
      data: []
    };
    tmp.name = key;
    tmp.data = value;
    stockData.push(tmp);
  }

  const options = {
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
    series: stockData,
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

  return (
    <>
      <form className='chart-form' onSubmit={(e) => {
        e.preventDefault();
        setIsLoading(true);
        const codeList = getCode(props.search.corpList);
        props.getStockData(codeList).then(res => {
          // setIsLoading(false);
        })
        }}>
        <Search maxLength={4}></Search>
        <button type="submit">확인</button>
      </form>

      <HighchartsReact
        highcharts={HighStock}
        constructorType={"stockChart"}
        options={options}
      />

      <div>
        준비중
        {isLoading? (<Loading/>):null}
      </div>
    </>
  );
}

export default hot(module)(Chart);