import React, { useState, useRef } from 'react';
import { Route, Switch } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';

import AuthForm from '../../containers/auth/authForm';
import Profile from '../../containers/profile/profile';
import Calc from '../../containers/pages/calc/calc';
import Chart from '../../containers/pages/chart/chart';
import Rank from '../../containers/pages/rank/rank';
import Board from '../../containers/pages/board/board';

import Home from '../pages/home/home';

import Info from '../../components/pages/info/info'

import Board from '../../containers/pages/board/board';
import Article from '../pages/board/article';


import NotFound from '../notfound';

import './assets/css/style.scss'

const Main = () => {
    console.log("main rendering")
    return (
        <main className="main">
            <Switch>
                <Route exact path="/" component={Home}></Route>

                <Route path="/auth" component={AuthForm}></Route>
                <Route path="/profile" component={Profile}></Route>

                <Route path="/chart" component={Chart}></Route>
                <Route path="/calc" component={Calc}></Route>
                <Route path="/rank" component={Rank}></Route>
                <Route path="/info" component={Info}></Route>

                <Route path="/board" component={Board}></Route>
                <Route path="/article/:id" component={Article}></Route>

                <Route component={NotFound}></Route>
            </Switch>

        </main>
    );
}

export default hot(module)(Main);