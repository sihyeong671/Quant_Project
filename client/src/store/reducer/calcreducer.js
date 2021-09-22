import Constants from "../constants"

const initState ={
  account:[
    {
      fsname: '유동자산',
      subAccount: [
        {
          name: '현금및현금성자산',
          amount: 4773580.0
        },
        {
          name:'매출채권 및 기타유동채권',
          amount:7312390.0
        }
      ]
    },
    {
      fsname:'유동부채',
      subAccount:[
        {
          name: '부채1',
          amount: 477
        },
        {
          name:'부채2',
          amount:731
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



      return newState
  }

  return state
}