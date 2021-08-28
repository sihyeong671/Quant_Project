import React,{useState, useEffect} from 'react';
import { hot } from 'react-hot-loader';
import axios from 'axios';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import Cookies from 'universal-cookie';
import axios from 'axios';

import Header from '../containers/base/header/header';
import Footer from '../components/base/footer/footer';
import Main from '../components/main/main';


axios.defaults.withCredentials = true;

function App(){
  useEffect(async () => {
    const token = JSON.parse(JSON.parse(localStorage.getItem('persist:root')).user).token
    if (token !== null){
      try{
        await axios({
          method:'post',
          url:'http://localhost:8000/api/v1/auth/login/verify',
          data:{
            token:token
          }
        })
      }catch(error){
        await axios({
          method:'post',
          url:'http://localhost:8000/api/v1/auth/login/refresh',
          data:{
            token:token
          }
        })
        console.log(error);
      }
    }
  },[]
  );
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