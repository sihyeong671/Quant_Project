import Constants from "../constants";

const initState = {
  corpList:[],
  id : 0
}

export default function reducer(state=initState, action){
  switch(action.type){

    case Constants.search.CREATE:
      var result
      
      var corpArr = []
      state.corpList?.map(item=>{
        corpArr.push(item.name)
      })

      !corpArr.includes(action.corpName) ? 
        (
          result = {
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
          
        ) : (alert('이미 추가된 기업입니다.'), result = state)
      return result 
    

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