import React from 'react';
import ReactDOM from 'react-dom';

import { BrowserRouter } from "react-router-dom";
import { Provider } from "react-redux"; 

import store from './store/store';
import App from './App/App';
import './index.scss'

const rootElement = document.getElementById('root');
ReactDOM.render(
    <Provider store = {store}>
      <BrowserRouter>
        <App/>    
      </BrowserRouter>
    </Provider>
    ,
    rootElement
);