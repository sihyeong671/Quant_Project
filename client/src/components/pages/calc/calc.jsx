import React, {useState, useRef, useEffect} from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import Search from '../../../containers/search/search';

function Calc(props){
  let years = [];
  for(let i = 2015; i < 2022; i ++){
    years.push(i.toString());
  }
  // console.log(props);
  const onSubmit = (e) => {
    e.preventDefault();
    // props.getFsData(e.target.);
    console.log(e);
  }

  let table = [];
  for(let fs in props.data){
    table.push(
      <tr>
        <td>{fs}</td>
        <td> 입력 값</td>
        <td> 수정 값</td>
      </tr>
    )
    
  }

  useEffect(() => {
    // api요청으로 기업 가져오기
  },[])
  //리스트로 수정

  return (
    <>
    <div>
      <form onSubmit={onSubmit}>

        <Search maxLength={1} />

        <select name="year">
          {years.map((year)=>(
            <option key = {year} value={year}>{year}</option>
          ))}
        </select>

        <select name="quarter">
          <option value="1">1분기</option>
          <option value="2">2분기</option>
          <option value="3">3분기</option>
          <option value="4">4분기</option>
        </select>

        <input id='CFS' type="radio" name='FS' value="CFS" defaultChecked/>
        <label htmlFor="CFS">CFS</label>
        <input id='OFS' type="radio" name='FS' value="OFS"/>
        <label htmlFor="OFS">OFS</label>
        
        <button type='submit'>제출</button>
      </form>

    </div>
      <table>
        <thead>
          <tr>
            <th> 재무제표</th>
            <th> 입력</th>
            <th> 수정값</th>
          </tr>
        </thead>
        <tbody>
          {table}
        </tbody>
      </table>
    </>
  )
}

export default hot(module)(Calc);