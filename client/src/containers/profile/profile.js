import Profile from '../../components/auth/profile/profile'
import Rank from '../../components/pages/rank/rank';
import React from 'react';
import {connect}  from 'react-redux';


function mapStateToProps(state){
  return state.user
}

function mapDispatchToProps(dispatch){
  return {
    
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(Profile);

