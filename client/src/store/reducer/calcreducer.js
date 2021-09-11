import Constants from "../constants"

const initState ={
  data:{
    money1: {
      sub1: 100
    },
    money2: {
      sub1: 200
    }
  }
}
  

export default function reducer(state=initState, action){
  switch(action.type){
    case Constants.calc.GET:
      
      return state
  }

  return state
}