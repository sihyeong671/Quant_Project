import Rank from '../../../components/pages/rank/rank';
import React from 'react';
import Constants from '../../../store/constants';
import {connect}  from 'react-redux';


function mapStateToProps(state){
  return state.rank;
}

function mapDispatchToProps(dispatch){
  return{
    showCondition: () => {
      dispatch({
        type: Constants.rank.SHOWCONDITION
      })
    },
    showRankCondition: () => {
      dispatch({
        type: Constants.rank.SHOWRANKCONDITION
      })
    },
    deleteCondition: (idx) => {
      dispatch({
        type: Constants.rank.DELETECONDITION,
        index: idx
      })
    },
    deleteRankCondition: (idx) => {
      dispatch({
        type: Constants.rank.DELETERANKCONDITION,
        index: idx
      })
    }

  }
}


export default connect(mapStateToProps, mapDispatchToProps)(Rank);

