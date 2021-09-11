from time import strptime, mktime


def getData(stocks):
    close_list = []
    open_list = []
    low_list = []
    high_list = []
    vol_list = []

    for stock in stocks:
        times = strptime(str(stock.date), '%Y-%m-%d')
        utc_now = mktime(times) * 1000

        close_list.append([utc_now, stock.close, stock.id])
        open_list.append([utc_now, stock.open, stock.id])
        high_list.append([utc_now, stock.high, stock.id])
        low_list.append([utc_now, stock.low, stock.id])
        vol_list.append([utc_now, stock.volume, stock.id])

    data = {
        'close': close_list,
        'open': open_list,
        'high': high_list,
        'low': low_list,
        'vol': vol_list,
    }
    return data
