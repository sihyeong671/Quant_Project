import Constants from "../constants";

const initState = {
  isAuthenticated:false,
  accessToken:null,
  user:{}
}

export default function reducer(state=initState, action){
  switch (action.type){
    case Constants.user.LOGIN_SUCCESS:
    case Constants.user.REGISTER_SUCCESS:
      return {
        isAuthenticated:true,
        accessToken:action.accessToken
      }
    case Constants.user.LOGOUT:
      return{
        isAuthenticated:false,
        accessToken:null
      }
    case Constants.user.GETALL_SUCCESS:
      return{
        
      }
  }
  return state;
};
