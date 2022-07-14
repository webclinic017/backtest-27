import pandas as pd
import backtrader as bt
import pandasquant as pq
from .data import *
from .indicators import *
from .strategies import *
from matplotlib import pyplot as plt


class BackTest:

    def __init__(self, config: dict) -> None:
        self.datafetcher = config['datafetcher']
        self.fetcherargs = config['fetcherargs']
        self.indicators = config.get('indicators', None)
        self.strategy = config.get('strategy', None)
        self.observers = config.get('observers', None)
        self.analyzers = config.get('analyzers', None)
        self.cash = config.get('cash', 1000000)
    
    def __call__(self, image_path: str = None, data_path: str = None, show: bool = True):
        cerebro = bt.Cerebro(stdstats=False)
        cerebro.broker.setcash(self.cash)
        data = self.datafetcher(**self.fetcherargs)

        if not isinstance(data, dict):
            data = {"data": data}
        for n, d in data.items():
            cerebro.adddata(d, name=n)
        
        if self.indicators is not None:
            indicators = pq.item2list(self.indicators)
            for i in indicators:
                cerebro.addindicator(i)
        
        if self.strategy is not None:
            cerebro.addstrategy(self.strategy)

        if self.observers is None:
            observers = [bt.observers.Broker, bt.observers.BuySell, bt.observers.DrawDown]
        observers = pq.item2list(observers)
        for ob in observers:
            cerebro.addobserver(ob)
        
        if self.analyzers is None:
            analyzers = [bt.analyzers.SharpeRatio, bt.analyzers.TimeDrawDown, bt.analyzers.TimeReturn, pq.OrderTable]
        analyzers = pq.item2list(analyzers)
        for an in analyzers:
            cerebro.addanalyzer(an)
        
        result = cerebro.run()

        timereturn = pd.Series(result[0].analyzers.timereturn.rets)
        pq.CONSOLE.print(dict(result[0].analyzers.sharperatio.rets))
        pq.CONSOLE.print(dict(result[0].analyzers.timedrawdown.rets))
        cerebro.plot(width=18, height=9, style='candel')
        if image_path is not None:
            plt.savefig(image_path)
        
        if show:
            plt.show()
            if not timereturn.empty:
                timereturn.printer.display(title='time return')
            if not result[0].analyzers.ordertable.rets.empty:
                result[0].analyzers.ordertable.rets.printer.display(title='order table')
        if data_path is not None:
            with pd.ExcelWriter(data_path) as writer:
                timereturn.to_excel(data_path, sheet_name='TimeReturn')
                result[0].analyzers.ordertable.rets.to_excel(data_path, sheet_name='OrderTable')
