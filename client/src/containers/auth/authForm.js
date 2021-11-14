import { connect } from 'react-redux';
import React from 'react';
import AuthForm from '../../components/auth/login/authForm';
import Constants from '../../store/constants';
import axios from 'axios';



const onSilentRefresh = async(token) => {
  const res = await axios.post('/api/v1/auth/login/refresh', data={token});
  return res.data;
}

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
  return state; // 수정 필요
}



//
function mapDispatchToProps(dispatch){
  return {
    // local 로그인 함수
    basicLogin: async function(username, pwd){
      const data = {
        "username":username,
        "password":pwd
      }
      try{
        const res = await axios.post('/api/v1/auth/login/', data);
        console.log(res);
        const accessToken = res.data.access_token;
        axios.defaults.headers.common['Authorization'] = `JWT ${accessToken}`;
        // 만료시간 3분 이기 때문에 서버에서 201오류 날때 refresh토큰으로 갱신 필요
        // post 작업에 모두 accesstoken 이 유효한지 검사필요
        dispatch({
          type: Constants.user.LOGIN_SUCCESS,
          accessToken: accessToken,
          isAuthenticated:true
        })
        return true;
      }catch(error){
        console.log(error);
        return false;
      }
    },
    // local 회원가입 함수
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
          url: '/api/v1/auth/validate/username/',
          data:{
            username: username
          }
        })

        await axios({
          method:'post',
          url: '/api/v1/auth/validate/email/',
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
        console.log(res);
        dispatch({
          type: Constants.user.REGISTER_SUCCESS,
          accessToken: res.data.access_token,
          isAuthenticated:true
        })

        return true;
      }catch(error){
        console.log(error);
        return false;
      }
    },
    getUserData: async () => {
      try{
        const profileRes = await axios.get('api/v1/users/me');
        console.log(profileRes.data);
        const [dateJoined, email, lastLogin, userName, profile, mybstitle] = [
          profileRes.data[0].date_joined,
          profileRes.data[0].email,
          profileRes.data[0].last_login,
          profileRes.data[0].username,
          profileRes.data[0].profile,
          profileRes.data[0].mybstitle,
        ];
        console.log(dateJoined, email, lastLogin, userName, profile, mybstitle)
        dispatch({
          type:Constants.user.GETALL_SUCCESS,
          dateJoined: dateJoined,
          email: email,
          lastLogin: lastLogin,
          userName: userName,
          profile: profile,
          mybstitle: mybstitle,
      })
      }catch(error){
        console.log(error);
      }
    },
    searchId: async (email) => {
      try{
        const res = await axios({
          method: 'post',
          url: '/api/v1/users/me/id/',
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
        await axios.get('/api/v1/auth/login/kakao')
        // dispatch
      }catch(error){
        console.log(error);
      }
    },
    googleLogin: async () => {
      try{
        await axios.get('/api/v1/auth/login/google');
        // dispatch
      }catch(error){
        console.log(error);
      }
    }
  }
}



export default connect(mapStateToProps, mapDispatchToProps)(AuthForm);