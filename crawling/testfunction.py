import requests as rq
import pandas as pd
from io import BytesIO
from pykrx import stock
from datetime import date

today = date.today().isoformat().replace('-', '')
# df = stock.get_market_cap_by_ticker(today)
df_p2 = stock.get_market_fundamental_by_ticker(today, market="ALL")
df = df_p2.index[3]
print(df)