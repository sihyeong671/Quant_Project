import React, {useState, useRef} from 'react';
import Constants from "../../../store/constants";
import { useState } from "react";


const SignUp = (props) => {
  console.log('SignUp rendering');
  const [id, setId] = useState('');
  const [pwd1, setPwd1] = useState('');
  const [pwd2, setPwd2] = useState('');
  const [email, setEmail] = useState('');
  // usecallback쓰면 최적화 되나?

  const onChangeId = (e) => {
    setId(e.target.value);
  };

  const onChangePwd1 = (e) => {
    setPwd1(e.target.value);
  };

  const onChangePwd2 = (e) => {
    setPwd2(e.target.value);
    }

  const onChangeEmail = (e) => {
    setEmail(e.target.value);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    const [username ,pwd1, pwd2, email] = [
      e.target.username.value,
      e.target.pwd1.value,
      e.target.pwd2.value,
      e.target.email.value,
    ];
    props.basicSignUp(username, pwd1, pwd2, email);
    
  }

  return(
    <div className='login'>
      <h1>Sign Up</h1>
      
      <div className='login-form'>
        <form onSubmit={onSubmit}>
          <div className="input-area">
            <input id="username" name='username' type="text" onChange={onChangeId} value={id} required='required'/>
            <label htmlFor="username">USERNAME</label>
          </div>
          <div className="input-area">
            <input id='pwd1' name='pwd1' type="password" onChange={onChangePwd1} value={pwd1} required='required'/>
            <label htmlFor="pwd1">PASSWORD1</label>
          </div>
          <div className="input-area">
            <input id='pwd2' name='pwd2' type="password" onChange={onChangePwd2} value={pwd2} required='required'/>
            <label htmlFor="pwd2">PASSWORD2</label>
          </div>
          <div className="input-area">
            <input id='email' name='email' type="email" onChange={onChangeEmail} value={email} required='required'/>
            <label htmlFor="email">EMAIL</label>
          </div>
          <div>
            <button type="submit">Sign UP</button>
          </div>
        </form>

      </div>

    </div>
  );
}

export default SignUp;