import React from 'react';
import loading from './loading.gif';
import './style.scss'
export const BASEURL = "https://quant.or.kr";

export const Loading = () => {
  return (
    <div className='loading'>
      <img src={loading}></img>
      <div className="loading-bg"></div> 
    </div>
  )
}