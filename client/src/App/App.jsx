import React,{useState, useEffect, useRef} from 'react';
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import axios from 'axios';

import Header from '../containers/base/header/header';
import Footer from '../components/base/footer/footer';
import Main from '../components/main/main';



function App(){
  const token = document.cookie;
  console.log(token);
  // useEffect(async (token) => {
    
  //   try{
  //     const res = await axios.post('/api/v1/auth/login/refresh',data={token});
  //     console.log(res);
  //   }catch(error){
  //     console.log(error);
  //   }
  // });
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