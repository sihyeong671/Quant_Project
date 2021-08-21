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
        <span>Guide</span>

      </div>

      <div className="foot-bottom">
        <span>문의 이메일: | 문의 전화번호: </span>
          
      </div>

      <div className="foot-bottom">
        <span>아이콘</span>
          
      </div>
      <div>
        <span>박시형|조현우|허상원</span>
      </div>
    </div>
  );
}

export default hot(module)(Footer);
