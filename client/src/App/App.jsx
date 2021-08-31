import React,{useState, useEffect, useRef} from 'react';
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import axios from 'axios';

import Header from '../containers/base/header/header';
import Footer from '../components/base/footer/footer';
import Main from '../components/main/main';


axios.defaults.withCredentials = true;

const JWT_EXPIRE_TIME = 24*3600*1000;

function App(props){
  const toekn = useRef('');
  useEffect(async (token) => {
    await props.onSilentRefresh(token);

  });
  // 로그인 상태 확인 필요


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