import { connect } from 'react-redux';
import React from 'react';
import App from '../../App/App';
import Constants from '../../../store/constants';
import axios from 'axios';



const mapStateToProps=(state)=>{

  return state.user;
}

const mapDispatchToProps=(dispatch)=>{
  return {
    // 이 부분 로직 확인 필요 async 가 두번 사용
    onSilentRefresh: async (token) => {
      const data = {
        token
      } 
      axios.post('/api/v1/auth/login/refresh', data)
    }
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(App);