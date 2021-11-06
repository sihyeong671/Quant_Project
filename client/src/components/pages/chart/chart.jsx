import React, {useState, useRef, useEffect} from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import HighchartsReact from 'highcharts-react-official';
import HighStock from 'highcharts/highstock';
import axios from 'axios';
import newLst from '../../../../data';
import Search from '../../../containers/search/search';

function getCode(list){
  return list.map(corp => corp.code);
}

function Chart(props){

  console.log("Chart rendering");
  

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
    series: [stockData],
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
      <form onSubmit={(e) => {
        e.preventDefault();
        const codeList = getCode(props.search.corpList);
        props.getStockData(codeList)}}>
        <Search maxLength={4}></Search>
        <button type="submit">확인</button>
      </form>

      <HighchartsReact
        highcharts={HighStock}
        constructorType={"stockChart"}
        options={options}
      />
    </>
  );
}

export default hot(module)(Chart);