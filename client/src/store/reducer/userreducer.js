import Constants from "../constants";

const initState = {
  token: null,
  username:null
}

export default function reducer(state=initState, action){
  switch (action.type){
    case Constants.user.LOGIN_SUCCESS:
      return {
        ...state,
        username:action.username,
        token:action.token
      }
    case Constants.user.LOGOUT:
      return{
        ...state,
        username:null,
        token:null
      }
  }
  return state;
};
