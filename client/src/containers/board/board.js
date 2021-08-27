import React from 'react';
import {connect}  from 'react-redux';
import Constants from '../../store/constants';

import Board from '../../components/board/board';

function mapStateToProps(state){
    return state
}

function mapDispatchToProps(dispatch){
    const url = 'http://192.168.0.19:8000/'
    return {
        onClickGet: async ()=>{
            const getList = await fetch(`http://192.168.0.19:8000/api/v1/board/`, {
                method: 'GET',
            });
            const listJson = await getList.json();

            await dispatch({
                type:Constants.board.BOARD_CREATE,
                catList: listJson
            });

            // await console.log(listJson);
        },
        onClickPost: async ()=>{
            const getList = await fetch(`http://192.168.0.19:8000/api/v1/board/manage/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNjI5NjMyNzU4LCJleHAiOjE2Mjk2MzYzNTgsImp0aSI6IjI5MjRmYzIxLTlhNGItNGJkNS1hNjhlLTQzZTBlYWQ0Mjc1YyIsInVzZXJfaWQiOjEsInVzZXJfcHJvZmlsZV9pZCI6WzFdLCJvcmlnX2lhdCI6MTYyOTYzMjc1OH0.z6BsaVWBSTZOKkGM-SnYZ7WNWPLdPlOcPwFjQkW1wWk`
                },
                body: JSON.stringify({
                    title: 'Hello Mac Im Won',
                    anonymous: false,
                }),
            });
            const listJson = await getList.json();
            await console.log(listJson);
        },
        onClickDelete: async ()=>{
            const getList = await fetch(`http://192.168.0.19:8000/api/v1/board/manage/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNjI5NjMyNzU4LCJleHAiOjE2Mjk2MzYzNTgsImp0aSI6IjI5MjRmYzIxLTlhNGItNGJkNS1hNjhlLTQzZTBlYWQ0Mjc1YyIsInVzZXJfaWQiOjEsInVzZXJfcHJvZmlsZV9pZCI6WzFdLCJvcmlnX2lhdCI6MTYyOTYzMjc1OH0.z6BsaVWBSTZOKkGM-SnYZ7WNWPLdPlOcPwFjQkW1wWk`
                },
                body: JSON.stringify({
                    'id': 10,
                }),
            });
            const listJson = await getList.json();
            await console.log(listJson);
        },
        onClickImage: async ()=>{
            const getList = await fetch(`http://192.168.0.19:8000/api/v1/board/manage/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNjI5NjMyNzU4LCJleHAiOjE2Mjk2MzYzNTgsImp0aSI6IjI5MjRmYzIxLTlhNGItNGJkNS1hNjhlLTQzZTBlYWQ0Mjc1YyIsInVzZXJfaWQiOjEsInVzZXJfcHJvZmlsZV9pZCI6WzFdLCJvcmlnX2lhdCI6MTYyOTYzMjc1OH0.z6BsaVWBSTZOKkGM-SnYZ7WNWPLdPlOcPwFjQkW1wWk`
                },
                body: JSON.stringify({
                    'id': 10,
                }),
            });
            const listJson = await getList.json();
            await console.log(listJson);
        },
    }
}



export default connect(mapStateToProps, mapDispatchToProps)(Board);

