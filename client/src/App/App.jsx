import React from 'react';
import { Link, Route, BrowserRouter as Router } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';

import Header from '../containers/base/header/header';
import Footer from '../components/base/footer/footer';
import Main from '../components/main/main';

function App(){

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