import React, { useState } from 'react';

import './assets/style.scss';


const Info = () => {

  const [developerInfos, setDeveloperInfos] = useState([
    ["박시형", "bshlab671@naver.com", "https://github.com/sihyeong671", "https://blog.naver.com/bshlab671", "frontend"],
    ["조현우","hyun0404woo@naver.com", "https://github.com/hyun98", "https://hyeo-noo.tistory.com/", "backend"],
    ["허상원", "gjehdtjr911@gmail.com", "https://github.com/POBSIZ", "https://pobsiz.tistory.com", "design" ]
  ]);



  return(
    <div className="info">

      <div className="info-head">
        <div>이름</div>
        <div>이메일</div>
        <div>깃허브</div>
        <div>블로그</div>
        <div>역할</div>
      </div>

      <div className="info-body">
        {developerInfos.map((person, idx)=>{
          console.log(person);
          return(
            <div key={idx} className="person">
              {person.map((info, _idx) => (<div key={_idx}>{info}</div>))}
            </div>
          )
        })}
      </div>


    </div>
  )
}


export default Info;