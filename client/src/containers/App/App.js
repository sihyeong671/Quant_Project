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
    reload: async() => {
      try{
        const res = await axios.post('/api/v1/auth/login/refresh');
        console.log(res);
        const accessToken = res.data.access_token;
        axios.defaults.headers.common['Authorization'] = `JWT ${accessToken}`;
        dispatch({
          type:Constants.user.LOGIN_SUCCESS,
          accessToken:res.data.access_token,
          isAuthenticated:true
        })
        const profileRes = await axios.get('api/v1/users/me');
        // Logic 겹치는 데 분할해서 합칠 수 있나? 미들웨어 써야하나?
        const [dateJoined, email, lastLogin, userName] = [
          profileRes.data.date_joined,
          profileRes.data.email,
          profileRes.data.last_login,
          profileRes.data.username
          //profile 추가 필요
        ];
        dispatch({
          type:Constants.user.GETALL_SUCCESS,
          dateJoined: dateJoined,
          email: email,
          lastLogin: lastLogin,
          userName: userName
          // 유저 데이터 전달
        })
      }catch(error){
        console.log(error);
      }
    }
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(App);