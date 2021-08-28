import React, {useState, useRef} from 'react';
import { Link, Route, BrowserRouter as Router } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import './assets/css/style.scss';

function Footer(){
  return(
    <div className="footer">
      <div className='foot-top'>
        <span>Quant</span>
      </div>
      
      <div className="foot-bottom">
        <span>GUIDE</span>

      </div>

      <div className="foot-bottom">
        <div>
          CONTACT
        </div>
        <div>
          projectquant@naver.com
        </div>
        <div>
          010 - 0000 - 0000
        </div>
      </div>

      <div className="foot-bottom">
        <div>ABOUT</div>
        <div>
          박시형 | 조현우 | 허상원
        </div>
      </div>
    </div>
  );
}

export default hot(module)(Footer);
