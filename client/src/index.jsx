import React from 'react';
import ReactDOM from 'react-dom';

import axios from 'axios';
import { PersistGate } from 'redux-persist/integration/react';
import { BrowserRouter, HashRouter } from "react-router-dom";
import { Provider } from "react-redux";
import { CookiesProvider } from 'react-cookie';

import {store, persistor} from './store/store';
import App from './containers/App/App';
import './index.scss'

import { createHashHistory } from 'history';

axios.defaults.baseURL = "https://quant.or.kr";
axios.defaults.withCredentials = true;

axios.interceptors.request.use(function(config){
  //요청이 전달되기 전에 작업 수행
  console.log("요청전달전")
  return config;
}, function(error){
  //요청 오류가 있는 작업 수행
  return Promise.reject(error)
});

axios.interceptors.response.use(function(response){
  console.log("응답데이터있음");
  //응답데이터가 있는 작업 수행
  return response;
}, function(error){
  // 응답오류가 있는 작업 수행
  return Promise.reject(error);
})

// create history
const history = createHashHistory({
  basname: '',
  hashType: 'slash'
})

const rootElement = document.getElementById('root');
ReactDOM.render(
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <CookiesProvider>
          <HashRouter history={history}>
            <App/>    
          </HashRouter>
        </CookiesProvider>  
      </PersistGate>
    </Provider>
    ,
    rootElement
);