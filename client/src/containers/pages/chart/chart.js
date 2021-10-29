import Chart from '../../../components/pages/chart/chart';
import React from 'react';
import {connect}  from 'react-redux';
import Constants from '../../../store/constants';
import axios from 'axios';

function mapStateToProps(state){
  return state.chart
}

function mapDispatchToProps(dispatch){
  return {
    // 서버에서 주가 정보 받아오기
    getStockData: async () => {
      try{
        const res = await axios.get('api/v1/');
        console.log(res);
        dispatch({
          type: Constants.chart.GET,
          
        })
      }catch(error){
        console.log(error);
      }
    }
  }
}



export default connect(mapStateToProps, mapDispatchToProps)(Chart);

