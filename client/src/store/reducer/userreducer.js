import Constants from "../constants";
import { userConstants } from "../constants/userconstants";

const initState = {
  isAuthenticated: false,
  user:null
}

export default function reducer(state=initState, action){
  switch (action.type){
    case Constants.user.LOGIN_SUCCESS:
      return {
        ...state,
        user:action.username,
        isAuthenticated:true
      }
    case Constants.user.LOGOUT:
      return{
        ...state,
        user:null,
        inAuthenticated:false
      }
  }
  return state;
};
