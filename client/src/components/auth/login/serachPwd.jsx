import React, { useState } from 'react';
import { hot } from 'react-hot-loader';

import React, { useState } from 'react';
import { hot } from 'react-hot-loader';

const InputCode = ({userName, sendCode}) => {
  const [code, setCode] = useState('');

  function onChange(e){
    e.preventDefault();
    setCode(e.target.value);
  }

  function onSubmit(e){
    e.preventDefault();
    sendCode(userName, code);
  }

  return(
    <div className="code-input-container">
        <form onSubmit={onSubmit}>
          <div className="input-area">
            <input type="text" name="code" id="code" onChange={onChange} value={code} required='reauired'/>
            <label htmlFor='code'>인증코드</label>
          </div>
          <button type='submit'>제출</button>
        </form>
    </div>
  );
}


export default ({searchPwd, sendCode}) => {
  console.log('SearchPwd rendering');
  const [userName, setUserName] = useState('');
  const [email, setEmail] = useState(''); 
  const [iscodeSend, setIsCodeSend] = useState(false);

  const onChangeUserName = (e) => {
    e.preventDefault();
    setUserName(e.target.value);
  };

  const onChangeEmail = (e) => {
    e.preventDefault();
    setEmail(e.target.value);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    await searchPwd(userName, email);
    setIsCodeSend(true);
  }

  return(
    <>
      <h1>비밀번호 찾기</h1>

      <div className='login-form'>
        <form onSubmit={onSubmit}>
          <div className="input-area">
            <input id="username" name='username' type="text" onChange={onChangeUserName} value={userName} required='required'/>
            <label htmlFor='username'>아이디</label>
          </div>
          <div className="input-area">
            <input id="email" name='email' type="email" onChange={onChangeEmail} value={email} required='required'/>
            <label htmlFor='email'>이메일</label>
          </div>
          <div>
            <button type="submit">인증코드 발송</button>
          </div>
        </form>

        {iscodeSend? <InputCode userName={userName} sendCode={sendCode}/>:null}

      </div>
    </>
  )
}