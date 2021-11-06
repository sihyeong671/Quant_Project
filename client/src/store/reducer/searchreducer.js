import Constants from "../constants";

const initState = {
  corpList: []
};

export default function reducer(state = initState, action) {
  switch (action.type) {
    case Constants.search.CREATE: {
      let result;
      let corpArr = [];
      state.corpList?.map(item => {
        corpArr.push(item.name)
      })

      if (!corpArr.includes(action.corpName)) {
        result = {
          corpList: [
            ...state.corpList,
            {
              code: action.code,
              name: action.corpName
            }
          ]
        }
        return result;
      } else {

        alert('이미 추가된 기업입니다.')
      }


    }
    case Constants.search.DELETE: {
      const newList = state.corpList.filter(data => data.code != action.code);
      return {
        corpList: newList
      }

    }
    case Constants.search.INIT: {
      return {
        corpList: []
      }
    }
    default:
      return state
  }
}