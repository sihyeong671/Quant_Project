import React, {useState, useRef} from 'react';
import { Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';

import './assets/css/style.scss'


function Header(){
	return(
		<header className="header">
			<div className="logo">
				Quant
			</div>
			<nav className="nav">
				<Link to="/">Home</Link>
			</nav>
		</header>
	);
}

export default hot(module)(Header);