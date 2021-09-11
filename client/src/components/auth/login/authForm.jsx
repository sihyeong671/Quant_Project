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

import Test from "../../../containers/pages/rank/rank";

import './assets/css/style.scss';

import srcSet from "./assets/src";

const authForm = (props) => (
  <div className="auth">
    <Switch>
      <Route exact path ='/auth/login' render={() => <Login basicLogin={props.basicLogin}/>}></Route>
      <Route path ='/auth/search_id' render={() => <SearchId searchId={props.searchId}/>}></Route>
      <Route path ='/auth/search_pwd' render={() => <SearchPwd searchPwd={props.searchPwd} sendCode={props.sendCode}/>}></Route>
      <Route path ='/auth/signup'  render={() => <SignUp basicSignUp={props.basicSignUp}/>}></Route>
    </Switch>

    <div className='social-btn'>
      <a className="social-kakao" href='http://localhost:8000/api/v1/auth/login/kakao'>
        <img src={srcSet.kakao} alt="kakaologin" />
        <span>카카오로 로그인</span>
      </a>

      <a className="social-google" href='http://localhost:8000/api/v1/auth/login/google'>
        <img src={srcSet.google} alt="googlelogin" />
        <span>구글로 로그인</span>
      </a>
      
      <a className="social-naver" href='http://localhost:8000/api/v1/auth/login/naver'>
        <img src={srcSet.naver} alt="naverlogin" />
        <span>네이버로 로그인</span>
      </a>
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