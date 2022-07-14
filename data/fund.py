import akshare as ak
import pandas as pd
import backtrader as bt
import quool as ql


@ql.Cache(prefix='etffeedsina')
def etffeedsina(code: str, fromdate: str = None, todate: str = None):
    data = ak.fund_etf_hist_sina(symbol=code)
    data = data.rename(columns={'date': 'datetime'})
    data['datetime'] = pd.to_datetime(data['datetime'])
    data = data.set_index('datetime')
    fromdate = ql.str2time(fromdate) if fromdate else data.index[0]
    todate = ql.str2time(todate) if todate else data.index[-1]
    feed = bt.feeds.PandasData(dataname=data, fromdate=fromdate, todate=todate)
    return feed


if __name__ == "__main__":
    etffeedsina('sh510300', fromdate='2019-01-01', todate='2019-01-31')
