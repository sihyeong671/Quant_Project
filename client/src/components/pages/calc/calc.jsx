import React, {useState, useRef, useEffect} from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import Search from '../../../containers/search/search';

const Input = ({index, coef, changeCoef}) => {
  console.log("Input rendering")
  const [coefficient, setCoefficient] = useState(coef);
  const onChange = (e) => {
    e.preventDefault();
    setCoefficient(e.target.value);
    changeCoef([index[0], index[1]], e.target.value);
  }
  return(
    <input type="number" step='0.1' min="-10" max = '10' value={coefficient} onChange={(e) => onChange(e)}></input>
  );
}

const SubAccount = ({idx_1, subAccount, changeCoef}) => {
  console.log('SubAccount rendering');

  console.log(subAccount);
  const subAccountList = subAccount.map((subacnt, idx_2) => {
    return(
      <div key={idx_2}>
        <span>{subacnt.name}</span>
        <span>{subacnt.amount}</span>
        <Input coef={subacnt.coef} changeCoef={changeCoef} index={[idx_1, idx_2]}/>
      </div>
    )
  });
  return(
    <>
      {subAccountList}
    </>
  )
}

const Account = ({account, changeCoef}) => {
  const AccountList = account.map((acnt, idx_1)=>{
    return(
      <div key={idx_1}>
        <SubAccount subAccount={acnt.subAccount} changeCoef={changeCoef} idx_1={idx_1}/>
      </div>
    )
  })
  
  return(
    <>
      {AccountList}
    </>
  )
}


function Calc(props){

  useEffect(() => {
    // api요청으로 기업 가져오기
  },[])
  console.log(props);

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
    // props.sendCustom();
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
      <Account account={props.account} changeCoef={props.changeCoef}/>
      <button type='submit'>확인</button>
    </form>
    
    

    <div>
      청산가치
    </div>

    </>
  )
}

export default hot(module)(Calc);