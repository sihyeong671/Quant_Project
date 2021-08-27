import Rank from '../../components/pages/rank/rank';
import React from 'react';
import {connect}  from 'react-redux';


function mapStateToProps(state){
  return {
    title: state.title
  }
}

function mapDispatchToProps(){

}


export default connect(mapStateToProps, null)(Rank);

