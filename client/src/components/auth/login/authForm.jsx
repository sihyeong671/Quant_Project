import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import React from 'react';

import Login from './login';
import SignUp from './signup';
import SearchId from './searchId';
import SearchPwd from './serachPwd';

import GoogleLogo from './assets/img/googlelogin.png';
import KakaoLogo from './assets/img/kakaologin.png';
import NaverLogo from './assets/img/naverlogin.png'

import './assets/css/style.scss';


const authForm = (props) => (
  <div className="auth">
    <Switch>
      <Route exact path ='/auth/login' render={() => <Login basicLogin={props.basicLogin}/>}></Route>
      <Route path ='/auth/search_id' render={() => <SearchId searchId={props.searchId}/>}></Route>
      <Route path ='/auth/search_pwd' render={() => <SearchPwd searchPwd={props.searchPwd} sendCode={props.sendCode}/>}></Route>
      <Route path ='/auth/signup'  render={() => <SignUp basicSignUp={props.basicSignUp}/>}></Route>
    </Switch>

    <div className='social-btn'>
      <a href='http://localhost:8000/api/v1/auth/login/kakao'><img src={KakaoLogo} alt="kakaologin" /></a>
      <a href='http://localhost:8000/api/v1/auth/login/kakao'><img src={GoogleLogo} alt="googlelogin" /></a>
      <a href='http://localhost:8000/api/v1/auth/login/kakao'><img src={NaverLogo} alt="naverlogin" /></a>
    </div>

    <div>
      <ul>
        <li><Link to ='/auth/search_id'>아이디 찾기</Link></li>
        <li><Link to ='/auth/search_pwd'>비밀번호 찾기</Link></li>
        <li><Link to='/auth/signup'>회원가입</Link></li>
      </ul>
    </div>
  </div>
);

export default hot(module)(authForm);