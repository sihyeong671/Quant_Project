import React, {useState, useRef, useEffect} from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';

function Rank(props){
  console.log(props);

  
  return (
    <>
      <div> 순위 </div>
    </>
  )
} 
export default hot(module)(Rank);