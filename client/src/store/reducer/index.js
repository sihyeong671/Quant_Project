import { combineReducers } from "redux";
import chart from './chartreducer'
import search from './searchreducer';
import user from './userreducer';
import { persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage";

const persistConfig = {
  key: 'root',
  storage:storage,
  whitelist: ['user']
}
const rootReducer =  combineReducers({
  chart,
  search,
  user
});

export default persistReducer(persistConfig, rootReducer);