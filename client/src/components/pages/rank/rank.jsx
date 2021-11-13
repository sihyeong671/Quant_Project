import React, { useState, useRef, useEffect } from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';

import ConditionPopUp from '../../../containers/pages/rank/conditionpopup';
import RankConditionPopUp from '../../../containers/pages/rank/rankconditionpopup';

import './assets/css/style.scss';

function Rank(props) {

  console.log("Rank rendering")
  return(
    <>
      <div className="container">
        <div className="container-box">
          {props.condition.map((cond, idx) => {
            return(
              <div key={idx}>
                <span>{cond}</span>
                <button onClick={e => props.deleteCondition(idx)}>❌</button>
              </div>
            )
          })}
          <button onClick={props.showCondition}>조건 추가</button>
        </div>
        <div className="verticalLine">

        </div>
        <div className="container-box">
          {props.rankCondition.map((rcond, idx) => {
            let condition;
            if(rcond[1] === "1"){
              condition = <span>오름차순</span>
            }
            else if(rcond[1] === "0"){
              condition = <span>내림차순</span>
            }
            return(
              <div key={idx}>
                <span>{rcond[0]}</span>
                {condition}
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

    </>
  )
}


export default hot(module)(Rank);