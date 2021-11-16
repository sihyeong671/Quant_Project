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
    "account": [{
            "fsname": "유동자산",
            "amount": 36268771.0,
            "coef": 1,
            "sub_account": [{
                    "name": "현금및현금성자산",
                    "amount": 5925140.0,
                    "coef": 1
                },
                {
                    "name": "매출채권 및 기타유동채권",
                    "amount": 8163169.0,
                    "coef": 1
                },
                {
                    "name": "재고자산",
                    "amount": 10800282.0,
                    "coef": 1
                },
                {
                    "name": "기타유동금융자산",
                    "amount": 6443917.0,
                    "coef": 1
                },
                {
                    "name": "기타유동자산",
                    "amount": 4936263.0,
                    "coef": 1
                }
            ]
        },
        {
            "fsname": "비유동자산",
            "amount": 50798431.0,
            "coef": 1,
            "sub_account": [{
                    "name": "장기매출채권 및 기타비유동채권",
                    "amount": 1911233.0,
                    "coef": 1
                },
                {
                    "name": "유형자산",
                    "amount": 29490596.0,
                    "coef": 1
                },
                {
                    "name": "영업권 이외의 무형자산",
                    "amount": 9051848.0,
                    "coef": 1
                },
                {
                    "name": "종속기업, 조인트벤처와 관계기업에 대한 투자자산",
                    "amount": 0.0,
                    "coef": 1
                },
                {
                    "name": "기타비유동금융자산",
                    "amount": 6399794.0,
                    "coef": 1
                },
                {
                    "name": "비유동매도가능금융자산",
                    "amount": 3702560.0,
                    "coef": 1
                },
                {
                    "name": "기타비유동자산",
                    "amount": 242400.0,
                    "coef": 1
                }
            ]
        },
        {
            "fsname": "자산총계",
            "amount": 87067202.0,
            "coef": 1,
            "sub_account": []
        },
        {
            "fsname": "유동부채",
            "amount": 18648083.0,
            "coef": 1,
            "sub_account": [{
                    "name": "매입채무 및 기타유동채무",
                    "amount": 2663206.0,
                    "coef": 1
                },
                {
                    "name": "단기차입금",
                    "amount": 12140595.0,
                    "coef": 1
                },
                {
                    "name": "기타유동금융부채",
                    "amount": 3611689.0,
                    "coef": 1
                },
                {
                    "name": "기타유동부채",
                    "amount": 232593.0,
                    "coef": 1
                }
            ]
        },
        {
            "fsname": "비유동부채",
            "amount": 19842071.0,
            "coef": 1,
            "sub_account": [{
                    "name": "장기차입금",
                    "amount": 17365164.0,
                    "coef": 1
                },
                {
                    "name": "기타비유동금융부채",
                    "amount": 212884.0,
                    "coef": 1
                },
                {
                    "name": "이연법인세부채",
                    "amount": 436492.0,
                    "coef": 1
                },
                {
                    "name": "기타비유동부채",
                    "amount": 1827531.0,
                    "coef": 1
                }
            ]
        },
        {
            "fsname": "부채총계",
            "amount": 38490154.0,
            "coef": 1,
            "sub_account": []
        },
        {
            "fsname": "지배기업의 소유주에게 귀속되는 자본",
            "amount": 40370561.0,
            "coef": 1,
            "sub_account": [{
                    "name": "자본금",
                    "amount": 1366450.0,
                    "coef": 1
                },
                {
                    "name": "자본잉여금",
                    "amount": 34575747.0,
                    "coef": 1
                },
                {
                    "name": "기타자본구성요소",
                    "amount": -2335863.0,
                    "coef": 1
                },
                {
                    "name": "기타포괄손익누계액",
                    "amount": -1621787.0,
                    "coef": 1
                },
                {
                    "name": "이익잉여금(결손금)",
                    "amount": 8386014.0,
                    "coef": 1
                }
            ]
        },
        {
            "fsname": "비지배지분",
            "amount": 8206487.0,
            "coef": 1,
            "sub_account": []
        },
        {
            "fsname": "자본총계",
            "amount": 48577048.0,
            "coef": 1,
            "sub_account": []
        }
    ]
}
// sub_account의 amount는 그대로 -> 프론트에서 amount와 coef를 곱해 바로 보여준다.
// account의 amount는 나머지를 더해서 실제 데이터를 변경

export default function reducer(state = initState, action) {

    // 선언부 위로 끌고 오기



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

    }

    return state
}