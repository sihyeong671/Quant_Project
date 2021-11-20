import React, { useState, useRef, useEffect } from 'react';
import { Route, Switch, Link } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import axios from 'axios';

import './assets/css/article.scss';

const Article = (props) => {

    const [contentList, setContentList] = useState();

    useEffect(async () => {
        const getList = await axios.get(`api/v1/board/${1}/post/${props.match.params.id}`);
        console.log(getList);
        setContentList(getList.data);
        return () => { }
    }, []);

    return (
        <>
            <h1>Article</h1>
        </>
    )
}

export default hot(module)(Article);