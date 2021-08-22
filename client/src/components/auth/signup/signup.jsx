import React, {useState, useRef} from 'react';
import Constants from "../../../store/constants";
import { useState } from "react";


const SignUp=(props)=>{
  console.log('Login rendering');
  const [id, setId] = useState('');
  const [pwd1, setPwd1] = useState('');
  const [pwd2, setPwd2] = useState('');
  const [email, setEmail] = useState('');

  const onChangeId = (e) => {
    e.preventDefault();
    setId(e.target.value);
  };

  const onChangePwd1 = (e) => {
    e.preventDefault();
    setPwd1(e.target.value);
  };

  const onChangePwd2 = (e) => {
    e.preventDefault();
    setPwd2(e.target.value);
  };

  const onChangeEmail = (e) => {
    e.preventDefault();
    setEmail(e.target.value);
  };

  return(
    <div className='login'>
      <h1>Sign Up</h1>
      
      <div className='login-form'>
        {/* 이게 맞나? */}
        <form onSubmit={(e) => props.basicSiginUp(e)}>
          <input name='id' type="text" placeholder="아이디" onChange={onChangeId} value={id}/>
          <input name='pwd1' type="text" placeholder="비밀번호" onChange={onChangePwd1} value={pwd1}/>
          <input name='pwd2' type="text" placeholder="비밀번호 확인" onChange={onChangePwd2} value={pwd2}/>
          <input name='email' type="text" placeholder="이메일" onChange={onChangeEmail} value={email}/>
          <button>회원가입</button>
        </form>
      </div>

      {/* <div className='social-btn'>
        <a href='#' ><img src="./assets/img/kakaologin.png" alt="" />카카오로 로그인</a>
        <a href='#' ><img src="./assets/img/googlelogin.png" alt="" />구글로 로그인</a>
      </div> */}
      
      <div className="login-other">
        아이디 찾기 | 비밀번호 찾기 | 회원가입
      </div>

    </div>
  );
}

export default SignUp;