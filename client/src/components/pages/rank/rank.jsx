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
      islink: props.isLink
    }
    return parameter;
  }





  console.log("Rank rendering")
  return (
    <>
      <div className="container">
        <div className="container-box">
          <button onClick={props.showCondition}>
            <span>조건 추가</span> <span className="material-icons">add_circle_outline</span>
          </button>
          {props.condition.map((cond, idx) => {
            let element;
            switch (cond[1]) { //
              case 0:
                element = <span>% 하위</span>
                break
              case 1:
                element = <span>% 상위</span>
                break
              case 2:
                element = <span> 이하</span>
                break
              case 3:
                element = <span> 이상</span>
                break
            }
            return (
              <div className='condition-itm' key={idx}>
                <span>{cond[0]}</span>
                <p>
                  <span>{cond[2]}</span>
                  {element}
                </p>
                <span className="material-icons" onClick={e => props.deleteCondition(idx)}>cancel</span>
              </div>
            )
          })}
        </div>

        <div className="verticalLine"></div>

        <div className="container-box">
          <button onClick={props.showRankCondition}>
            <span>순위 추가</span> <span className="material-icons">add_circle_outline</span>
          </button>
          {props.rankCondition.map((rcond, idx) => {
            let rankElement;
            if (rcond[1] === 1) {
              rankElement = <span>오름차순</span>
            }
            else if (rcond[1] === 0) {
              rankElement = <span>내림차순</span>
            }
            return (
              <div className='condition-itm' key={idx}>
                <span>{rcond[0]}</span>
                {rankElement}
                <span className="material-icons" onClick={e => props.deleteRankCondition(idx)}>cancel</span>
              </div>
            )
          })}
        </div>
      </div>

      {props.conditionPopUp ? (
        <ConditionPopUp></ConditionPopUp>
      ) : null}
      {props.rankConditionPopUp ? (
        <RankConditionPopUp></RankConditionPopUp>
      ) : null}

      <button className='post-condition' type="button" onClick={() => {
        props.getRankData(getParameter())
      }}>확인</button>

      <div className='result-wrapper'>
        <div className='result-inner' style={{ width: `calc((100% * (${props.tableName.length} + 2)) / 2)` }}>
        {/* <div className='result-inner'> */}

          <div className='condition-filter'>
            <div className='filter-itm start'>회사명</div>
            {props.tableName.map((name, idx) => {
              return (
                <div className='filter-itm' key={idx}>
                  {name}
                </div>
              )
            })}
            <div className='filter-itm end'>종합순위</div>
          </div>

          <div className='condition-result'>
            {props.rankData.map((data, idx) => {
              return (
                <div className='result-itm' key={idx}>
                  <div>
                    {data.company_name}
                  </div>
                  {props.tableName.map((element, idx_) => {
                    return (
                      <div key={idx_}>
                        {(data[element]).toFixed(5)}
                      </div>
                    );
                  })}
                  <div>
                    {data.rank}
                  </div>
                </div>
              )
            })}
          </div>

        </div>
      </div>

    </>
  )
}

export default hot(module)(Rank);