import Chart from '../../../components/pages/chart/chart';
import React from 'react';
import {connect}  from 'react-redux';
import Constants from '../../../store/constants';

function mapStateToProps(state){
  return state.chart
}

function mapDispatchToProps(dispatch){
  return {
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
    },
    onClickGetData: function(data){
      dispatch({
        type:Constants.chart.UPDATE
      })
    }
  }
}



export default connect(mapStateToProps, mapDispatchToProps)(Chart);

