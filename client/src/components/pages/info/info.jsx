import React, { useState } from 'react';

// import { faBlog, faEnvelope } from "@fortawesome/free-solid-svg-icons";
// import { faGithub } from "@fortawesome/free-brands-svg-icons";
// import { } from "@fortawesome/free-regular-svg-icons";
// import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import dataImg from './assets/img/Profile.png'
import dataImgWon from './assets/img/Won.jpg'

import logo from './assets/img/LOGO.png';

import './assets/style.scss';


const Info = () => {

  const [developerInfos, setDeveloperInfos] = useState([
    [dataImg, "박시형", "Front-End", "bshlab671@naver.com", "https://github.com/sihyeong671", "https://blog.naver.com/bshlab671"],
    [dataImg, "조현우", "Back-End", "hyun0404woo@naver.com", "https://github.com/hyun98", "https://hyeo-noo.tistory.com/"],
    [dataImgWon, "허상원", "Design", "gjehdtjr911@gmail.com", "https://github.com/POBSIZ", "https://pobsiz.tistory.com"]
  ]);



  return (
    <>
      <div className='info-title'>
        <img src={logo}/>
        <p>
          <b>Q</b>uant <br />
          <b>M</b>anagement
        </p>
        <span>DEVELOPER</span>
      </div>

      <div className="info">
        {
          developerInfos?.map((item, i) => {
            return (
              <div className='info-data' key={i}>
                <div className='data-img' style={{ backgroundImage: `url(${item[0]})` }}></div>
                <div className='data-title'>
                  <span className='title-name'>{item[1]}</span>/
                  <span className='title-work'>{item[2]}</span>
                </div>
                <div className='data-sns'>
                  <a className='sns-itm' href={`mailto:${item[3]}`} target="_blank">
                    <FontAwesomeIcon icon={faEnvelope} />
                    이메일
                  </a>
                  <a className='sns-itm' href={item[4]} target="_blank">
                    <FontAwesomeIcon icon={faGithub} />
                    깃허브
                  </a>
                  <a className='sns-itm' href={item[5]} target="_blank">
                    <FontAwesomeIcon icon={faBlog} />
                    블로그
                  </a>
                </div>
              </div>
            )
          })
        }
      </div>

    </>
  )
}


export default Info;