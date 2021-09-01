import React, {useState, useRef} from 'react';
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import {Link} from 'react-router-dom';

import "./assets/style/style.scss";
import banner from './assets/img/1.jpg';

const Home=()=>{
  console.log("home rendering")
	return(
    <>
      <div className="search">
        인기검색
      </div>
      <div className="main-box-container">

        <Link 
          className="main-box" 
          style={{backgroundImage: `url(${banner})`}} 
          to ='/chart'
        >
          <span className="main-text">차트</span>
        </Link>

        <Link 
          className="main-box" 
          style={{backgroundImage: `url(${banner})`}} 
          to ='/calc'
        >
          <span className="main-text">연산</span>
        </Link>

        <Link 
          className="main-box" 
          style={{backgroundImage: `url(${banner})`}} 
          to ='/rank'
          >
            <span className="main-text">순위</span>
        </Link>

      </div>
    </>
	);
}

export default hot(module)(Home);