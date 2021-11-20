import React, { useState } from 'react';
import { hot } from 'react-hot-loader';
import { useHistory } from 'react-router';
import { Link } from "react-router-dom";
import { Cookies, useCookies } from 'react-cookie';
import axios from 'axios';

// 엔터 누르면 자동으로 submit이 된다
function Login({basicLogin, getUserData}){
  console.log('Login rendering');
  const [username, setUserName] = useState('');
  const [pwd, setPwd] = useState('');
  const history = useHistory();

  const onChangeUserName = (e) => {
    setUserName(e.target.value);
  };

  const onChangePwd = (e) => {
    setPwd(e.target.value);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    const check = await basicLogin(username ,pwd);
    
    if(check) {
      await getUserData();
      history.goBack();
    }
    else alert("다시")

    
  }

  return(
    <>
      <h1>로그인</h1>
      <div className='login-form'>
        <form onSubmit={onSubmit}>
          <div className="input-area">
            <input username="username" name='username' type="text" onChange={(e) => onChangeUserName(e)} value={username} required='required'/>
            <label htmlFor='username'>아이디</label>
          </div>
          <div className="input-area">
            <input id="pwd" name='pwd' type="password" onChange={(e) => onChangePwd(e)} value={pwd} required='required'/>
            <label htmlFor="pwd">비밀번호</label>
          </div>
          <div>
            <button type="submit">로그인</button>
          </div>
        </form>
      </div>
    </>
  );
}

export default hot(module)(Login);