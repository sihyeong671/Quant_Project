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

  // const check = async ()=>{
  //   const res = await axios({
  //     method:'GET',
  //     url: '/api/v1/users/me',
  //   })
  //   console.log(res);
  // }

  return(
    <article className="profile">

      <section className="profile_user-info">
        <img className='info-img' src="" alt=""/>
        <h2></h2>
      </section>



    </article>
  );
}

export default hot(module)(Profile);