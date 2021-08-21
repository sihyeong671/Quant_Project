import React, {useState, useRef} from 'react';
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import "./assets/style/style.scss";
import {Link} from 'react-router-dom';

function Home(){
	return(
    <>
      <div className="search">
        인기검색
      </div>
      <div className="main-box-container">
        <div className="main-box">
          <Link to ='/chart'>차트</Link>
        </div>

        <div className="main-box">
          <Link to ='/calc'>연산</Link>
        </div>  

        <div className="main-box">
          <Link to ='/rank'>순위</Link>
        </div>
      </div>
    </>
	);
}

export default hot(module)(Home);