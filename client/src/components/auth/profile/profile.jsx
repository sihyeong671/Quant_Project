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
  console.log('props',props);
  const [jwtToken, setJwtToken] = useState(`JWT ${props.accessToken}`);
  const [xcsrfToken, setXcsrfToken] = useState(cookies?.csrftoken);
  const [userInfo, setUserInfo] = useState();
  const [cookies, setCookie] = useCookies();
  
  // console.log(props);
  axios.defaults.headers.common['Authorization'] = jwtToken;
  axios.defaults.headers.common['X-CSRFToken'] = xcsrfToken;
  
  useEffect(async ()=>{
    try{
      await console.log('jwtToken', props);
      await console.log('jwtToken', xcsrfToken);
      const res = await axios({
        method:'GET',
        url: '/api/v1/users/me',
      })
      await console.log(res);
      await setUserInfo(res.data)
      await console.log('user: ',userInfo);
    }catch(err){
      console.log(err);
    }
    
    return(async ()=>{
      await axios({
        method:'GET',
        url: '/api/v1/users/me',
      })
      await console.log(res)
      await setUserInfo(res.data)
      await console.log('user: ',userInfo)
    })
  },[])

  return(
    <article className="profile_manage">

      <section className="profile-info">{}</section>

    </article>
  );
}

export default hot(module)(Profile);