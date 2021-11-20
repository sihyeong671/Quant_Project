import React from 'react';
import loading from './loading.gif';
import './style.scss'
export const BASEURL = "https://quant.or.kr";

export const Loading = () => {
  return (
    <>
      <img src={loading}></img>
      <div className="loading-bg"></div> 
    </>
  )
}