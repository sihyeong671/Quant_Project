import React, { useState, useEffect } from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import Constants from "../../../store/constants";

import './assets/css/style.scss';

import profileImg from './assets/img/1.jpg';
import {Loading} from '../../../utils/utils';

import { useCookies } from 'react-cookie';
import axios from 'axios';
// import axios from 'axios';

import { useHistory } from 'react-router';

// 데이터 전체 삭제
// 데일리 데이터 주가 크롤링
// 다트 크롤링
// 재무제표 크롤링




const Profile=(props)=>{

  const history = useHistory();
  const [isLoading, setIsLoading] = useState(false);

  const deleteAllCompany = async () => {
    try{
      setIsLoading(true);
      const res = await axios.delete('api/v1/stock/crawling/fs'); // 모든 데이터 삭제
      setIsLoading(false);
      console.log(res);
    }catch(error){
      console.log(error);
    }
  }
  
  const dailyCrawling = async () => {
    try{
      setIsLoading(true);
      const res = await axios.get('api/v1/stock/crawling/daily'); // 현재 존재하는 기업들 주가 가져오기(get)
      setIsLoading(false);
      console.log(res);
    }catch(error){
      console.log(error);
    }
  }
  
  const dartCrawling = async () => {
    try{
      setIsLoading(true);
      const res = await axios.get('api/v1/stock/crawling/dart'); // 고유번호 가져오기
      setIsLoading(false);
      console.log(res);
    }catch(error){
      console.log(error);
    }
  }
  
  const fsCrawling = async () => {
    try{
      setIsLoading(true);
      const res = await axios.get('api/v1/stock/crawling/fs'); // 재무제표 크롤링
      console.log(res);
    }catch(error){
      console.log(error);
    }
  }
  
  useEffect(()=>{
    console.log('props: ', props.isAuthenticated);
    if(props.accessToken == null){
      history.push('/');
    }
  },[])

  console.log('Profile rendering');
  return(
    <article className='profile-container'>
      <section className='profile-info'>
        <div className='info-img' style={{backgroundImage: `url(${profileImg})`,}}></div>
        <h1 className='info-username'>{props.userData.userName}</h1>
        <span className='info-datejoined'>{props.userData.dateJoined}</span>
        <button className='info-edit'>프로필 수정</button>
      </section>

      {
        props.userData.isSuperUser ? (
          <section className='admin-btns'>
            <h1>관리자 버튼</h1>
            <button onClick={deleteAllCompany}>데이터 전체 삭제</button>
            <button onClick={dailyCrawling}>데일리 데이터 주가 크롤링</button>
            <button onClick={dartCrawling}>다트 크롤링</button>
            <button onClick={fsCrawling}>재무제표</button>
          </section>
        ):(null)
      }


      <section className='saved-bstitle'></section>

    </article>
  );
}

export default hot(module)(Profile);