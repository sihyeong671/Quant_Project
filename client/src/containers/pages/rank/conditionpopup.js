import {ConditionPopUp} from '../../../components/pages/rank/popup';
import React from 'react';
import {connect}  from 'react-redux';
import Constants from '../../../store/constants';

function mapStateToProps(state){

  return state.rank;
}

function mapDispatchToProps(dispatch){
  return{
    closePopUp: () => {
      dispatch({
        type: Constants.rank.CLOSECONDITION
      })
    },
    addCondition: (rlist) => {
      dispatch({
        type: Constants.rank.ADDCONDITION,
        list: rlist
      })
    }
  }
};


export default connect(mapStateToProps, mapDispatchToProps)(ConditionPopUp);
