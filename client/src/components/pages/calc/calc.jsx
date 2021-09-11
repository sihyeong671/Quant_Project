import React, {useState, useRef, useEffect} from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import Search from '../../../containers/search/search';


const Table = ({account}) => {
  console.log('Table render');
  
  // const[fixStock, setFixStock] = useEffect();

  let table = [];

  // . [] 차이는?
  // key값 어떻게 정하지?
  for(const idx in account){
    const fs = account[idx];
    table.push(
      <div key={idx}>
        <span>{fs.fsname}</span>
      </div>);
    for(const subIdx in fs.subAccount){
      const subFs = fs.subAccount[subIdx];
      table.push(
        <div key={subFs.amount}>
          <span>{subFs.name}</span>
          <span>{subFs.amount}</span>
          <input type="text" name={subFs.name}/>
          <span>수정후금액</span>
        </div>
      )
    }
  }

  return(
    <div>
      {table}
    </div>
  )
}

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
        
        <button type='submit'>확인</button>
      </form>
    </div>

    <Table
    account={props.account}></Table>

    <div>
      청산가치
    </div>

    </>
  )
}

export default hot(module)(Calc);