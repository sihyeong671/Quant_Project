import { connect } from 'react-redux';
import React from 'react';
import Calc from '../../../components/pages/calc/calc';
import Constants from '../../../store/constants';
import axios from 'axios';

const mapStateToProps=(state)=>{
  return state.calc;
}

const mapDispatchToProps=(dispatch)=>{
  return {
    getFsData: async (corpName) => {
      try{
        const res = await axios.get('api/v1/');
        console.log(res);
        dispatch({
          type: Constants.calc.GET,

        })
      }catch(error){
        console.log(error);
      }
    }
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(Calc);