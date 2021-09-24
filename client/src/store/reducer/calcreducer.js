import Constants from "../constants"

const initState ={
  account:[
    {
      fsname: '유동자산',
      subAccount: [
        {
          name: '현금및현금성자산',
          amount: 4773580.0,
          coef: 1
        },
        {
          name:'매출채권 및 기타유동채권',
          amount:7312390.0,
          coef: 1
        }
      ]
    },
    {
      fsname:'유동부채',
      subAccount:[
        {
          name: '부채1',
          amount: 477,
          coef: 1
        },
        {
          name:'부채2',
          amount:731,
          coef: 1
        }
      ]
    }
  ]
}
  

export default function reducer(state=initState, action){
  switch(action.type){
    case Constants.calc.GET:
      const newState = {
        
      }
    case Constants.calc.CHANGE:
      let newState = {...state};
      newState.account[action.index[0]].subAccount[action.index[1]].coef = action.coef;
      console.log(newState);
      return newState;


      return newState
  }

  return state
}