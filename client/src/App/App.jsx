import React from 'react';
import { Link, Route, BrowserRouter as Router } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';

import Header from '../components/header/header';
import Footer from '../components/footer/footer';
import Main from '../components/main/main';

function App(){
  return (
    <>
      <Header></Header>
      <Main></Main> 
      <Footer></Footer>
    </>
  );
}


export default hot(module)(App);