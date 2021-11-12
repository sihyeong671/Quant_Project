import React, { useState, useRef } from 'react';
import { Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import { useHistory } from 'react-router';

import './assets/css/style.scss'
import logo from './assets/img/LOGO.png'

function Header(props) {
	console.log("Header rendering");

	const onClick = async () => {
		await props.basicLogOut(props.user.username);
		// 로그아웃 로직 구현
		navClose()
	};

	const [navTabStyle, setNavTabStyle] = useState();
	const [navBgStyle, setNavBgStyle] = useState();
	const [navStyle, setNavStyle] = useState();
	const navOpen = () => {
		setNavTabStyle({
			right: '0',
			left: '0',
			opacity: '100%',
		})
		setTimeout(() => {
			setNavStyle({
				right: '0',
				left: 'auto',
				opacity: '100%',
			});
			setNavBgStyle({
				left: '0',
				opacity: '100%',
			});
		}, 300);
	};
	
	const navClose = () => {
		setNavStyle({
			right: '-30%',
			left: 'auto',
			opacity: '0',
		});
		setNavBgStyle({
			left: '-70%',
			opacity: '100%',
		});
		setTimeout(() => {
			setNavTabStyle({
				left: '-100%',
				opacity: '0',
			})
		}, 300);
	}

	return (
		<header className="header">
			<div className="logo">
				<Link to='/'>Quant</Link>
			</div>
			<nav className="nav">
				<button className='nav-menuBar material-icons' onClick={navOpen}>menu</button>

				<div className='navTab' style={navTabStyle}>
					<div className='navTab-container' style={navStyle}>
						<div className='navTab-user'>
							{
								!props.user.isAuthenticated ? (
									<>
										<Link to='/auth/login' className='user-login' onClick={navClose}>로그인</Link>
										<p className='user-more'>회원가입을 하실려면 <Link to='/auth/signup'>여기</Link>를 클릭해주세요</p>
									</>
								) : (
									<>
										<div className='user-profile'>
											<div className='profile_left'>
												<Link 
													to='/profile' 
													className='profile-img' 
													style={{ backgroundImage: `url(${logo})` }}
													onClick={navClose}
												></Link>
												<span><strong>USER</strong> 님</span>
											</div>
											<Link onClick={onClick} className='user-logout'>로그아웃</Link>
										</div>
									</>
								)
							}
						</div>
						<ul className='navTab-link'>
							<Link to="/chart" onClick={navClose}>📈차트</Link>
							<Link to="/calc" onClick={navClose}>🧮연산</Link>
							<Link to="/rank" onClick={navClose}>🥇순위</Link>
							<Link to="/" onClick={navClose}>📄공지</Link>
							<Link to="/" onClick={navClose}>📫문의</Link>
						</ul>
					</div>
					<div className='navTab-bg' onClick={navClose} style={navBgStyle}></div>
				</div>

			</nav>
		</header>
	);
}

export default hot(module)(Header);