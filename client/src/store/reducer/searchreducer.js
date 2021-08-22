import Constants from "../constants";


const initState = {
  corpList:[],
  id : 0
}


export default function reducer(state=initState, action){
  switch(action.type){
    case Constants.search.CREATE:

      return {
        ...state,
        corpList: [
          ...state.corpList,
          {
            id: action.id,
            name: action.corpName
          }
        ],
        id: action.id
      }
    
    case Constants.search.DELETE:

      const newList = state.corpList.filter(data=> data.id != action.id);
      return{
        ...state,
        corpList: newList
      }

    default:
      return state
  }
}