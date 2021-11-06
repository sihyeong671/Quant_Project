import Constants from "../constants"
import _ from "lodash";
const initState = {

}

export default function reducer(state=initState, action){
  switch(action.type){
    case Constants.chart.GET:
      let newState = _.cloneDeep();
      
      return state
  }

  return state
}