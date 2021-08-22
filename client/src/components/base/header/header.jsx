import React, {useState, useRef} from 'react';
import { Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';

import './assets/css/style.scss'

// {} <- 파라미터에 이거 까먹지 말기
function Header({isAuthenticated, username, handleLogout}){
	// console.log(handleLogout);
	// handleLogout()
	const genAuth=()=>{
		console.log(isAuthenticated);
		if(isAuthenticated == false){
			return(
				<div className="auth-link" key={1}>
					{/* {console.log(isAuthenticated)} */}
					<Link to='/login'>Login</Link>
					<Link to='/signup'>Sign Up</Link>
				</div>
			)
		}else{
			return(
				<div className="auth-link" key={0}>
					<button onClick={handleLogout}>Logout</button> 
					<Link to='/profile'>Profile</Link>
				</div>	
			)
		}
	}

	return(
		<header className="header">
			<div className="logo">
				Quant
			</div>
			<nav className="nav">
				<Link to="/">Home</Link>
				<Link to='/login'>Log In</Link>
				<Link to='/signup'>Sign Up</Link>
				<Link to='/profile'>Profile</Link>
			</nav>
		</header>
	);
}

export default hot(module)(Header);