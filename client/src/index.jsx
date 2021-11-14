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

axios.defaults.baseURL = "https://quant.or.kr";
axios.defaults.withCredentials = true;

import { createHashHistory } from 'history';

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