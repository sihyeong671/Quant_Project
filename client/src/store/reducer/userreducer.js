import Constants from "../constants";
import { userConstants } from "../constants/userconstants";

const initState = {
  isAuthenticated: false,
  username:null
}

export default function reducer(state=initState, action){
  switch (action.type){
    case Constants.user.LOGIN_SUCCESS:
      return {
        ...state,
        username:action.username,
        isAuthenticated:true
      }
    case Constants.user.LOGOUT:
      return{
        ...state,
        username:null,
        isAuthenticated:false
      }
  }
  return state;
};
