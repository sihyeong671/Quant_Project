import React from 'react';
import { connect } from "react-redux";
import Constants from '../../store/constants';
import axios from 'axios';
import Main from '../../components/main/main';

function mapStateToProps(state){
  return state.main;
}

function mapDispatchToProps(dispatch){
  return {
    changeBG: async function(background){
      try{
        dispatch({
          type: Constants.main.BG_CHANGE,
          BG: background
        })
      }catch(error){ console.log(error); }
    }
  }
}

export default connect (mapStateToProps, mapDispatchToProps)(Main);