import React, { useState, useRef, useEffect } from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import axios from 'axios';

import './assets/css/board.scss';

const Board = (props) => {

    const [contentList, setContentList] = useState();

    useEffect(async () => {
        const getList = await axios.get('api/v1/board/1');
        setContentList(getList.data);
        return () => { }
    }, []);

    return (
        <>
            <h1>공지</h1>
            <ul className='content-list'>
                <div className='content-itm top'>
                    <span className='itm-id'>ID</span>
                    <h3 className='itm-title'>제목</h3>
                    <p className='itm-content'>내용</p>
                    <span className='itm-creator'>작성자</span>
                </div>
                {
                    contentList?.map((item, i) => {
                        return (
                            <Link className='content-itm' to={`article/${item.id}`} key={i}>
                                <span className='itm-id'>{item.id}</span>
                                <h3 className='itm-title'>{item.title}</h3>
                                <p className='itm-content'>{item.content}</p>
                                <span className='itm-creator'>{item.creator}</span>
                            </Link>
                        )
                    })
                }
            </ul>
        </>
    )
}

export default hot(module)(Board);