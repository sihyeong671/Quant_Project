import React, { useState, useRef, useEffect } from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import './assets/css/style.scss';

const RankCondtion = (props) => {

  const [fsIndicators, setFsIndicators] = useState();
  //userEffect api로 정보 한번만 가져오기


  return(
    <div className = "popUp">
      순위 추가하기
      <div>
        <input type="text"/>
      </div>
      <button onClick={props.hideRank}>❌</button>
      <button onClick={props.hideRank}>확인</button>
      {/* 확인하면 오른쪽 창에 추가 후 조건 창 생성 */}
    </div>
  )
}

const Condition = (props) => {
  //userEffect 정보 한번만 가져오기
  const [llist, setLlist] = useState([
    'ROE',
    'LOL',
    'ROP',
    'PER',
  ]);

  const [rlist, setRlist] = useState([]);

  const pushVal = (i) =>{
    console.log(i);
    let tempList = [...rlist];
    tempList.push(i);
    setRlist(tempList);
    console.log(rlist);
  }

  return (
    <div className="popUp">
      <div className='popUp-inner'>
        <h2>조건추가하기</h2>
        <form>
          <input className='condition-input' name='condition-input' type="text" />
          <span className="material-icons">search</span>
        </form>
        <div className='condition_main'>
          <ul className='condition_main-slist'>
            {
              llist?.map((item, i)=>{
                return(
                  <li onClick={e=>pushVal(item)} key={i}>
                    <p>{item}</p>
                    <span className="material-icons">add_circle_outline</span>
                  </li>
                )
              })
            }
          </ul>
          <div className='condition_main-divLine'></div>
          <ul className='condition_main-rlist'>
            {
              rlist?.map((item, j)=>{
                return(
                  <li key={j}>
                    <h3>{item}</h3>
                    <div className='input-wrapper'>
                      <div className='uinput'>
                        <input type="text"/>
                        <button className='up'>이상</button>
                        <button className='down'>이하</button>
                      </div>
                      <div className='pinput'>
                        <input type="text"/>
                        <button className='up'>초과</button>
                        <button className='down'>미만</button>
                      </div>
                    </div>
                  </li>
                )
              })
            }
          </ul>
        </div>
        <div className='endBtn'>
          <button onClick={props.hideCondition}>취소</button>
          <button onClick={props.hideCondition}>확인</button>
        </div>
      </div>
      <div className='popUp-bg' onClick={props.hideCondition}></div>
    </div>
  )
}


function Rank(props) {
  console.log(props);

  const [conditionPopUp, setConditionPopUp] = useState(false);
  const [rankPopUp, setRankPopUp] = useState(false);

  const showCondition = () => { setConditionPopUp(true); };
  const hideCondition = () => { setConditionPopUp(false); }

  const showRank = () => { setRankPopUp(true); }
  const hideRank = () => { setRankPopUp(false); }

  return (
    <>
      <div className="container">
        <div className="container-box">

          <button onClick={showCondition}>조건 추가</button>
        </div>
        <div className="verticalLine">

        </div>
        <div className="container-box">

          <button onClick={showRank}>순위 추가</button>
        </div>
      </div>

      {conditionPopUp ? (
        <Condition hideCondition={hideCondition}></Condition>
      ) : null}
      {rankPopUp ? (
        <RankCondiion hideRank={hideRank}></RankCondiion>
      ) : null}

    </>
  )
}
export default hot(module)(Rank);