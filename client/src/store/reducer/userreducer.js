import Constants from "../constants";

const initState = {
  isAuthenticated:false,
  accessToken:null,
  userData:{
    // dateJoined: '2021-09-11',
    // email: 'test@test.com',
    // lastLogin: '2021-11-11',
    // userName: 'TEST',
    // profile: '',
    // mybstitle: [
    //   { title: 'test', create_date: '2021-09-11' },
    // ],
  }
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
          userName: action.userName,
          profile: action.profile,
          mybstitles: action.mybstitles,
          isSuperUser: action.isSuperUser
        }
      }
  }
  return state;
};
