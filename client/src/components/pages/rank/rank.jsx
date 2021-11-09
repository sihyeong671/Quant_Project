import React, {useState, useRef, useEffect} from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import './assets/css/style.scss';

const rankCondiion = () => {
  //userEffect api로 정보 한번만 가져오기
  
}

const Condition = () => {
  //userEffect 정보 한번만 가져오기
}


function Rank(props){
  console.log(props);

  const [conditionPopUp, setConditionPopUp] = useState(false);
  const [rankPopUp, setRankPopUp] = useState(false);

  const showCondition = () => {
    setConditionPopUp(true);
  };

  const hideCondition = () => {
    setConditionPopUp(false);
  }

  const showRank = () => {
    setRankPopUp(true);
  }

  const hideRank = () => {
    setRankPopUp(false);
  }

  return (
    <>
      <div className = "container">
        <div className = "container-box">
          
          <button onClick={showCondition}>조건 추가</button>
        </div>
        <div className="verticalLine">

        </div>
        <div className = "container-box">
          
          <button onClick={showRank}>순위 추가</button>
        </div>
      </div>
      
      {conditionPopUp? (
          <div className = "popUp">
            조건추가하기
            <div>
              검색 창
            </div>
            <button onClick={hideCondition}>❌</button>
            <button onClick={hideCondition}>확인</button>
          </div>
      ): null}
      {rankPopUp? (
        <div className = "popUp">
          순위 추가하기
          <div>
            검색 창
          </div>
          <button onClick={hideRank}>❌</button>
          <button onClick={hideRank}>확인</button>
          {/* 확인하면 오른쪽 창에 추가 후 조건 창 생성 */}
        </div>
      ): null}
    </>
  )
} 
export default hot(module)(Rank);