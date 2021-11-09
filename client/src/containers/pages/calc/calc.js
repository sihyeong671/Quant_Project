import { connect } from 'react-redux';
import React from 'react';
import Calc from '../../../components/pages/calc/calc';
import Constants from '../../../store/constants';
import axios from 'axios';
import { offset } from 'highcharts';

const mapStateToProps=(state)=>{

  const newState = {
    calc: state.calc,
    search: state.search,
    user: state.user
  }
  return newState;
}

const mapDispatchToProps=(dispatch)=>{
  return {
    // 서버에서 재무상태표 (BS) 받아오기
    getBsData: async (parameter) => {
      try{
        const res = await axios.post('api/v1/stock/account', parameter);
        console.log(res.data);
        dispatch({
          type: Constants.calc.GET,
          data: res.data
        })
      }catch(error){
        console.log(error);
      }
    },

    // 서버로 사용자가 커스텀한 숫자 전송
    sendCustom: async (parameter) => {

      try{
        const res = await axios.post('api/v1/stock/custombs', parameter);
        console.log(res);

      }catch(error){
        console.log(error);
      }
    },
    changeSubCoef: (idx, coef) => { // idx는 리스트
        dispatch({
          type: Constants.calc.CHANGESUB,
          coef: coef,
          index: idx
        });
      },
    changeCoef: (idx, coef) => { // idx 는 number
      dispatch({
        type: Constants.calc.CHANGE,
        coef: coef,
        index: idx
      })
    }
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(Calc);