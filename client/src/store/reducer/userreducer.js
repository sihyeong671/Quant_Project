import Constants from "../constants";

const initState = {}

export default function reducer(state=initState, action){
  switch (action.type){
    case Constants.user.LOGIN_SUCCESS:
      return state;
  }
  return state;
};
