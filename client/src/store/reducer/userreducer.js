import Constants from "../constants";

const initState = {
  isAuthenticated:false,
  accessToken:null,
  userData:{}
}

export default function reducer(state=initState, action){
  switch (action.type){
    case Constants.user.LOGIN_SUCCESS:
    case Constants.user.REGISTER_SUCCESS:
      return {
        ...state,
        isAuthenticated:true,
        accessToken:action.accessToken
      }
    case Constants.user.LOGOUT:
      return{
        isAuthenticated:false,
        accessToken:null,
        userData: {}
      }
    case Constants.user.GETALL_SUCCESS:
      return{
        ...state,
        userData:{
          dateJoined: action.dateJoined,
          email: action.email,
          lastLogin: action.lastLogin,
          userName: action.userName
        }
      }
  }
  return state;
};
