import React, { useState } from 'react';
import { hot } from 'react-hot-loader';
import { Link } from "react-router-dom";
import Constants from "../../../store/constants";
import GoogleLogo from './assets/img/googlelogin.png';
import KakaoLogo from './assets/img/kakaologin.png';

import './assets/css/style.scss';

// #D3D5FD
// #929AAB
// #474A56
// #0B0B0D

function Login(props){
  console.log('Login rendering');
  const [id, setId] = useState('');
  const [pwd, setPwd] = useState('');

  const onChangeId = (e) => {
    e.preventDefault();
    setId(e.target.value);
  };

  const onChangePwd = (e) => {
    e.preventDefault();
    setPwd(e.target.value);
  };

  return(
    <div className="login">

      <h1>Login</h1>

      <div className='login-form'>
        <form onSubmit={(e) => props.basicLogin(e)}>
          <div className="input-area">
            <input id="username" name='username' type="text" onChange={(e) => onChangeId(e)} value={id}/>
            <label htmlFor='username'>USERNAME</label>
          </div>
          <div className="input-area">
            <input id="pwd" name='pwd' type="password" onChange={(e) => onChangePwd(e)} value={pwd}/>
            <label htmlFor="pwd">PASSWORD</label>
          </div>
          <div>
            <button type="submit">LOG IN</button>
          </div>
        </form>
      </div>
      
      <div className='social-btn'>
        <Link to="" style={{backgroundImage: `url(${KakaoLogo})`}}></Link>
        <Link to="" style={{backgroundImage: `url(${GoogleLogo})`}}></Link>
      </div>

      <div>
        <ul>
          <li><a href="#">아이디 찾기</a></li>
          <li><a href="#">비밀번호 찾기</a></li>
          <li><a href="#">회원가입</a></li>
        </ul>

      </div>

    </div>
  );
}

export default hot(module)(Login);