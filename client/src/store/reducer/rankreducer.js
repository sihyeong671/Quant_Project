import Constants from "../constants";
import _ from 'lodash';

const initState = {
  conditionPopUp: false,
  rankConditionPopUp: false,
  fsInit:[
    "ROA",
    "ROE",
    "EBIT",
    "부채비율"
  ],
  condition:[
  ],
  rankCondition:[
  ]
}

export default function reducer(state=initState, action){

  // let newState = {...state}; // 선언부를 여기로 올리는게 맞나?

  switch(action.type){
    // 열기
    case Constants.rank.SHOWCONDITION:{
      let newState = {...state};
      newState.conditionPopUp = true;
      return newState;
    }

    case Constants.rank.SHOWRANKCONDITION:{
      let newState = {...state};
      newState.rankConditionPopUp = true
      return newState;
    }
    // 닫기
    case Constants.rank.CLOSECONDITION:{
      let newState = {...state};
      newState.conditionPopUp = false
      return newState;
    }

    case Constants.rank.CLOSERANKCONDITION:{
      let newState = {...state};
      newState.rankConditionPopUp = false
      return newState;
    }
    //추가
    case Constants.rank.ADDCONDITION:{
      let newState = _.cloneDeep(state);
      action.list.forEach(element => {
        newState.condition.push(element)
      });
      return newState;
      }
    case Constants.rank.ADDRANKCONDITION:{
      let newState = _.cloneDeep(state);
      action.list.forEach(element => {  
        newState.rankCondition.push(element)
      });
      return newState;
      }
    //삭제
    case Constants.rank.DELETECONDITION:{
      let newState = _.cloneDeep(state);
      newState.condition.splice(action.index, 1);
      return newState;
    }

    case Constants.rank.DELETERANKCONDITION:{
      let newState = _.cloneDeep(state);
      newState.rankCondition.splice(action.index, 1);
      return newState;
    }

    default:
      return state;
      

  }
}
