import { connect } from "react-redux";
import Header from "../../../components/base/header/header";
import Constants from '../../../store/constants';
import axios from 'axios';
import React from 'react';

function mapStateToProps(state){
  return state;
}

function mapDispatchToProps(dispatch){
  return {
    basicLogOut: async function(){
      try{
        // axios.post 로 하니 문제 생김
        const res = await axios({
          method: 'post',
          url: 'http://localhost:8000/api/v1/auth/logout/',
        })
        console.log(res)
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