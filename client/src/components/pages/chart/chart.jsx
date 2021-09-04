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
      text: 'My chart'
    },
    series: [
      {data: [1, 2, 3]},
      {data: [3, 2, 1]}
    ]
  }

  return (
    <>
      <Search></Search>

      <HighchartsReact
        highcharts={Highcharts}
        options={options}
      />
    </>
  );
}

export default hot(module)(Chart);