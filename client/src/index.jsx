import React from 'react';
import ReactDOM from 'react-dom';

import axios from 'axios';
import { PersistGate } from 'redux-persist/integration/react';
import { BrowserRouter } from "react-router-dom";
import { Provider } from "react-redux";
import { CookiesProvider } from 'react-cookie';

import {store, persistor} from './store/store';
import App from './containers/App/App';
import './index.scss'

axios.defaults.baseURL = "http://localhost:8000";
axios.defaults.withCredentials = true;

const rootElement = document.getElementById('root');
ReactDOM.render(
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <CookiesProvider>
          <BrowserRouter>
            <App/>    
          </BrowserRouter>
        </CookiesProvider>  
      </PersistGate>
    </Provider>
    ,
    rootElement
);