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
            <span className="text-title">📈<strong>차트</strong></span>
            <p className="text-info">
              기업의 주가 및 지표 차트 비교
            </p>
          </div>
          <div className='box-img' style={{ backgroundImage: `url(${banner_b})` }}></div>
        </Link>

        <Link className="main-box" to='/calc'>
          <div className='main-text'>
            <span className="text-title">💻<strong>연산</strong></span>
            <p className="text-info">
              재무상태표의 연산
            </p>
          </div>
          <div className='box-img' style={{ backgroundImage: `url(${banner_b})` }}></div>
        </Link>

        <Link className="main-box" to='/rank'>
          <div className='main-text'>
            <span className="text-title">🥇<strong>순위</strong></span>
            <p className="text-info">
              재무지표 조건에 따른 순위
            </p>
          </div>
          <div className='box-img' style={{ backgroundImage: `url(${banner_b})` }}></div>
        </Link>

      </div>
    </>
  );
}

export default hot(module)(Home);