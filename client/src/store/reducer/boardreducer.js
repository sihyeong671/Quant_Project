import Constants from "../constants"

const initState = {
    catList: []
}

export default function reducer(state=initState, action){
  switch(action.type){
    case Constants.board.BOARD_CREATE:
      return state
  }
  return state
}