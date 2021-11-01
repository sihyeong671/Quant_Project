import { connect } from 'react-redux';
import React from 'react';
import Search from '../../components/search/search';
import Constants from '../../store/constants';
import axios from 'axios';

const mapStateToProps=(state)=>{

  return state.search;
}

// async 는 promise를 반환
const mapDispatchToProps=(dispatch)=>{
  return {
    getFsData: async (corpName) => {
      try{
        // api만들면 수정
        const res = await axios.get('api/v1/stock/company');
        console.log(res.data);
        console.log(typeof(res.data));
        
        return res.data.company;
      }catch(error){
        console.log(error);
      }
    },
    onClickCreate: function(id, name){
      dispatch({
        type:Constants.search.CREATE,
        corpName :name,
        id: id
      })
    },
    onClickDelete: function(id){
      dispatch({
        type:Constants.search.DELETE,
        id: id
      })
    }
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(Search);