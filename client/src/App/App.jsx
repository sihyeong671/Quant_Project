import React,{useState, useEffect, useRef} from 'react';
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import axios from 'axios';
import { useCookies } from 'react-cookie';

import Header from '../containers/base/header/header';
import Footer from '../components/base/footer/footer';
import Main from '../components/main/main';



function App(props){
  const [cookies, setCookie, removeCookie] = useCookies(['toekn']);
  useEffect(async () => {
    if(cookies.jwt_token){
      props.onSilentRefresh(cookies.jwt_token);
    };
  },[]);
  //로그인 상태 확인 필요


  console.log('App rendering');
  return (
    <>
      <Header></Header>
      <Main></Main>
      <Footer></Footer>
    </>
  );
}


export default hot(module)(App);