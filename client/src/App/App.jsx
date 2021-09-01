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

  const [cookies, setCookie] = useCookies();
  useEffect(async() => {
    // csrf존재할때 코드수정해야 할 것 같음
    if (cookies.csrftoken !== undefined){
      console.log('헤더설정');
      axios.defaults.headers.post['X-CSRFToken'] = cookies.csrftoken;
      props.reload();
    }
    
    // setTimeout 필요
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