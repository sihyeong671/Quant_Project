import { alertConstants } from "../constants";

// action 생성 함수
const success = (messeage) => {
  return { type: alertConstants.success, message}
}

const error = (messeage) => {
  return { type: alertConstants.ERROR, message}
}

const clear = (messeage) => {
  return { type: alertConstants.CLEAR, message}
}



export const alertActions = {
  success,
  error,
  clear

};