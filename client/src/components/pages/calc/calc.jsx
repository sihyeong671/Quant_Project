import React, { useState, useRef, useEffect } from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import Search from '../../../containers/search/search';

import './assets/css/style.scss';


function commas(x) {
  try {
    if (x == NaN || x == 'NaN') { return 0; }
    else { return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }
  }
  catch (err) { return null; }
}

// 각 컴포넌트 따로 connect로 연결 해서 최적화 필요


// index : 리스트
const Input = ({ index, coef, changeFunction, pre_value }) => {
  console.log("Input rendering")
  const [coefficient, setCoefficient] = useState(coef);
  const onChange = (e) => {
    e.preventDefault();
    if (e.target.value == '') { // 빈 값을 넣으면 0이 되도록 함
      setCoefficient(0);
      changeFunction(index, 0);
      return;
    }
    setCoefficient(e.target.value); // 이거 지우고 하면 왜 값이 안바뀔까?
    changeFunction(index, e.target.value);
  }
  const changedValue = coefficient * pre_value;
  return (
    <div className='subAccount_value' key={"n" + index[0]}>
      <input type="number" step='0.1' min="-10" max='10' value={coefficient} onChange={(e) => onChange(e)}></input>
      <h3>=</h3>
      <span>{commas(changedValue.toFixed(2))}</span>
    </div>
  );
}

const SubAccount = ({ idx_1, subAccount, changeSubCoef }) => {
  console.log('SubAccount rendering');
  const subAccountList = subAccount.map((subacnt, idx_2) => {
    return (
      <div className='subAccount' key={idx_2}>
        <div className='subAccount_info'>
          <span className='subAccount-name'>{subacnt.name}</span>
          <span className='subAccount-amount'>{commas(subacnt.amount)}</span>
          <h3>x</h3>
        </div>
        <Input coef={subacnt.coef} changeFunction={changeSubCoef} index={[idx_1, idx_2]} pre_value={subacnt.amount} />
      </div>
    )
  });
  return (<>{subAccountList}</>)
}

// 비지배지분 input 값 넣어줘야함
const Account = ({ account, changeCoef, changeSubCoef }) => {
  useEffect(() => {
    return () => { }
  }, [])

  const [subAccountStyle, setSubAccountStyle] = useState(0);
  const setSubListStyle = (e) => {
    let fP = e.target.parentNode;
    let sP = fP.parentNode
    let tP = sP.parentNode
    let subList = tP.childNodes[1];
    if (subList.style.maxHeight == 'fit-content') {
      subList.style.maxHeight = 0;
      e.target.style.transform = 'rotateZ(90deg)';
      setSubAccountStyle(1);
    } else {
      subList.style.maxHeight = 'fit-content';
      e.target.style.transform = 'rotateZ(0deg)';
      setSubAccountStyle(0);
    }
  }

  const AccountList = account.map((acnt, idx_1) => {
    let amount;
    if (acnt.sub_account.length == 0) { amount = acnt.amount }

    const acntForm = () => {
      return (
        <>
          {
            acnt.fsname == "비지배지분" ? (
              <div className='account-vi'>
                <div className='subAccount_info'>
                  <span className='subAccount-name'>{acnt.fsname}</span>
                  <span className='subAccount-amount'>{commas(acnt.amount)}</span>
                  <h3>x</h3>
                </div>
                <Input index={[idx_1]} coef={acnt.coef} changeFunction={changeCoef} pre_value={acnt.amount}></Input>
              </div>
            ) : (
              <div className='account-base'>
                <div className='account-header'>
                  <div className='account-name-wrapper'>
                    <span className='account-name'>{acnt.fsname}</span>
                    <span className="material-icons" onClick={e => setSubListStyle(e)}>expand_more</span>
                  </div>
                  <span className='account-amount'>{commas(amount)}</span>
                </div>
                <div className='subaccount-wrapper'>
                  <SubAccount subAccount={acnt.sub_account} changeSubCoef={changeSubCoef} idx_1={idx_1} />
                </div>
              </div>
            )
          }
        </>
      )
    }
    return (<div className='account-wrapper' key={idx_1}>{acntForm()}</div>)
  })
  return (<>{AccountList}</>)
}

