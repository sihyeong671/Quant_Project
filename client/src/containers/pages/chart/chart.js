import Chart from '../../../components/pages/chart/chart';
import React from 'react';
import {connect}  from 'react-redux';
import Constants from '../../../store/constants';

function mapStateToProps(state){
  return state.chart
}

function mapDispatchToProps(dispatch){
  return {
    
  }
}



export default connect(mapStateToProps, mapDispatchToProps)(Chart);

