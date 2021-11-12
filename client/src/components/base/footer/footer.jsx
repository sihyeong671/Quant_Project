import React, { useState, useRef } from 'react';
import { Link, Route, BrowserRouter as Router } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import './assets/css/style.scss';

import logo from './assets/img/logo_w.png'

function Footer() {
  console.log("Footer rendering")
  return (
    <footer className="footer">
      <div className='footer-ico'>
        <div className='ico-img' style={{ backgroundImage: `url(${logo})` }}></div>
        <p>
          <strong>Q</strong>uant <br/>
          <strong>M</strong>anagement
        </p>
      </div>
      <div className='footer-copyrights'>
        <p>박시형 | 조현우 | 허상원</p>
        <div className='copyrights-mail'>
          <span className='material-icons'>mail</span>
          <a href='mailto:projectquant@naver.com'>projectquant@naver.com</a>
        </div>
        <span>@Copyright 2021 QuantManagement All rights reserved</span>
      </div>
    </footer>
  );
}

export default hot(module)(Footer);
