import Constants from "../constants"

const initState = {}

export default function reducer(state=initState, action){
  switch(action.type){
    case Constants.chart.GET:
      return state
  }

  return state
}