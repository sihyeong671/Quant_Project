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
    // props.getFsData(e.target.);
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
            <th> </th>
            <th> </th>
            <th> </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{props.one}</td>
            <td></td>
            <td></td>
          </tr>
          <tr>
            <td>{props.two}</td>
            <td></td>
            <td></td>
          </tr>
          <tr>
            <td>{props.three}</td>
            <td></td>
            <td></td>
          </tr>
        </tbody>
      </table>
    </>
  )
}

export default hot(module)(Calc);