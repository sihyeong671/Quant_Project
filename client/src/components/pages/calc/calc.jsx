import React, {useState, useRef} from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';

function Calc(props){
  let years = [];
  for(let i = 2015; i < 2022; i ++){
    years.push(i.toString());
  }
  // console.log(props);
  const onSubmit = (e) => {
    e.preventDefault();
    console.log(e);

  }

  return (
    <>
    <div>
      <form onSubmit={onSubmit}>
        <input type="text" placeholder="기업명"/>
        <select name="year">
          {years.map((year)=>(
            <option key = {year} value={year}>{year}</option>
          ))}
        </select>
        <select name="quarter">
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
        </select>
        <input id='CFS' type="radio" name='FS' value="CFS" defaultChecked/>
        <label htmlFor="CFS">CFS</label>
        <input id='OFS' type="radio" name='FS' value="OFS"/>
        <label htmlFor="OFS">OFS</label>
        
        <button type='submit'>검색</button>
      </form>
    </div>
      <table>
        <thead>
          <tr>
            <th>재무제표</th>
            <th>입력 값</th>
            <th>수정 재무제표</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{props.one}</td>
            <td>입력</td>
            <td>수정값</td>
          </tr>
          <tr>
            <td>{props.two}</td>
            <td>입력</td>
            <td>수정값</td>
          </tr>
          <tr>
            <td>{props.three}</td>
            <td>입력</td>
            <td>수정값</td>
          </tr>
        </tbody>
      </table>
    </>
  )
}

export default hot(module)(Calc);