import React,{useEffect} from 'react';
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import {useCookies} from 'react-cookie';

import Header from '../containers/base/header/header';
import Footer from '../components/base/footer/footer';
import Main from '../components/main/main';

function App(){

  // 로그인 상태 확인 필요
  console.log('App rendering');
  
  
  useEffect(() => {
    console.log('asdf')
    // 토큰 유효성 확인
  }, [])

  return (
    <>
      <Header></Header>
      <Main></Main> 
      <Footer></Footer>
    </>
  );
}


export default hot(module)(App);