const ResultValue = ({ currentAsset, nonCurrentAsset, totalDebt }) => {

  const [botFix, setBotFix] = useState();
  const cirState = useRef();
  const [cirConState, setCirConState] = useState();
  
  const scrollAnim = () => {
    let target = cirState.current.getBoundingClientRect().top - window.scrollY;
    console.log(target);
    if (target < 0) {
      setBotFix({
        position: "relative",
        bottom: 0,
        padding: '20px 0'
      });
    } else {
      setBotFix({
        position: "fixed",
        bottom: 0
      });
    }
  };

  useEffect(() => {
    console.log('add'),
      window.addEventListener('scroll', scrollAnim)
    return () => {
      console.log('remove')
      window.removeEventListener('scroll', scrollAnim)
    }
  }, []);

  return (
    <>
      {/*
      청산가치 = 유동자산 + 비유동 자산 - 부채 총계
      보수적 계산법(벤자민 그레이엄) = 유동자산 - 부채총계 
    */}
      <hr className='calc-form' style={{ opacity: 0 }} ref={cirState}/>
      <div className='resVal' style={botFix}>
        <div className='resVal-value'>
          <h3>청산가치(Liquidation Value)</h3>
          <div>
            <span>{commas((currentAsset + nonCurrentAsset - totalDebt).toFixed(2))}</span>
          </div>
        </div>

        <div className='resVal-value'>
          <h3>보수적 청산 가치</h3>
          <div>
            <span>{commas((currentAsset - totalDebt).toFixed(2))}</span>
          </div>
        </div>
      </div>
    </>
  )
}

function Calc(props) {
  console.log('Calc rendering');
  // 값이 바뀌었을 때 리렌더링이 필요한 변수만 useState를 이용해 선언해줌 
  const [parameter, setParamter] = useState({});

  // 유동 자산
  let currentAsset;
  // 비유동 자산
  let nonCurrentAsset;
  // 부채 총계
  let totalDebt;

  props.calc.account?.forEach(acnt => {
    if (acnt.fsname === "유동자산") currentAsset = acnt.amount;
    else if (acnt.fsname === "비유동자산") nonCurrentAsset = acnt.amount;
    else if (acnt.fsname === "부채총계") totalDebt = acnt.amount;
  });

  let years = [];
  for (let i = 2015; i < 2022; i++) {
    years.push(i.toString());
  }

  const onSubmitGet = (e) => {
    e.preventDefault();
    const param = {
      code: props.search.corpList[0].code,
      name: props.search.corpList[0].name, // 필요없음
      year: e.target.year.value,
      quarter: e.target.quarter.value,
      link: e.target.FS.value,
      fs: "BS",
    }
    setParamter(param);
    props.getBsData(param);
  }

  const onSubmitSave = (e) => {
    e.preventDefault();

    console.log({
      ...parameter,
      account: props.calc.account,
      title: e.target.title.value
    });


    props.sendCustom({ // 커스텀 변수 보내서 사용자 정보에 저장
      ...parameter,
      account: props.calc.account,
      title: e.target.title.value
    });
  }

  return (
    <section className='calcPage'>
      <div className="calc-head">
        <form onSubmit={onSubmitGet}>

          <Search maxLength={1} />
          <div className='calc-filter'>
            <select className='filter-year select' name="year">
              {years.map((year) => (
                <option key={year} value={year}>{year}</option>
              ))}
            </select>

            <select className='filter-quarter select' name="quarter">
              <option value="11013">1분기</option>
              <option value="11012">2분기</option>
              <option value="11014">3분기</option>
              <option value="11011">4분기</option>
            </select>

            <div className='filter-CFS radio'>
              <input id='CFS' type="radio" name='FS' value="CFS" defaultChecked />
              <label htmlFor="CFS">CFS</label>
            </div>

            <div className='filter-OFS radio'>
              <input id='OFS' type="radio" name='FS' value="OFS" />
              <label htmlFor="OFS">OFS</label>
            </div>

            <button className='filter-submit' type='submit'>확인</button>

          </div>

        </form>
      </div>

      <div className='saved-list'>
        {props.user.userData.mybstitles?.map((element, idx) => (<div key={idx}>{element}</div>))}
      </div>

      <form onSubmit={onSubmitSave}>
        <div className='calc-save'>
          <input type="text" name="title" />
          <button type='submit'>저장하기</button>
        </div>
        {props.calc.account ? (
          <Account account={props.calc.account} changeCoef={props.changeCoef} changeSubCoef={props.changeSubCoef} />
        ) : null}
      </form>

      <ResultValue currentAsset={currentAsset} nonCurrentAsset={nonCurrentAsset} totalDebt={totalDebt}></ResultValue>

    </section>
  )
}

export default hot(module)(Calc);

