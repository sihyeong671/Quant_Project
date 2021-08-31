import React, {useState, useRef} from 'react';
import { Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import { useHistory } from 'react-router';

import './assets/css/style.scss'

function Header(props){

	console.log("Header rendering");
	let authHeader;

	const history = useHistory();

	const onClick = async () => {
		await props.basicLogOut(props.user.username);
		// 로그아웃 로직 구현
	}



	const getAuth = () => {
		if(!props.user.isAuthenticated)
		{
			return(
				<div className="auth-link">
					<Link to='/auth/login'>LogIn</Link>
				</div>
			)
		}else{
			// user명 출력
			return(
				<div className="auth-link">
					<button onClick={onClick}>LogOut</button>
					<Link to='/profile'>Profile</Link>
				</div>	
			)
		}
	}
	authHeader = getAuth();

	return(
		<header className="header">
			<div className="logo">
				<Link to ='/'>Quant</Link>
			</div>
			<nav className="nav">
				{authHeader}
			</nav>
		</header>
	);
}

export default hot(module)(Header);