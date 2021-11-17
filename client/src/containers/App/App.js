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
        const profileRes = await axios.get('api/v1/users/me'); //authform 로직 겹침
        console.log(profileRest.data)
        const [dateJoined, email, lastLogin, userName, profile, mybstitle] = [
          profileRes.data[0].date_joined,
          profileRes.data[0].email,
          profileRes.data[0].last_login,
          profileRes.data[0].username,
          profileRes.data[0].profile,
          profileRes.data[0].mybstitle
        ];
        dispatch({
          type:Constants.user.GETALL_SUCCESS,
          dateJoined: dateJoined,
          email: email,
          lastLogin: lastLogin,
          userName: userName,
          profile: profile,
          mybstitle: mybstitle,
          // 유저 데이터 전달
        })
      }catch(error){
        console.log(error);
      }
    }
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(App);