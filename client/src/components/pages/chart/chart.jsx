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

  const options = {
    title: {
      text: 'Stock Chart'
    },
    yAxis:{
      title:{
        text: "stock price"
      }
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
        data: [1, 2, 3]
      },
      {
        name: '네이버',
        data: [3, 2, 1]
      }
    ]
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