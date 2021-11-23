import React, { useState, useRef, useEffect } from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import HighchartsReact from 'highcharts-react-official';
import HighStock from 'highcharts/highstock';
import HighChart from 'highcharts';


import Search from '../../../containers/search/search';

import {Loading} from '../../../utils/utils'
import {priceOptions, perOptions, pbrOptions} from './options'


import './assets/css/style.scss';


function getCode(list){
  return list.map(corp => corp.code);
}

function Chart(props){

  console.log("Chart rendering");
  
  const [isLoading, setIsLoading] = useState(false);

  let priceData = [];
  let perData = [];
  let pbrData = [];

  for(const [key, value] of Object.entries(props.chart)){
    let tmpPrice = {
      name: '',
      data: []
    };
    let tmpPer = {
      name: '',
      data: []
    };
    let tmpPbr = {
      name: '',
      data: []
    };
    if(value.length !== 0){
      tmpPrice.name = key;
      tmpPrice.data = value?.map(elements => {
        return [elements[0], elements[1]];
      });
      priceData.push(tmpPrice);
      tmpPer.name = key;
      tmpPer.data = value?.map(elements => {
        return [elements[0], elements[2]];
      });
      perData.push(tmpPer);
      tmpPbr.name = key;
      tmpPbr.data = value?.map(elements => {
        return [elements[0], elements[3]];
      });
      pbrData.push(tmpPbr);

    }
  }

  return (
    <>
      <form className='chart-form' onSubmit={(e) => {
        e.preventDefault();
        setIsLoading(true);
        const codeList = getCode(props.search.corpList);
        props.getStockData(codeList).then(res => {
          setIsLoading(false);
        })
        }}>
        <Search maxLength={4}></Search>
        <button type="submit">확인</button>
      </form>

      <HighchartsReact
        highcharts={HighStock}
        constructorType={"stockChart"}
        options={priceOptions(priceData)}
      />

      <HighchartsReact
        highcharts={HighStock}
        constructorType={"stockChart"}
        options={pbrOptions(pbrData)}
      />

      <HighchartsReact
        highcharts={HighStock}
        constructorType={"stockChart"}
        options={perOptions(perData)}
      />



      <div>
        {/* 준비중 */}
        {isLoading? (<Loading/>):null}
      </div>
    </>
  );
}

export default hot(module)(Chart);