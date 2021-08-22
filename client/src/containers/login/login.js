import { connect } from 'react-redux';
import React from 'react';
import Login from '../../components/auth/login/login';
import Constants from '../../store/constants';
import axios from 'axios';

function mapStateToProps(state){
  
  return state;
}

function mapDispatchToProps(dispatch){
  return {
    basicLogin: function(e){
      // console.log(e);
      e.preventDefault(); 

      const username  = e.target.username.value;
      const pwd = e.target.pwd.value;
      if (username === "" || pwd === ""){
        window.alert("아이디 비밀번호를 입력해주세요");
        return;
      }

      let userData = {
        username: username,
        pwd: pwd
      }

      async () => {
        try{
          const userData = await axios({
            method:'post',
            url: 'http://localhost:8000/api/v1/auth/login/',
            data:{
              username: userData.username,
              password: userData.pwd
              }
          })
          dispatch({
            type:Constants.user.LOGIN_REQUEST,
            username:res.data.user.username,
          })
          setCookie('token', res.data.token, 1);
          // 유저데이터 
          
        } catch(error){
          window.alert(error);
        }
      console.log(userData);
      }

          



    }
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(Login);