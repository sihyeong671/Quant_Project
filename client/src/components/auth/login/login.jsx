import React, { useState } from 'react';
import { hot } from 'react-hot-loader';
import { useHistory } from 'react-router';
import { Link } from "react-router-dom";
import { Cookies, useCookies } from 'react-cookie';


// 엔터 누르면 자동으로 submit이 된다
function Login({basicLogin}){
  console.log('Login rendering');
  const [username, setUserName] = useState('');
  const [pwd, setPwd] = useState('');
  const history = useHistory();
  // const [cookies, setCookie, removeCookie] = useCookies(['token']);
  // console.log('cookie', cookies);

  const onChangeUserName = (e) => {
    e.preventDefault();
    setUserName(e.target.value);
  };

  const onChangePwd = (e) => {
    e.preventDefault();
    setPwd(e.target.value);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    const token = await basicLogin(username ,pwd);
    // setCookie('token', token);
    history.push('/');
  }

  return(
    <>
      <h1>Login</h1>

      <div className='login-form'>
        <form onSubmit={onSubmit}>
          <div className="input-area">
            <input username="username" name='username' type="text" onChange={(e) => onChangeUserName(e)} value={username} required='required'/>
            <label htmlFor='username'>USERNAME</label>
          </div>
          <div className="input-area">
            <input id="pwd" name='pwd' type="password" onChange={(e) => onChangePwd(e)} value={pwd} required='required'/>
            <label htmlFor="pwd">PASSWORD</label>
          </div>
          <div>
            <button type="submit">LOG IN</button>
          </div>
        </form>
      </div>
    </>
  );
}

export default hot(module)(Login);