import React, { useState, useRef, useEffect } from 'react';
import { hot } from 'react-hot-loader';
import './assets/css/style.scss';

// 검색할 기업 보여주는 컴포넌트
const List = (props) => {
  console.log('list rendering');
  return (
    <li onClick={() => props.onClick(props.code)}>
      <span className="search_list_corp">{props.name}</span>
      <span className="material-icons">cancel</span>
    </li>
  )
};

const Search = (props) => {
  console.log('Search rendering');
  const [corpName, setCorpName] = useState('');

  const [corpList, setCorpList] = useState();

  useEffect(async () => {
    // await를 안으로 옮겨야 함 실제적으로 쓰이는 곳 앞에 위치해야한다.
    setCorpList(await props.getFsData());
    props.onClickInit()
  }, []);

  // 연관 검색어 리스트
  const [relList, setRelList] = useState([]);

  // 스타일
  const [listStyle, setStyle] = useState({});

  useEffect(async () => {
    await filterRelList();
  }, [corpName]);

  // 연관 검색어 필터링
  const filterRelList = async () => {
    const filterList = await corpList?.filter(item => {
      return (item.name.toLowerCase().includes(corpName.toLowerCase()))
    });

    (corpName.length > 0 && filterList.length > 0) ? (
      setRelList(filterList),
      setStyle({ display: 'block' })
    ) : (
      setRelList(),
      setStyle({ display: 'none' })
    )
  }

  // 연관 검색어 렌더링
  const renderRelList = () => {
    return (
      <ul className="search_relative-list" style={listStyle}>
        {relList?.map((item, idx) => {
          return (
            <li key={idx} onClick={e => {
              // 작동안함
              setCorpName('');
              setRelList([]);
              props.onClickCreate(
                item.code,
                item.name,
                props.maxLength
              );
            }}>
              {item.name}
              <button><span className="material-icons">add_circle_outline</span></button>
            </li>
          )
        })}
      </ul>
    )
  }

  const onChange = async (e) => {
    setCorpName(e.target.value);
  }

  let inputState = false;
  let message;
  if (props.corpList.length >= props.maxLength) {
    message = <div className='search-warn'>더 이상 추가 할 수 없습니다</div>
    inputState = true;
  } else {
    message = null
    inputState = false;
  };

  return (
    <section className="search-form">
      <input
        disabled={inputState}
        className="search-input"
        type="text"
        placeholder="기업명"
        onChange={onChange}
        // onBlur={()=>{ setStyle({display: 'none'}) }}
        // onFocus={setStyle({display: 'none'})}
        value={corpName}
      />

      {renderRelList()}
      {message}

      <ul className="search_list">
        {props.corpList.map((data, i) => (
          <List
            key={i}
            onClick={props.onClickDelete}
            name={data.name}
            code={data.code}
          >
          </List>
        ))}
      </ul>
    </section>
  )
}

export default hot(module)(Search);