import React, { useState, useRef, useEffect } from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';

import ConditionPopUp from '../../../containers/pages/rank/conditionpopup';
import RankConditionPopUp from '../../../containers/pages/rank/rankconditionpopup';

import './assets/css/style.scss';




function Rank(props) {

  const getParameter = () => {
    const parameter = {
      case: [...props.condition],
      rank: [...props.rankCondition],
      islink: true // 나중에 파라미터 받는걸로 고치기 ##
    }
    return parameter;
  }
  console.log("Rank rendering")
  return(
    <>
      <div className="container">
        <div className="container-box">
          {props.condition.map((cond, idx) => {
            let element;
            switch(cond[1]){ //
              case 0:
                element = <span>%하위</span>
                break
              case 1:
                element = <span>%상위</span>
                break
              case 2:
                element = <span>이하</span>
                break
              case 3:
                element = <span>이상</span>
                break
            }
            return(
              <div key={idx}>
                <span>{cond[0]}</span>
                <span>{cond[2]}</span>
                {element}
                <button onClick={e => props.deleteCondition(idx)}>❌</button>
              </div>
            )
          })}
          <button onClick={props.showCondition}>조건 추가</button>
        </div>

        <div className="verticalLine"></div>

        <div className="container-box">
          {props.rankCondition.map((rcond, idx) => {
            let rankElement;
            if(rcond[1] === 1){
              rankElement = <span>오름차순</span>
            }
            else if(rcond[1] === 0){
              rankElement = <span>내림차순</span>
            }
            return(
              <div key={idx}>
                <span>{rcond[0]}</span>
                {rankElement}
                <button onClick={e => props.deleteRankCondition(idx)}>❌</button>
              </div>
            )
          })}
          <button onClick={props.showRankCondition}>순위 추가</button>
        </div>
      </div>

      {props.conditionPopUp ? (
        <ConditionPopUp></ConditionPopUp>
      ) : null}
      {props.rankConditionPopUp ? (
        <RankConditionPopUp></RankConditionPopUp>
      ) : null}

      <button type="button" onClick={() => props.getRankData(getParameter())}>확인</button>


    </>
  )
}


export default hot(module)(Rank);