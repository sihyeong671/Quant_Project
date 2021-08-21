import Chart from '../../components/chart/chart';
import React from 'react';
import {connect}  from 'react-redux';
import Constants from '../../store/constants';

function mapStateToProps(state){
  return state
}

function mapDispatchToProps(dispatch){
  return {
    onClickCreate: function(id, name, l, e){
      e.preventDefault();
      //
      if (l >= 4){
        return
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
    // input 안의 값 조정
    // 제출시 corpList에 value 추가
    // input 초기화
}



export default connect(mapStateToProps, mapDispatchToProps)(Chart);

