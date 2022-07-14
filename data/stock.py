import akshare as ak
import pandas as pd
import pandasquant as pq
import backtrader as bt


@pq.Cache(prefix='stockmarketdaily')
def marketdaily(code: str, start: str, end: str, fromdate: str = None, todate: str = None):
    data = ak.stock_zh_a_hist(symbol=code, period='daily', start_date=start, end_date=end)
    data = data.rename(columns={'日期': 'datetime', '开盘': 'open', '收盘': 'close', '最高': 'high',
        '最低': 'low', '成交量': 'volume'}).drop(['成交额', '振幅', '涨跌幅', 
        '换手率', '涨跌额'], axis=1).set_index('datetime')
    data.index = pd.to_datetime(data.index)
    fromdate = pq.str2time(fromdate) if fromdate else data.index[0]
    todate = pq.str2time(todate) if todate else data.index[-1]
    feed = bt.feeds.PandasData(dataname=data, fromdate=fromdate, todate=todate)
    return feed


if __name__ == '__main__':
    print(marketdaily('000001.SZ', '2019-01-01', '2019-01-31'))