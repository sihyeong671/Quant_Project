import { connect } from 'react-redux';
import React from 'react';
import Search from '../../../components/search/search';
import Constants from '../../../store/constants';
import axios from 'axios';

const mapStateToProps=(state)=>{
  return state.calc;
}

const mapDispatchToProps=(dispatch)=>{
  return {
    getFsData: async (corpName) => {
      try{
        // api만들면 수정
        const res = await axios.post('api/v1/');
        console.log(res);
        data = res.data;
      }catch(error){
        console.log(error);
      }
    }
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(Calc);