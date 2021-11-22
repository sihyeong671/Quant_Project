import Constants from "../constants"

const initState = {
    BG: ''
}

export default function reducer(state = initState, action) {
    switch (action.type) {
        case Constants.main.BG_CHANGE:
            return {
                BG: action.BG
            }
    }
    return state
}