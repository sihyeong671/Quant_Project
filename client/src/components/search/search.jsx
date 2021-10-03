import React, { useState, useRef, useEffect } from 'react';
import { hot } from 'react-hot-loader';
import './assets/css/style.scss';

// 검색할 기업 보여주는 컴포넌트
const List = (props) => {
    console.log('list rendering')
    return (
        <li>
            {props.name}
            <button onClick={() => props.onClick(props.id)}>❌</button>
        </li>
    )
};

const Search = (props) => {
    console.log('Search rendering');
    const [corpName, setCorpName] = useState('');

    // API로 회사들 가져와야 함 
    const [getList, setGetList] = useState([
        {
            name: '네이버',
            id: 2313
        },
        {
            name: '삼성',
            id: 32456
        },
        {
            name: 'Apple',
            id: 54823
        },
        {
            name: 'Tesla',
            id: 97832
        },
    ])

    // 연관 검색어 리스트
    const [relList, setRelList] = useState([])

    const [listStyle, setStyle] = useState({});

    useEffect(async () => {
        await filterRelList()
    }, [corpName]);

    // 연관 검색어 필터링
    const filterRelList = async () => {
        const filterList = await getList.filter(item => {
            return (
                item.name.toLowerCase().includes(corpName.toLowerCase())
            )
        });
        console.log(filterList);
        (corpName.length > 0 && filterList.length > 0) ? (
            await setRelList(filterList),
            setStyle({ display: 'block' })
        ) : (
            await setRelList(),
            setStyle({ display: 'none' })
        )
    }

    // 연관 검색어 렌더
    const renderRelList = () => {
        return (
            <ul className="search_relative-list" style={listStyle}>
                {relList?.map((item, i) => {
                    return (
                        <li key={i}>
                            {item.name}
                            <button onClick={e => {
                                props.props.onClickCreate(
                                    (props.props.search.id) + 1,
                                    item.name,
                                    props.props.search.corpList.length
                                );
                                setCorpName('');
                                setRelList([]);
                            }}>추가</button>
                        </li>
                    )
                })}
            </ul>
        )
    }

    const onChange = async (e) => {
        await setCorpName(e.target.value)
    }

    let message;
    if (props.props.search.corpList.length >= 4) {
        message = <div>더 이상 추가 할 수 없습니다</div>
    }
    else {
        message = null
    }

    return (
        <section className="search-form">
            <input className="search-input" type="text" placeholder="기업명" onChange={onChange} />
            {renderRelList()}
            {message}

            <div className="search_list">
                {props.props.search.corpList.map((data) => (
                    <List
                        onClick={props.props.onClickDelete}
                        name={data.name}
                        id={data.id}
                        key={data.id}>
                    </List>
                ))}
            </div>
        </section>
    )
}

export default hot(module)(Search);