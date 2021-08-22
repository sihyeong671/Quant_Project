import React, {useState, useRef} from 'react';
import { Route, Switch } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';

import NoneRegRoute from '../router/NoneRegRoute';
import NeedRegRoute from '../router/NeedRegRoute';

import SignUp from '../../containers/signup/signup';
import Login from '../../containers/login/login';
import Profile from '../../containers/profile/profile';

import Home from '../pages/home/home';

import Calc from '../../containers/calc/calc';
import Chart from '../../containers/chart/chart';
import Rank from '../../containers/rank/rank';


import NotFound from '../notfound';

import './assets/css/style.scss'

const Main=()=>{
	return(
        <main className="main">
            <Switch>
                <Route exact path="/" component={Home}></Route>

                <Route path="/login" component={Login}></Route>
                <Route path="/signup" component={SignUp}></Route>
                <Route path="/profile" component={Profile}></Route>

                <Route path="/chart" component={Chart}></Route>
                <Route path="/calc" component={Calc}></Route>
                <Route path="/rank" component={Rank}></Route>

                <Route component={NotFound}></Route>
            </Switch>
        </main>
	);
}

export default hot(module)(Main);