import { connect } from "react-redux";
import Header from "../../../components/base/header/header";
import Constants from '../../../store/constants';
import axios from 'axios';
import React from 'react';


function mapStateToProps(state){
  return {
    user: state.user
  };
}

function mapDispatchToProps(dispatch){
  return {
    basicLogOut: async function(){
      try{
        await axios.post('/api/v1/auth/logout');
        
        dispatch({
          type: Constants.user.LOGOUT
        })
      }catch(error){
        console.log(error);
      }
    }
  }
}

export default connect (mapStateToProps, mapDispatchToProps)(Header);