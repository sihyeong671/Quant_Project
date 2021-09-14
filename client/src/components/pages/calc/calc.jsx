import React, {useState, useRef, useEffect} from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import Search from '../../../containers/search/search';


const Input = ({name}) => {
  // 숫자만 넣을 수 있도록 조정하기
  const [coeffiecient, setCoeeficient] = useState(1);
  const onChange = (e) => {
    e.preventDefault();
    setCoeeficient(e.target.value);
  }
  return(
    <input type="text" name={name} onChange={onChange} value={coeffiecient}/>
  )

}

const SubAccount = ({subAccount}) => {
  console.log('SubAccount rendering');
  const subAccountList = subAccount.map((subacnt, idx) => {
    return(
      <div>
        <span>{subacnt.name}</span>
        <span>{subacnt.amount}</span>
        <Input name={subacnt.name}/>
      </div>
    )
  });
  return(
    <>
      {subAccountList}
    </>
  )
}

const Account = ({account}) => {
  console.log('Account rendering');

  const accountList = account.map((acnt, idx) =>{
    return(
      <div key={idx}>
        <div>{acnt.fsname}</div>
        <SubAccount subAccount={acnt.subAccount}/>
      </div>
      );
  });
  return(
    <>
      {accountList}
    </>
  );

}


function Calc(props){

  useEffect(() => {
    // api요청으로 기업 가져오기
  },[])
  console.log(props);
  for(let i = 0; i < props.account.length; i++){

  }

  let years = [];
  for(let i = 2015; i < 2022; i ++){
    years.push(i.toString());
  }
  // console.log(props);
  const onSubmitGet = (e) => {
    e.preventDefault();
    // props.getFsData(e.target.);
    console.log(e);
  }

  const onSubmitCalc = (e) => {
    e.preventDefault();
    console.log(e);
    console.log(e.target);
    console.log(e.target.input);
  }

  return (
    <>
    <div>
      <form onSubmit={onSubmitGet}>

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
    
    <form onSubmit={onSubmitCalc}>
      <Account account={props.account}/>
      <button type='submit'>확인</button>
    </form>
    
    <div>
      청산가치
    </div>

    </>
  )
}

export default hot(module)(Calc);