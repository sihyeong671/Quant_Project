import { combineReducers } from "redux";
import chart from './chartreducer'
import search from './searchreducer';

export default combineReducers({
  chart,
  search
});