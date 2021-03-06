import Chart from '../../../components/pages/chart/chart';
import React from 'react';
import {connect}  from 'react-redux';
import Constants from '../../../store/constants';
import axios from 'axios';

function mapStateToProps(state){
  const newState = {
    search: state.search,
    chart: state.chart
    };
  return newState;
}

function mapDispatchToProps(dispatch){
  return {
    // 서버에서 주가 정보 받아오기
    getStockData: async (codeList) => {
      try{
        const param = {code : codeList};
        const res1 = await axios.post('api/v1/stock/chart/daily', param);

        dispatch({
          type: Constants.chart.GET,
          data: res1.data,

        })
      }catch(error){
        console.log(error);
      }
    }
  }
}



export default connect(mapStateToProps, mapDispatchToProps)(Chart);

