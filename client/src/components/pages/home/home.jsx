import React, { useState, useRef } from 'react';
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import { Link } from 'react-router-dom';

import "./assets/style/style.scss";
import banner from './assets/img/1.jpg';

const Home = () => {
  console.log("home rendering")
  return (
    <>
      <div className="main-box-container">

        <Link className="main-box" to='/chart'>
          <div className='main-text'>
            <span className="text-title">📈차트</span>
            <p className="text-info">
              Lorem ipsum, dolor sit amet consectetur adipisicing elit. Vitae sequi eos distinctio illo.
            </p>
          </div>
          <div className='box-img' style={{ backgroundImage: `url(${banner})` }}></div>
        </Link>

        <Link className="main-box" to='/calc'>
          <div className='main-text'>
            <span className="text-title">🧮연산</span>
            <p className="text-info">
              Lorem ipsum, dolor sit amet consectetur adipisicing elit. Vitae sequi eos distinctio illo.
            </p>
          </div>
          <div className='box-img' style={{ backgroundImage: `url(${banner})` }}></div>
        </Link>

        <Link className="main-box" to='/rank'>
          <div className='main-text'>
            <span className="text-title">🥇순위</span>
            <p className="text-info">
              Lorem ipsum, dolor sit amet consectetur adipisicing elit. Vitae sequi eos distinctio illo.
            </p>
          </div>
          <div className='box-img' style={{ backgroundImage: `url(${banner})` }}></div>
        </Link>

      </div>
    </>
  );
}

export default hot(module)(Home);