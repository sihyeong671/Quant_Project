import { connect } from 'react-redux';
import React from 'react';
import Calc from '../../../components/pages/calc/calc';
import Constants from '../../../store/constants';

const mapStateToProps=(state)=>{
  return state.calc;
}

const mapDispatchToProps=(dispatch)=>{
  return {}
}


export default connect(mapStateToProps, mapDispatchToProps)(Calc);