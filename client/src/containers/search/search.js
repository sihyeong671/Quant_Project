import {
  connect
} from 'react-redux';
import React from 'react';
import Search from '../../components/search/search';
import Constants from '../../store/constants';
import axios from 'axios';

const mapStateToProps = (state) => {

  return state.search;
}

// async 는 promise를 반환
const mapDispatchToProps = (dispatch) => {
  return {
    getFsData: async () => {
      try {
        // api만들면 수정
        const res = await axios.get('api/v1/stock/company');
        // console.log(res);
        return res.data.company;
      } catch (error) {
        console.log(error);
      }
    },
    onClickCreate: function (code, name, max) {
      dispatch({
        type: Constants.search.CREATE,
        corpName: name,
        code: code,
        max: max
      })
    },
    onClickDelete: function (code) {
      dispatch({
        type: Constants.search.DELETE,
        code: code
      })
    },
    onClickInit: function () {
      dispatch({
        type: Constants.search.INIT,
      })
    }
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(Search);