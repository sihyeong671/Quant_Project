import { connect } from 'react-redux';
import React from 'react';
import Search from '../../components/search/search';
import Constants from '../../store/constants';
import axios from 'axios';

const mapStateToProps=(state)=>{
  return state.search;
}

const mapDispatchToProps=(dispatch)=>{
  return {
    getFsData: async (corpName) => {
      try{
        // api만들면 수정
        const res = await axios.post('api/v1/');
        console.log(res);
        return res.data;
      }catch(error){
        console.log(error);
      }
    },
    onClickCreate: function(id, name, l){
      if (l >= 4){
        return;
      }
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