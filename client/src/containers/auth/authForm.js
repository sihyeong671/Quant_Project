import { connect } from 'react-redux';
import React from 'react';
import AuthForm from '../../components/auth/login/authForm';
import Constants from '../../store/constants';
import axios from 'axios';

// 이메일 검사
function isvalidEmail(email) {

	let reg = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i;

	return reg.test(email);
}

// 비밀 번호 검사
function isVaildForm(pwd1, pwd2, email){
  let message = null;

  if(pwd1 !== pwd2){
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
          url: 'http://localhost:8000/api/v1/auth/login/',
          data:{
            username: username,
            password: pwd
            }
        })
        dispatch({
          type: Constants.user.LOGIN_SUCCESS,
          username: res.data.user.username,
        })
        return res.data.token;
        
      } catch(error){
        console.log(error);
      }
    },
    basicSignUp: async function(e){
      const [username ,pwd1, pwd2, email] = [
        e.target.username.value,
        e.target.pwd1.value,
        e.target.pwd2.value,
        e.target.email.value,
      ];
      // 유효성 검사
      const [check, message] = isVaildForm(pwd1, pwd2, email);
      if (!check){
        window.alert(message);
        return;
      }
      try{
        await axios({
          method:'post',
          url: 'http://localhost:8000/api/v1/auth/validate/username/',
          data:{
            username: username
          }
        })

        await axios({
          method:'post',
          url: 'http://localhost:8000/api/v1/auth/validate/email/',
          data:{
            email: email
          }
        }) 

        const res = await axios({
          method:'post',
          url: 'http://localhost:8000/api/v1/users/me',
          data:{
            username: username,
            password1: pwd1,
            password2: pwd2,
            email: email
          }
        })
        console.log(res);
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
          url: 'http://localhost:8000/api/v1/users/me/id',
          data:{
            email: email
          }
        })
        return res
      }catch(error){
        console.log(error)
      }
    },
    serachPwd: async () => {

    },
    kakaoLogin: async () => {

    },
    googleLogin: async () => {

    },
    naverLogin: async () => {

    },


  }
}



export default connect(mapStateToProps, mapDispatchToProps)(AuthForm);