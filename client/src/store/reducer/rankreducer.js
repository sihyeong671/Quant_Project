import Constants from "../constants";


const initState = {
  // 재무지표
  fsIndicator: [
    "ROE",
    "ROA",
    "PER",
    "PBR",
    "부채비율",
    "시가총액"
  ]
  // 
};

export default function reducer(state=initState, action){
  switch(action.type){
    case Constants.rank.GET:
      return state;
  }
};