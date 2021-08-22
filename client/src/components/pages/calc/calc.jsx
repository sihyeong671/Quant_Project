import React, {useState, useRef} from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';

function Calc(){
  return (
    <div> 연산 </div>
  )
}

export default hot(module)(Calc);