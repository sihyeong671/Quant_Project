import Constants from "../constants"

const initState = {
  one:100,
  two:200,
  three:300
}

export default function reducer(state=initState, action){
  switch(action.type){
    case Constants.calc.GET:
      
      return state
  }

  return state
}