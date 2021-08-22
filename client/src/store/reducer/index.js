import { combineReducers } from "redux";
import chart from './chartreducer'
import search from './searchreducer';
import user from './userreducer';

export default combineReducers({
  chart,
  search,
  user
});