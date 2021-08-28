import { connect } from 'react-redux';
import React from 'react';
import AuthForm from '../../components/auth/login/authForm';
import Constants from '../../store/constants';
import axios from 'axios';

axios.defaults.baseURL = "http://localhost:8000";
axios.defaults.withCredentials = true;

// 이메일 검사
function isvalidEmail(email) {

	let reg = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i;

	return reg.test(email);
}

// 비밀 번호 검사
function isVaildForm(username, pwd1, pwd2, email){
  let message = null;
  if(username.length < 3){
    message = "아이디가 너무 짧습니다 3자리 이상으로 만들어 주세요"
    return [fasle, message];
  }

  else if (pwd1.length < 8){
    message = "비밀번호가 너무 짧습니다 8자리 이상으로 만들어주세요"
    return [false, message];
  }

  else if(pwd1 !== pwd2){
    message = "비밀번호가 일치하지 않습니다";
    return [false, message];

  }
  else if(!isvalidEmail(email)){
    message = "이메일이 형식에 맞지 않습니다";
    return [false, message];
  }

  return [true, message];
}

//
function mapStateToProps(state){
  return state;
}

function mapDispatchToProps(dispatch){
  return {
    basicLogin: async function(username, pwd){
      // 이벤트는 컴포넌트에서 처리하는 걸로 로직바꾸기
      try{
        const res = await axios({
          method:'post',
          url: '/api/v1/auth/login/',
          data:
          {
            username: username,
            password: pwd
          }
        })
        dispatch({
          type: Constants.user.LOGIN_SUCCESS,
          username: res.data.user.username,
          token: res.data.token
        })
      } catch(error){
        console.log(error);
      }
    },
    basicSignUp: async function(username, pwd1, pwd2, email){
      
      // 유효성 검사
      const [check, message] = isVaildForm(username, pwd1, pwd2, email);
      if (!check){
        window.alert(message);
        return;
      }
      try{
        await axios({
          method:'post',
          url: '/api/v1/auth/validate/username',
          data:{
            username: username
          }
        })

        await axios({
          method:'post',
          url: '/api/v1/auth/validate/email',
          data:{
            email: email
          }
        }) 

        const res = await axios({
          method:'post',
          url: '/api/v1/users/me/',
          data:{
            username: username,
            password1: pwd1,
            password2: pwd2,
            email: email
          }
        })
        // dispatch 유저 정보 저장
        
        // 토큰 저장
      }catch(error){
        console.log(error);
      }
    },
    searchId: async (email) => {
      try{
        const res = await axios({
          method: 'post',
          url: '/api/v1/users/me/id',
          data:{
            email: email
          }
        })
        if(res.status === 200)
          return res.data.id;
      }catch(error){
        console.log(error)
      }
    },
    serachPwd: async (username, email) => {
      try{
        const res = await axios({
          method: 'post',
          url: '/api/v1/users/me/password/code',
          data:{
            username: username,
            email: email
          }
        })
      }catch(error){
        console.log(error);
      }

    },
    sendCode: async (username, code) => {
      try{
        await axios({
          method:'post',
          url:'/api/v1/users/me/password/verifycode',
          data:{
            username: username,
            code: code
          }
        })
      }catch(error){
        console.log(error);
      }

    },
    kakaoLogin: async () => {
      try{
        await axios({
          method: 'post',
          url:'/api/v1/auth/login/kakao/callback'
        })
        // dispatch
      }catch(error){
        console.log(error);
      }
    },
    googleLogin: async () => {
      try{
        await axios({
          method: 'post',
          url:'/api/v1/auth/login/google'
        })
        // dispatch
      }catch(error){
        console.log(error);
      }
    },
    naverLogin: async () => {

    },


  }
}



export default connect(mapStateToProps, mapDispatchToProps)(AuthForm);