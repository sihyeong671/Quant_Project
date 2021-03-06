import React, { useState } from 'react';
import { hot } from 'react-hot-loader';

export default ({searchId}) => {
  console.log('SearchId rendering');
  const [email, setEmail] = useState('');
  const [findName, setFindName] = useState(false);
  const [userName, setUserName] = useState('');
  const onChangeEmail = (e) => {
    e.preventDefault();
    setEmail(e.target.value);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    const resName = await searchId(email);
    console.log(resName);
    setUserName(resName);
    setFindName(true);
    // 아이디 찾기 로직
  }


  let showForm;

  if (!findName){
    showForm = 
    <>
      <div className="input-area">
        <input id="email" name='email' type="email" onChange={onChangeEmail} value={email} required='required'/>
        <label htmlFor='email'>이메일</label>
      </div>
      <div>
        <button type="submit">찾기</button>
      </div>
      </>;
  }
  else{
    // 에러인 경우 아이디가 없습니다
    showForm = 
    <>
      <h3>아이디를 찾았습니다</h3>
      <div className="show-name-container">
        <div className='show-name'>
          {userName}
        </div>
      </div>
    </>;
  }

  return(
    <>
      <h1>아이디 찾기</h1>

      <div className='login-form'>
        <form onSubmit={onSubmit}>
          {showForm}
        </form>
      </div>
    </>
  )
}