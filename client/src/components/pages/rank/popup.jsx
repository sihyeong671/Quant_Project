import React, { useState, useRef, useEffect } from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import { Helmet } from 'react-helmet';
import './assets/css/style.scss';

// case(
//   1: 상위
//   0: 하위
//   3: 이상
//   2: 이하
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
              props.fsInit?.map((item, i)=>{
                return(
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
              rlist?.map((item, j)=>{
                return(
                  <li key={j}>
                    <h3>{item}</h3>
                    <button onClick={e => popVal(j)}>❌</button>
                    <div className='input-wrapper'>
                      <div className='updown'>
                        <input type="radio" name={"up"+(j).toString()} id="up"/>
                        <label htmlFor="up"></label>
                        <input type="radio" name={"down"+(j).toString()} id="down" />
                        <label htmlFor="down"></label>
                      </div>
                    </div>
                  </li>
                )
              })
            }
          </ul>
        </div>
        <div className='endBtn'>
          <button onClick={props.closePopUp}>취소</button>
          <button onClick={e => {
              console.log(e.target);
              props.addCondition(rlist);
              props.closePopUp();
              setRlist([]);
            }}>확인</button>
        </div>
      </div>
      <div className='popUp-bg' onClick={props.closePopUp}></div>
    </div>
  )

}


const ConditionPopUp = (props) => {

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
    console.log(e);
  }

  return (
    <div className="popUp">
      <form className='popUp-inner' onSubmit={e => addCondition(e)}>
        <h2>조건추가하기</h2>
          <input className='condition-input' name='condition-input' type="text" />
          <span className="material-icons">search</span>
        <div className='condition_main'>
          <ul className='condition_main-slist'>
            {
              props.fsInit?.map((item, i)=>{
                return(
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
              rlist?.map((item, j)=>{
                console.log(item, j);
                return(
                  <li key={j}>
                    <h3>{item}</h3>
                    <button onClick={e => popVal(j)}>❌</button>
                    <div className='input-wrapper'>
                      <div className='uinput'>
                        <input type="text" className="updown" name="updown"/>
                        <input type="radio" id="up" name={"uInfo"+(j).toString()} className='up' value="up" defaultChecked="checked"/>
                        <label htmlFor="up">이상</label>
                        <input type="radio" id="down" name={"uInfo"+(j).toString()} className='down' value="down"/>
                        <label htmlFor="down">이하</label>
                      </div>
                      <div className='pinput'>
                        <input type="text" className="percent" name="percent"/>
                        <input type="radio" id="pUp" name={"pInfo"+(j).toString()} value="pUp" className='pUp' defaultChecked="chekced"/>
                        <label htmlFor="pUp">상위</label>
                        <input type="radio" id="pdown" name={"pInfo"+(j).toString()} value="pDown" className='pDown'/>
                        <label htmlFor="pdown">하위</label>
                      </div>
                    </div>
                  </li>
                )
              })
            }
          </ul>
        </div>
        <div className='endBtn'>
          <button onClick={props.closePopUp}>취소</button>
          <button type="submit" onClick={() => {
            props.addCondition(rlist);
            props.closePopUp();
            setRlist([]);
          }}>확인</button>
        </div>
        <button type="submit">네</button>
      </form>
      <div className='popUp-bg' onClick={props.closePopUp}></div>
    </div>
  )
}

export {ConditionPopUp, RankConditionPopUp};
