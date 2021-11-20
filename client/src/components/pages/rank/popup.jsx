import React, { useState, useRef, useEffect } from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import { Helmet } from 'react-helmet';
import './assets/css/style.scss';

// case(
//   0: 하위
//   1: 상위
//   2: 이하
//   3: 이상
// )

// rank(
//   1: 오름차순
//   0: 내림차순
// )

// case : [["ROE", 1(상위), 20(float)], ["ROA", 3, 0.5], ]
// rank: [["ROE", 1(오름차순)], ["PBR", 0(내림차순)]]
// islink : 연결(True)/일반(False) (기본: 연결, 없으면 일반) -> boolean

const RankConditionPopUp = (props) => {

  const [rlist, setRlist] = useState([]);

  const pushVal = (i) => {
    let tempList = [...rlist];
    tempList.push(i);
    setRlist(tempList);
  }

  const popVal = (idx) => {
    let tempList = [...rlist];
    tempList.splice(idx, 1);
    setRlist(tempList);
  }

  const addRankCondition = (e) => {
    e.preventDefault();

    let newList = [];
    for (let i = 0; i < rlist.length; ++i) {
      newList.push([rlist[i], Number(e.target["rInfo" + (i).toString()].value)]);
    }
    console.log(newList);
    props.addRankCondition(newList);
    props.closePopUp();
    setRlist([]);
  }

  return (
    <div className="popUp">
      <form className='popUp-inner' onSubmit={e => addRankCondition(e)}>
        <h2 style={{backgroundColor: 'rgba(254, 109, 115, 1)'}}>순위 추가하기</h2>
        {/* <input className='condition-input' name='condition-input' type="text" />
        <span className="material-icons">search</span> */}
        <div className='condition_main'>
          <ul className='condition_main-slist'>
            {
              props.fsInit?.map((item, i) => {
                return (
                  <li onClick={e => pushVal(item)} key={i}>
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
              rlist?.map((item, j) => {
                return (
                  <li key={j}>
                    <div className='input-title'>
                      <span className="material-icons" onClick={() => popVal(j)}>cancel</span>
                      <h3>{item}</h3>
                    </div>
                    <div className='input-wrapper'>
                      <div className='uinput'>
                        <div className='uninput-itm'>
                          <input type="radio" name={"rInfo" + (j).toString()} id={"up" + (j).toString()} value="1" defaultChecked="checked" />
                          <label htmlFor={"up" + (j).toString()}>오름차순</label>
                        </div>
                        <div className='uninput-itm'>
                          <input type="radio" name={"rInfo" + (j).toString()} id={"down" + (j).toString()} value="0" />
                          <label htmlFor={"down" + (j).toString()}>내림차순</label>
                        </div>
                      </div>
                    </div>
                  </li>
                )
              })
            }
          </ul>
        </div>
        <div className='endBtn'>
          <button type="button" onClick={props.closePopUp}>취소</button>
          <button type="submit">확인</button>
        </div>
      </form>
      <div className='popUp-bg' onClick={props.closePopUp}></div>
    </div>
  )
}


const ConditionPopUp = (props) => {
  console.log("rendering ConditionPopUp");
  const [rlist, setRlist] = useState([]);

  const pushVal = (i) => {
    let tempList = [...rlist];
    tempList.push(i);
    setRlist(tempList);
  }

  const popVal = (idx) => {
    let tempList = [...rlist];
    tempList.splice(idx, 1);
    setRlist(tempList);
  }

  const addCondition = (e) => {
    e.preventDefault();

    let newList = [];

    for (let i = 0; i < rlist.length; ++i) {
      let coefValue = Number(e.target["updown" + (i).toString()].value);

      let conditionValue = Number(e.target["uInfo" + (i).toString()].value);

      if ((conditionValue === 0 || conditionValue === 1) && coefValue < 0) {
        alert("하위, 상위 조건은 마이너스 값이 불가능합니다");
        return;
      }

      newList.push([rlist[i], conditionValue, coefValue])
    }
    console.log(newList);
    props.addCondition(newList);
    props.closePopUp();
    setRlist([]);
  }

  return (
    <div className="popUp">
      <form className='popUp-inner' onSubmit={e => addCondition(e)}>
        <h2 style={{backgroundColor: 'rgba(34, 124, 157, 1)'}}>조건 추가하기</h2>
        {/* <input className='condition-input' name='condition-input' type="text" />
        <span className="material-icons">search</span> */}
        <div className='condition_main'>
          <ul className='condition_main-slist'>
            {
              props.fsInit?.map((item, i) => {
                return (
                  <li onClick={() => pushVal(item)} key={i}>
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
              rlist?.map((item, j) => {
                console.log(item, j);
                return (
                  <li key={j}>
                    <div className='input-title'>
                      <span className="material-icons" onClick={() => popVal(j)}>cancel</span>
                      <h3>{item}</h3>
                    </div>
                    <div className='input-wrapper'>
                      <div className='uinput'>
                        <input type="number" step="0.1" max="100" min="-100" className="" name={"updown" + (j).toString()} required/>
                        <div className='uninput-itm'>
                          <input type="radio" id={"up" + (j).toString()} name={"uInfo" + (j).toString()} value="3" className='up' defaultChecked="checked" />
                          <label htmlFor={"up" + (j).toString()}>이상</label>
                        </div>
                        <div className='uninput-itm'>
                          <input type="radio" id={"down" + (j).toString()} name={"uInfo" + (j).toString()} value="2" className='down' />
                          <label htmlFor={"down" + (j).toString()}>이하</label>
                        </div>
                        <div className='uninput-itm'>
                          <input type="radio" id={"pUp" + (j).toString()} name={"uInfo" + (j).toString()} value="1" className='pUp' />
                          <label htmlFor={"pUp" + (j).toString()}>상위</label>
                        </div>
                        <div className='uninput-itm'>
                          <input type="radio" id={"pDown" + (j).toString()} name={"uInfo" + (j).toString()} value="0" className='pDown' />
                          <label htmlFor={"pDown" + (j).toString()}>하위</label>
                        </div>
                      </div>
                    </div>
                  </li>
                )
              })
            }
          </ul>
        </div>
        <div className='endBtn'>
          <button type="button" onClick={props.closePopUp}>취소</button>
          <button type="submit">확인</button>
        </div>
      </form>
      <div className='popUp-bg' onClick={props.closePopUp}></div>
    </div>
  )
}

export { ConditionPopUp, RankConditionPopUp };
