import React, { useState } from 'react';
import { hot } from 'react-hot-loader';

export default ({searchID}) => {
  console.log('SearchId rendering');
  const [email, setEmail] = useState('');

  const onChangeEmail = (e) => {
    e.preventDefault();
    setEmail(e.target.value);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    const id = await searchID(email);
    console.log(id);
    // 아이디 찾기 로직
  }

  return(
    <>
      <h2>아이디 찾기</h2>

      <div className='login-form'>
        <form onSubmit={onSubmit}>
          <div className="input-area">
            <input id="email" name='email' type="email" onChange={onChangeEmail} value={email} required='required'/>
            <label htmlFor='email'>E-MAIL</label>
          </div>
          <div>
            <button type="submit">다음</button>
          </div>
        </form>
      </div>
    </>
  )
}