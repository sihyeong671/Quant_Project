import React, { useState, useRef } from 'react';
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import { Link } from 'react-router-dom';

import "./assets/style/style.scss";
import banner_b from './assets/img/banner_b.png';
import banner_w from './assets/img/banner.png';

const Home = () => {
  console.log("home rendering")
  return (
    <>
      <div className='main-banner' style={{backgroundImage: `url(${banner_w})`}}></div>

      <div className="main-box-container">
        <Link className="main-box" to='/chart'>
          <div className='main-text'>
            <span className="text-title">π<strong>μ°¨νΈ</strong></span>
            <p className="text-info">
              κΈ°μμ μ£Όκ° λ° μ§ν μ°¨νΈ λΉκ΅
            </p>
          </div>
          <div className='box-img' style={{ backgroundImage: `url(${banner_b})` }}></div>
        </Link>

        <Link className="main-box" to='/calc'>
          <div className='main-text'>
            <span className="text-title">π»<strong>μ°μ°</strong></span>
            <p className="text-info">
              μ¬λ¬΄μννμ μ°μ°
            </p>
          </div>
          <div className='box-img' style={{ backgroundImage: `url(${banner_b})` }}></div>
        </Link>

        <Link className="main-box" to='/rank'>
          <div className='main-text'>
            <span className="text-title">π₯<strong>μμ</strong></span>
            <p className="text-info">
              μ¬λ¬΄μ§ν μ‘°κ±΄μ λ°λ₯Έ μμ
            </p>
          </div>
          <div className='box-img' style={{ backgroundImage: `url(${banner_b})` }}></div>
        </Link>

      </div>
    </>
  );
}

export default hot(module)(Home);