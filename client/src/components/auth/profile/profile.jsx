import React, { useState } from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import Constants from "../../../store/constants";

import './assets/css/style.scss';

import user from './assets/img/1.jpg';

const LikedCompany=()=>{
  return(
    <div>Liked Company</div>
  )
}

const LikedArticle=()=>{
  return(
    <div>Liked Article</div>
  )
}

const EditProfile=()=>{
  return(
    <div>Edit Profile</div>
  )
}

const Profile=(props)=>{
  console.log('Profile rendering');

  const [id, setId] = useState('');
  const [pwd, setPwd] = useState('');

  return(
    <article className="profile_manage">

      <section className="user_info">

        <div className="user_info-media">
          <img className="media-img" src={user} alt="대표 이미지"/>
          <span className="media-name"><strong>User</strong></span>
          <button className="media-edit">Edit Profile</button>
        </div>

        <div className="user_info-desc">
          <div className="desc_in">
            <span className="desc-corp">Corperation: <strong>PROJECT</strong></span>
            <span className="desc-email">E-mail: <strong>tester3528@test.com</strong></span>
            <span className="desc-adress">Adress: <strong>Busan Gwangan Suyeong</strong></span>
            <p className="desc-text">
              <strong>Description</strong>
              Lorem ipsum dolor sit amet consectetur, adipisicing elit. 
              Doloremque sed dicta obcaecati unde laborum exercitationem dolore facere repudiandae inventore. 
              Est aut veritatis, accusamus vero facilis incidunt quis culpa beatae! Porro.
            </p>
          </div>
        </div>

      </section>

      
      <section className="user_stat">
        <div className="stat-nav">
          <Link to="/profile">관심 기업 목록</Link>
          <Link to="/profile/like">좋아요 누른 글</Link>
        </div>

        <div className="stat-route">
          <Switch>
            <Route exact path="/profile" component={LikedCompany}></Route>
            <Route exact path="/profile/like" component={LikedArticle}></Route>
            <Route exact path="/profile/edit" component={EditProfile}></Route>
          </Switch>
        </div>
      </section>

    </article>
  );
}

export default hot(module)(Profile);