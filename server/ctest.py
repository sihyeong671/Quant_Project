import requests as rq
import json
from bs4 import BeautifulSoup

url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?"
params = {
    'crtfc_key': '7bd0686ed4f0d6ae5dd1b27866d99b9cf12c1e09', 
    'corp_code': '00107677', 
    'bsns_year': '20219', 
    'reprt_code': '11012', 
    'fs_div': 'CFS'}
# from fake_useragent import UserAgent

# ua = UserAgent(verify_ssl=False)
# user = ua.random
# print(user)
# headers = {"User-Agent": user}
# print(headers)

res = rq.get(url, params)
json_dict = json.loads(res.text)
# bs_soup = BeautifulSoup(bs_res.text, "lxml") # html.parser 도 가능

for data in json_dict['list']: # 한줄 씩 보여줌
    print(data["account_nm"])
    # print("".join(data["account_nm"].split()))
    # if "당기순이익" in "".join(data["account_nm"].split()):
    #     print(data["thstrm_amount"])
    # if data["sj_div"] == "CIS":
    #     print(data)
    #     print()
