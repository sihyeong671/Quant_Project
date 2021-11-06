import React, { useState, useEffect } from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import Constants from "../../../store/constants";

import './assets/css/style.scss';

import { useCookies } from 'react-cookie';
import axios from 'axios';
// import axios from 'axios';


// 데이터 전체 삭제
// 데일리 데이터 주가 크롤링
// 다트 크롤링
// 재무제표 크롤링

const deleteAllCompany = () => {
  axios.delete('api/v1/stock/crawling/'); // 모든 데이터 삭제
}

const dailyCrawling = () => {
  axios.get('api/v1/stock/daily'); // 현재 존재하는 기업들 주가 가져오기(get)
}

const dartCrawling = () => {
  axios.get('api/v1/crawlingdart');
}

const fsCrawling = () => {
  axios.get('api/v1/crawlingfs');
}


const Profile=(props)=>{
  console.log('Profile rendering');
  return(
    <div>
      <button onClick={deleteAllCompany}>데이터 전체 삭제</button>
      <button onClick={dailyCrawling}>데일리 데이터 주가 크롤링</button>
      <button onClick={dartCrawling}>다트 크롤링</button>
      <button onClick={fsCrawling}>재무제표</button>
    </div>
  );
}

export default hot(module)(Profile);