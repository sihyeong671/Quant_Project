import Constants from "../constants"

const initState ={
  "account": [
      {
          "fsname": "유동자산",
          "sub_account": [
              {
                  "name": "현금및현금성자산",
                  "amount": 4604291.0,
                  "coef": 1
              },
              {
                  "name": "매출채권 및 기타유동채권",
                  "amount": 9202795.0,
                  "coef": 1
              },
              {
                  "name": "기타유동금융자산",
                  "amount": 7524990.0,
                  "coef": 1
              },
              {
                  "name": "재고자산",
                  "amount": 10864800.0,
                  "coef": 1
              },
              {
                  "name": "기타유동자산",
                  "amount": 4022366.0,
                  "coef": 1
              }
          ]
      },
      {
          "fsname": "비유동자산",
          "sub_account": [
              {
                  "name": "장기매출채권 및 기타비유동채권",
                  "amount": 1800380.0,
                  "coef": 1
              },
              {
                  "name": "기타비유동금융자산",
                  "amount": 4586505.0,
                  "coef": 1
              },
              {
                  "name": "비유동 기타포괄손익-공정가치 측정 금융자산",
                  "amount": 2770217.0,
                  "coef": 1
              },
              {
                  "name": "비유동매도가능금융자산",
                  "amount": 0.0,
                  "coef": 1
              },
              {
                  "name": "종속기업, 조인트벤처와 관계기업에 대한 투자자산",
                  "amount": 2941828.0,
                  "coef": 1
              },
              {
                  "name": "유형자산",
                  "amount": 27170043.0,
                  "coef": 1
              },
              {
                  "name": "영업권 이외의 무형자산",
                  "amount": 9174606.0,
                  "coef": 1
              },
              {
                  "name": "기타비유동자산",
                  "amount": 159671.0,
                  "coef": 1
              }
          ]
      },
      {
          "fsname": "자산총계",
          "sub_account": []
      },
      {
          "fsname": "유동부채",
          "sub_account": [
              {
                  "name": "매입채무 및 기타유동채무",
                  "amount": 3146612.0,
                  "coef": 1
              },
              {
                  "name": "단기차입금",
                  "amount": 17185978.0,
                  "coef": 1
              },
              {
                  "name": "유동파생상품부채",
                  "amount": 188613.0,
                  "coef": 1
              },
              {
                  "name": "기타유동부채",
                  "amount": 219238.0,
                  "coef": 1
              }
          ]
      },
      {
          "fsname": "비유동부채",
          "sub_account": [
              {
                  "name": "장기매입채무 및 기타비유동채무",
                  "amount": 351974.0,
                  "coef": 1
              },
              {
                  "name": "장기차입금",
                  "amount": 21614245.0,
                  "coef": 1
              },
              {
                  "name": "비유동파생상품부채",
                  "amount": 278451.0,
                  "coef": 1
              },
              {
                  "name": "기타비유동부채",
                  "amount": 2396274.0,
                  "coef": 1
              },
              {
                  "name": "이연법인세부채",
                  "amount": 612215.0,
                  "coef": 1
              }
          ]
      },
      {
          "fsname": "부채총계",
          "sub_account": []
      },
      {
          "fsname": "지배기업의 소유주에게 귀속되는 자본",
          "sub_account": [
              {
                  "name": "자본금",
                  "amount": 1366450.0,
                  "coef": 1
              },
              {
                  "name": "자본잉여금",
                  "amount": 28073533.0,
                  "coef": 1
              },
              {
                  "name": "기타포괄손익누계액",
                  "amount": 383409.0,
                  "coef": 1
              },
              {
                  "name": "기타자본구성요소",
                  "amount": -2175125.0,
                  "coef": 1
              },
              {
                  "name": "이익잉여금(결손금)",
                  "amount": 5772230.0,
                  "coef": 1
              }
          ]
      },
      {
          "fsname": "비지배지분",
          "sub_account": []
      },
      {
          "fsname": "자본총계",
          "sub_account": []
      }
  ]
}
  

export default function reducer(state=initState, action){
  switch(action.type){
    
    case Constants.calc.GET:
      return action.data;

    case Constants.calc.CHANGE:
      let newState = {...state};
      newState.account[action.index[0]].subAccount[action.index[1]].coef = action.coef;
      console.log(newState);
      return newState;
  }

  return state
}