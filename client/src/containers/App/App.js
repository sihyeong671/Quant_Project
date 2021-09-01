import { connect } from 'react-redux';
import React from 'react';
import App from '../../App/App';
import Constants from '../../store/constants';
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
      try{
        const res = await axios.post('/api/v1/auth/login/refresh', data);
        console.log(res);
        dispatch({
          type:Constants.user.LOGIN_SUCCESS,
          username:res.data.user.username,
          accessToken:res.data.token,
          isAuthenticated:true
        })
        return true;
        
      }catch(error){
        console.log(error);
        return false
      }
    },
    reload: async() => {
      try{
        const res = await axios.post('/api/v1/auth/login/refresh');
        console.log(res);
        dispatch({
          type:Constants.user.LOGIN_SUCCESS,
          accessToken:res.data.access_token,
          isAuthenticated:true
        })
      }catch(error){
        console.log(error);
      }
    }

  }
}


export default connect(mapStateToProps, mapDispatchToProps)(App);