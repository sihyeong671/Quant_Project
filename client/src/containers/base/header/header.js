import { connect } from "react-redux";
import Header from "../../../components/base/header/header";
import Constants from '../../../store/constants';
import axios from 'axios';
import React from 'react';

// connect는 클래스 컴포넌트를 위해 사용하는 react-redux라고 볼 수 있고
// useSelector 가 mapStateToProps와 같은 역할을 한다. 
// 그러면 컨테이너를 따로 분리할 필요가 없다고 한다.
// 다음에 써보도록 하자

function mapStateToProps(state){
  const newState = state.user;
  return newState;
}

function mapDispatchToProps(dispatch){
  return {
    basicLogOut: async function(){
      try{
        // axios.post 로 하니 문제 생김
        const res = await axios({
          method:'post',
          url:'/api/v1/auth/logout'
        })
        console.log(res);
        dispatch({
          type: Constants.user.LOGOUT
        })
      }catch(error){
        console.log(error);
      }

    }
  }
}

export default connect (mapStateToProps, mapDispatchToProps)(Header);