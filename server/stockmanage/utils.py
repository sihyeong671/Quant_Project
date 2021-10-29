from time import strptime, mktime


def getData(stocks):
    close_list = []

    for stock in stocks:
        times = strptime(str(stock.date), '%Y-%m-%d')
        utc_now = mktime(times) * 1000

        close_list.append([utc_now, stock.close])

    return close_list
