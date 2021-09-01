import Constants from "../constants";

const initState = {
  isAuthenticated:false,
  username:null,
  accessToken:null
}

export default function reducer(state=initState, action){
  switch (action.type){
    case Constants.user.LOGIN_SUCCESS:
      return {
        username:action.username,
        isAuthenticated:true,
        accessToken:action.accessToken
      }
    case Constants.user.LOGOUT:
      return{
        username:null,
        isAuthenticated:false,
        accessToken:null
      }
  }
  return state;
};
