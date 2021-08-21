import React, {useState, useRef} from 'react';
import { Route, Switch } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';

import home from '../home/home';
import calc from '../calc/calc';
import chart from '../../containers/chart/chart';
import rank from '../../containers/rank/rank';




import './assets/css/style.scss'

function Main(){
	return(
        <main className="main">
            <Switch>
                <Route exact path="/" component={home}></Route>
                <Route path="/chart" component={chart}></Route>
                <Route path="/calc" component={calc}></Route>
                <Route path="/rank" component={rank}></Route>
            </Switch>
        </main>
	);
}

export default hot(module)(Main);