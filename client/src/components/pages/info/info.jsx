import React, { useState } from 'react';

import './assets/style.scss';


const Info = () => {

  const [developerInfos, setDeveloperInfos] = useState([
    ["박시형", "bshlab671@naver.com", "https://github.com/sihyeong671", "https://blog.naver.com/bshlab671", "frontend"],
    ["조현우", "hyun0404woo@naver.com", "https://github.com/hyun98", "https://hyeo-noo.tistory.com/", "backend"],
    ["허상원", "gjehdtjr911@gmail.com", "https://github.com/POBSIZ", "https://pobsiz.tistory.com", "design"]
  ]);



  return (
    <article className="info">

      <div className='info-data'>
        <div className='data-img'></div>
        <div className='data-name'></div>
        <div className='data-sns'>
          <span className='sns-itm'>
            <i className="fab fa-github"></i>
            깃허브
          </span> <br />
          <span className='sns-itm'>
            <i class="fab fa-blog"></i>
            <i class="fab fa-bold"></i>
            <i class="fas fa-book-open"></i>
            블로그
          </span>
        </div>
      </div>

    </article>
  )
}


export default Info;