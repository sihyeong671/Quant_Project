import React, { useState } from 'react';
import { hot } from 'react-hot-loader';

import React, { useState } from 'react';
import { hot } from 'react-hot-loader';

export default ({searchPwd}) => {
  console.log('SearchPwd rendering');
  const [pwd, setPwd] = useState('');
  const [email, setEmail] = useState(''); 

  const onChangeEmail = (e) => {
    e.preventDefault();
    setEmail(e.target.value);
  };

  const onChangePwd = (e) => {
    e.preventDefault();
    setPwd(e.target.value);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    await searchPwd(pwd, email);
    // 비밀번호 찾기 로직
  }

  return(
    <>
      <h2>비밀번호 찾기</h2>

      <div className='login-form'>
        <form onSubmit={onSubmit}>
          <div className="input-area">
            <input id="email" name='email' type="email" onChange={onChangeEmail} value={email} required='required'/>
            <label htmlFor='email'>E-MAIL</label>
          </div>
          <div className="input-area">
            <input id="pwd" name='pwd' type="pwd" onChange={onChangePwd} value={pwd} required='required'/>
            <label htmlFor='pwd'>PASSWORD</label>
          </div>
          <div>
            <button type="submit">다음</button>
          </div>
        </form>
      </div>
    </>
  )
}