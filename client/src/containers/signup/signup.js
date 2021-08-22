import Constants from "../../store/constants"
import { connect } from "react-redux"
import SignUp from "../../components/auth/signup/signup"
import { bindActionCreators } from "redux";
import { isValidElement } from "react";
import axios from "axios";

function validEmail(email) {

	let reg = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i;

	return reg.test(email);
}

function isVaildForm(username, pwd1, pwd2, email){
  let message = null;
  if (username ===""){
    message = "아이디를 입력하세요";
    return [false, message];
  }
  else if(pwd1 !== pwd2){
    message = "비밀번호가 일치하지 않습니다";
    return [false, message];

  }
  else if(!validEmail(email)){
    message = "이메일이 형식에 맞지 않습니다";
    return [false, message];
  }
  return [true, message];
}

function mapStateToProps(state){
  return state;
}

function mapDispatchToProps(dispatch){
  return{
    basicSignUp: (e) => {
      console.log(e); 
      e.preventDefault();
      const {username ,pwd1, pwd2, email} = e.target;
      // 유효성 검사
      const [check, message] = isVaildForm(username, pwd1, pwd2, email);
      if (!check){
        window.alert(message);
        return;
      }
      axios({
        method: 'post',
        url: '/api/v1/auth/',
        data:{
          username: username,
          password1: pwd1,
          password2: pwd2,
          email: email
        }
      })
    }
  }

}


export default connect (mapStateToProps, mapDispatchToProps)(SignUp);