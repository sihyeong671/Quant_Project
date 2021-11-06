import Constants from "../constants"
import _ from "lodash";
const initState = {
}

export default function reducer(state=initState, action){
  switch(action.type){
    case Constants.chart.GET:
      const newState = action.data;
      console.log(data);
      return newState
  }

  return state
}