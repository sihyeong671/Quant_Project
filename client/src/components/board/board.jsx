import React, {useState, useRef, useEffect} from 'react';
import { Route, Switch } from "react-router-dom";
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';

const Board =(props)=>{

    // useEffect(async ()=>{
    //     var d = ()=>{
    //         props.onClickGet()
    //     }
    //     await d()
    //     await console.log(props.board.catList);
    // });

    // const [catList, catState] = useState(props);
    return(
        <> 
            <h1>Hello World</h1>
            <button onClick={()=>props.onClickGet()}>GET</button>
            <button onClick={()=>props.onClickPost()}>POST</button>
            <button onClick={()=>props.onClickDelete()}>DELETE</button>

            <form onSubmit={()=>onClickImage()}>
                <input type="file"/>
                <button type="submit">IMAGE</button>
            </form>
            <p>{props.board.catList}</p>

        </>
    )
}

export default hot(module)(Board);