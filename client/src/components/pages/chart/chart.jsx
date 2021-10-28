import React, {useState, useRef, useEffect} from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import HighchartsReact from 'highcharts-react-official';
import Highcharts from 'highcharts';
import axios from 'axios';

import Search from '../../../containers/search/search';

function Chart(props){
  console.log("Chart rendering");

  const data1 = []
  const data2 = []
  for(let i = 0; i < 100; ++i){
    data1.push(i);
    data2.push(i**2);
  }

  const options = {
    title: {
      text: 'Stock Chart'
    },
    yAxis:{
      title:{
        text: "stock price"
      },
      plotLines:[{
        value: 0,
        width: 2,
        color: "silver"
      }]
    },
    xAxis:{
      title:{
        text: "date"
      }
    },
    chart: {
      type: 'line'
    },
    series: [
      {
        name:'삼성',
        data: [...data1] 
      },
      {
        name: '네이버',
        data: [...data2] 
      }
    ],
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
      x : 0,
      y : 0
    }
  }

  return (
    <>
    <form onSubmit={props.getStockData}>
      <Search maxLength={4}></Search>
      <button type="submit">확인</button>
    </form>

      <HighchartsReact
        highcharts={Highcharts}
        options={options}
      />
    </>
  );
}

export default hot(module)(Chart);