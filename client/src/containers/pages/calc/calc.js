import { connect } from 'react-redux';
import React from 'react';
import Calc from '../../../components/pages/calc/calc';
import Constants from '../../../store/constants';
import axios from 'axios';
import { offset } from 'highcharts';

const reArrange_ = (accountData) => {
  const showIndex = ["유동자산", "비유동자산", "자산총계", "유동부채", "비유동부채","부채총계", "지배기업", "비지배지분", "자본총계"];
  let data = []; 
  for(let idx = 0; idx < showIndex.length; idx++){
    for(let fs_idx = 0; fs_idx < accountData.length; ++fs_idx){
      if(idx === 6){
        if(accountData[fs_idx].account_name.includes(showIndex[idx])) data.push(accountData[fs_idx])
      }
      else{
        if(accountData[fs_idx].account_name === showIndex[idx]) data.push(accountData[fs_idx])
      }
      continue;
    }
  }      

  return data
}

const reArrange = (accountData) => {

  const showIndex = ["유동자산", "비유동자산", "자산총계", "유동부채", "비유동부채","부채총계", "지배기업", "비지배지분", "자본총계"];
  let data = []; 
  for(let idx = 0; idx < showIndex.length; idx++){
    for(let fs_idx = 0; fs_idx < accountData.length; ++fs_idx){
      if(idx === 6){
        if(accountData[fs_idx].fsname.includes(showIndex[idx])) data.push(accountData[fs_idx])
      }
      else{
        if(accountData[fs_idx].fsname === showIndex[idx]) data.push(accountData[fs_idx])
      }
      continue;
    }
  }      

  return data
}


const mapStateToProps=(state)=>{

  const newState = {
    calc: state.calc,
    search: state.search,
    user: state.user
  }
  return newState;
}

const mapDispatchToProps=(dispatch)=>{
  return {
    // 서버에서 재무상태표 (BS) 받아오기
    getBsData: async (parameter) => {
      try{
        const res = await axios.post('api/v1/stock/account', parameter);
        const accountData = res.data.account;
        
        const data = reArrange(accountData);

        dispatch({
          type: Constants.calc.GET,
          data: {account: data}
        })
      }catch(error){
        console.log(error);
      }
      
    },

    // 서버로 사용자가 커스텀한 숫자 전송
    sendCustom: async (parameter) => {

      try{
        const res = await axios.post('api/v1/stock/custombs', parameter);
        console.log(res);

      }catch(error){
        console.log(error);
      }

      // 유저 데이터 갱신
      try{
        const profileRes = await axios.get('api/v1/users/me');
        console.log(profileRes.data);
        const [dateJoined, email, lastLogin, userName, profile, mybstitles] = [
          profileRes.data[0].date_joined,
          profileRes.data[0].email,
          profileRes.data[0].last_login,
          profileRes.data[0].username,
          profileRes.data[0].profile,
          profileRes.data[0].mybstitles,
        ];
        console.log(dateJoined, email, lastLogin, userName, profile, mybstitles)
        dispatch({
          type:Constants.user.GETALL_SUCCESS,
          dateJoined: dateJoined,
          email: email,
          lastLogin: lastLogin,
          userName: userName,
          profile: profile,
          mybstitles: mybstitles,
      })
      }catch(error){
        console.log(error);
      }
    },

    changeSubCoef: (idx, coef) => { // idx는 리스트
        dispatch({
          type: Constants.calc.CHANGESUB,
          coef: coef,
          index: idx
        });
      },

    changeCoef: (idx, coef) => { // idx 는 number
      dispatch({
        type: Constants.calc.CHANGE,
        coef: coef,
        index: idx
      })
    },

    // 저장된 데이터 불러오기
    bsLoad: async (customTitle) => {
      const res = await axios.get('api/v1/stock/custombs', {params: {title: customTitle}});
      console.log(res.data[0].fs_account)
      const data = reArrange_(res.data[0].fs_account);
      dispatch({
        type: Constants.calc.GET,
        data: {account: data}
      })
    },

    bsDelete: async (customTitle) => {
      const res = await axios.delete('api/v1/stock/custombs',{params: {title: customTitle}});
      console.log(res);

      // 유저 데이터 갱신
      try{
        const profileRes = await axios.get('api/v1/users/me');
        console.log(profileRes.data);
        const [dateJoined, email, lastLogin, userName, profile, mybstitles] = [
          profileRes.data[0].date_joined,
          profileRes.data[0].email,
          profileRes.data[0].last_login,
          profileRes.data[0].username,
          profileRes.data[0].profile,
          profileRes.data[0].mybstitles,
        ];
        console.log(dateJoined, email, lastLogin, userName, profile, mybstitles)
        dispatch({
          type:Constants.user.GETALL_SUCCESS,
          dateJoined: dateJoined,
          email: email,
          lastLogin: lastLogin,
          userName: userName,
          profile: profile,
          mybstitles: mybstitles,
      })
      }catch(error){
        console.log(error);
      }
    }
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(Calc);