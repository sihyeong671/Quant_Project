import Constants from "../constants";

const initState = {
  isAuthenticated:false,
  username:null,
  token:null
}

export default function reducer(state=initState, action){
  switch (action.type){
    case Constants.user.LOGIN_SUCCESS:
      return {
        username:action.username,
        isAuthenticated:true,
        token:action.token

      }
    case Constants.user.LOGOUT:
      return{
        username:null,
        isAuthenticated:false,
        token:null
      }
  }
  return state;
};
