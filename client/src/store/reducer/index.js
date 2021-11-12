import { combineReducers } from "redux";
import { persistReducer } from "redux-persist";

import chart from './chartreducer'
import search from './searchreducer';
import user from './userreducer';
import board from './boardreducer';
import calc from './calcreducer'
import rank from './rankreducer';

import storage from "redux-persist/lib/storage";


// store 의 일부분을 로컬 스토리지에 저장함
// window.localstorage를 쓰면 스토어와는 별개로 저장
const persistConfig = {
  key: 'root',
  storage: storage,
  whitelist: []
}

const rootReducer =  combineReducers({
  chart,
  search,
  user,
  calc,
<<<<<<< HEAD
  rank
=======
>>>>>>> d0f6f4d7a6f16ab53ce041c625f6773066c225af
});

export default persistReducer(persistConfig, rootReducer);