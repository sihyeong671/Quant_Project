import React, { useState, useEffect } from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import Constants from "../../../store/constants";

import './assets/css/style.scss';

import { useCookies } from 'react-cookie';
import axios from 'axios';
// import axios from 'axios';


const Profile=(props)=>{
  console.log('Profile rendering');

  const [userInfo, setUserInfo] = useState();

  const check = async ()=>{
    const res = await axios({
      method:'GET',
      url: '/api/v1/users/me',
    })
    console.log(res);
  }
  
  // useEffect(async ()=>{
  // })

  return(
    <article className="profile_manage">

      <section className="profile-info"></section>
      {/* <button onClick={check}>Click Me!</button> */}
    </article>
  );
}

export default hot(module)(Profile);