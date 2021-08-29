import React, {useState, useRef} from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import HighchartsReact from 'highcharts-react-official';
import Highcharts from 'highcharts';
import axios from 'axios';


// 검색할 기업 보여주는 컴포넌트
const List = (props) => {
  console.log('list rendering')
  return(
    <li>
      {props.name}
      <button onClick={() => props.onClick(props.id)}>❌</button>
    </li>
  )
};

function Chart(props){
  console.log("Chart rendering");
  const [corpName, setCorpName] = useState('');

  const options = {
    title: {
      text: 'My chart'
    },
    series: [
      {
        data: [1, 2, 3]
      },
      {
        data: [3, 2, 1]
      }
    ]
  }

  let message;

  if ( props.search.corpList.length >= 4){
    message = <div>더 이상 추가 할 수 없습니다</div>
  }
  else{
    message = null
  }
  // else {
  //   for (let corpname in props.search.corpList){
  //     if (corpname === corpName){
  //       message = <div> 이미 존재하는 기업입니다</div>
  //     }
  //   }
  // 동작안함
  // if (corpName in props.search.corpList){
  //   message = <div>이미 존재하는 기업입니다</div>
  // }
  // }

  const onChange = (e) => {
    e.preventDefault();
    setCorpName(e.target.value);
  }

  const onClickSearch = (e) => {
    e.preventDefault();
    //api로 corpList에 담긴 기업 이름 데이터 가져오기
    props.onClickGetData(data);
  }

  return (
  <>
    {/* onChange할때 마다 렌더링 되서 컴포넌트화 해서 따로 분리하는게 좋을 것 같음 */}
    <div>
      <input type="text" placeholder="기업명" onChange={onChange} value={corpName}/>
      <a href='/chart' onClick={ e => {
        props.onClickCreate((props.search.id)+1, corpName, props.search.corpList.length, e);
        setCorpName('');
      }
        }>추가</a>
      {message}
      {/* 엔터키 누르면 바로 추가 하는 기능 추가 */}
    </div>

    <div>
      {props.search.corpList.map((data) => (
        <List 
          onClick={props.onClickDelete}
          name={data.name}
          id = {data.id}
          key={data.id}>
        </List>
        ))}
      <a href='/chart' onClick={(e) => onClickSearch(e)}>검색</a>
      {/* href 어떻게 하지? */}
      {/* 검색 누르면 api로 기업 정보 가져오기 */}
    </div>

    <HighchartsReact
      highcharts={Highcharts}
      options={options}
    />
  </>
  );
}

export default hot(module)(Chart);