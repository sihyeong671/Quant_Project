import Profile from '../../components/auth/profile/profile'
import React from 'react';
import {connect}  from 'react-redux';


function mapStateToProps(state){
  return state
}

function mapDispatchToProps(){

}


export default connect(mapStateToProps, null)(Profile);

