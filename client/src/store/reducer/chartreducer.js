import { chart } from "highcharts"
import { chartConstants } from "../constants/chartconstants"

const initState = {}

export default function reducer(state=initState, action){
  switch(action.type){
    case chartConstants.UPDATE:
      return state
  }

  return state
}