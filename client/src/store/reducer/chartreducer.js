import Constants from "../constants"
import _ from "lodash";
const initState = {
  price:{},
  per:{},
  pbr:{}
}

export default function reducer(state=initState, action){
  switch(action.type){
    case Constants.chart.GET:
      const newState = {
        price: action.price,
      }
      return newState;
    default:
      return state;
  }

}