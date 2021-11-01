import React, {useState, useRef, useEffect} from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import Search from '../../../containers/search/search';

import './assets/css/style.scss';

const Input = ({index, coef, changeCoef, pre_value}) => {

  console.log("Input rendering")

  const [coefficient, setCoefficient] = useState(coef);

  const onChange = (e) => {
    e.preventDefault();
    setCoefficient(e.target.value);
    changeCoef([index[0], index[1]], e.target.value);
  }

  const changedValue = coefficient * pre_value;

  return(
    <div className='subAccount_value'>
      <input type="number" step='0.1' min="-10" max = '10' value={coefficient} onChange={(e) => onChange(e)}></input>
      <h3>=</h3>
      <span>{changedValue}</span>
    </div>
  );
}

const SubAccount = ({idx_1, subAccount, changeCoef}) => {
  console.log('SubAccount rendering');

  const subAccountList = subAccount.map((subacnt, idx_2) => {
    return(
      <div className='subAccount' key={idx_2}>
        <div className='subAccount_info'>
          <span className='subAccount-name'>{subacnt.name}</span>
          <span className='subAccount-amount'>{subacnt.amount}</span>
          <h3>x</h3>
        </div>
        <Input coef={subacnt.coef} changeCoef={changeCoef} index={[idx_1, idx_2]} pre_value={subacnt.amount}/>
      </div>
    )
  });
  return(
    <>
      {subAccountList}
    </>
  )
}

// 비지배지분 input 값 넣어줘야함
const Account = ({account, changeCoef}) => {

  const AccountList = account.map((acnt, idx_1)=>{

    let amount = ''
    if(acnt.sub_account.length == 0){
      amount = acnt.amount
    }

    return(
      <div className='account-wrapper' key={idx_1}>
        <span className='account-name'>{acnt.fsname}</span>
        <span className='account-amount'>{amount}</span>
        <SubAccount subAccount={acnt.sub_account} changeCoef={changeCoef} idx_1={idx_1}/>
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
  console.log('Calc rendering');
  const [customTitle, setCustomTitle] = useState('');

  const [parameter, setParameter] = useState({});

  // 유동 자산
  const [currentAsset, setCurrentAsset] = useState(0);

  // 비유동 자산
  const [nonCurrentAsset, setNonCurrentAsset] = useState(0);

  // 부채 총계
  const [totalDebt, setTotalDebt] = useState(0);

  // props.account.forEach(acnt => {
  //   if(acnt.fsname == "유동자산") setCurrentAsset(acnt.amount);
  //   else if(acnt.fsname == "비유동자산") setNonCurrentAsset(acnt.amount);
  //   else if(acnt.fsname == "부채총계") setTotalDebt(acnt.amount);
  // })

  

  let years = [];
  for(let i = 2015; i < 2022; i ++){
    years.push(i.toString());
  }
  
  const onSubmitGet = (e) => {
    e.preventDefault();
    const param = {
      id: props.corpList[0].id, //stock_code
      name: props.corpList[0].name,
      year: e.target.year.value,
      quarter: e.target.quarter.value,
      link: e.target.FS.value,
      fs: "BS",
    }

    setParameter(param);
    // props.getFsData(param);

    // console.log(props.corpList[0].id);
    // console.log(props.corpList[0].name);
    // console.log(e.target.year.value);
    // console.log(e.target.quarter.value);
    // console.log(e.target.FS.value);
  }

  const onSubmitSave = (e) => {
    e.preventDefault();
    console.log(e);
    //서버로 보내기
    // props.sendCustom({
    //   ...parameter,
    //   title: e.target.title.value
    // });
  }


  return (
    <>
    <div>
      <form onSubmit={onSubmitGet}>

        <Search maxLength={1} />

        <select name="year">
          {years.map((year)=>(
            <option key={year} value={year}>{year}</option>
          ))}
        </select>

        <select name="quarter">
          <option value="11013">1분기</option>
          <option value="11012">2분기</option>
          <option value="11014">3분기</option>
          <option value="11011">4분기</option>
        </select>

        <input id='CFS' type="radio" name='FS' value="CFS" defaultChecked/>
        <label htmlFor="CFS">CFS</label>
        <input id='OFS' type="radio" name='FS' value="OFS"/>
        <label htmlFor="OFS">OFS</label>
        
        <button type='submit'>확인</button>
      </form>
    </div>
    
    <form onSubmit={onSubmitSave}>
      <Account account={props.account} changeCoef={props.changeCoef}/>
      <input type="text" name="title"/>
      <button type='submit'>저장하기</button>
    </form>

    {/*
      보여줄 것 : 시가총액, 청산가치
      청산가치 = 유동자산 + 비유동 자산 - 부채 총계
      보수적 계산법(벤자민 그레이엄) = 유동자산 - 부채총계 
    */}
    <div>
      <div>
        청산가치(Liquidation Value)
        <span>{currentAsset + nonCurrentAsset - totalDebt}</span>
      </div>
      <div>
        보수적 청산 가치
        <span>{currentAsset - totalDebt}</span>
      </div>
      
    </div>
    </>
  )
}

export default hot(module)(Calc);
// export default Calc;


