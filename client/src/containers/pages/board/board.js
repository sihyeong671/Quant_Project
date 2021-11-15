import React from 'react';
import {
    connect
} from 'react-redux';
import Constants from '../../../store/constants';
import axios from 'axios';
import Board from '../../../components/pages/board/board';

function mapStateToProps(state) {
    return state
}

function mapDispatchToProps(dispatch) {
    return {
        onClickGet: async () => {
            const getList = await axios.get('api/v1/board/')
            console.log(getList)
            await dispatch({
                type: Constants.board.BOARD_CREATE,
                catList: getList
            });
        },
        onClickPost: async () => {
            const getList = await axios.post('api/v1/board/manage/', {
                title: 'TEST',
                anonymous: false,
            });
            await console.log(getList);
        },
        onClickDelete: async () => {
            const getList = await axios.delete(`api/v1/board/manage/`, {
                'id': 10,
            });
            await console.log(getList);
        },
        onClickImage: async () => {
            const getList = await axios.delete(`api/v1/board/manage/`, {
                'id': 10,
            });
            await console.log(getList);
        },
    }
}



export default connect(mapStateToProps, mapDispatchToProps)(Board);