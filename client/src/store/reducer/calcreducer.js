import Constants from "../constants"
import _ from "lodash";


// 유동자산
// 비유동자산
//  자산총계
// 유동부채
// 비유동부채
//  부채총계
// 지배기업
// 비지배지분
//  자본총계
const initState = {

}
// sub_account의 amount는 그대로 -> 프론트에서 amount와 coef를 곱해 바로 보여준다.
// account의 amount는 나머지를 더해서 실제 데이터를 변경

export default function reducer(state = initState, action) {

    // 선언부 위로 끌고 와도 되나?

    switch (action.type) {

        case Constants.calc.GET:

            return action.data;

        case Constants.calc.CHANGESUB: {
            let newState = _.cloneDeep(state);
            let changed_account = newState.account[action.index[0]];

            changed_account.sub_account[action.index[1]].coef = action.coef;
    
            let account_sum = 0;
            changed_account.sub_account.forEach(element => {
                account_sum += (element.amount * element.coef);
            });
            changed_account.amount = account_sum;

            newState.account[2].amount = newState.account[0].amount + newState.account[1].amount;
            newState.account[5].amount = newState.account[3].amount + newState.account[4].amount;
            newState.account[8].amount = newState.account[6].amount + newState.account[7].amount;

            return newState;
        }
        case Constants.calc.CHANGE: {
            let newState = _.cloneDeep(state);
            newState.account[action.index[0]].coef = action.coef;
            newState.account[8].amount = newState.account[6].amount + newState.account[7].amount * newState.account[7].coef;
            return newState;
        }
        default:
            return state;
    }

}