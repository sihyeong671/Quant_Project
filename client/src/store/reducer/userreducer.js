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
        ...state,
        isAuthenticated:true,
        accessToken:action.accessToken
      }
    case Constants.user.LOGOUT:
      return{
        ...state,
        isAuthenticated:false,
        accessToken:null
      }
    case Constants.user.GETALL_SUCCESS:
      return{
        ...state,
        user:{
          //action으로 받은 데이터 저장
        }
      }
  }
  return state;
};
