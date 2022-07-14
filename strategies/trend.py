import numpy as np
import backtrader as bt
import quool as ql


class SMACrossStrategy(ql.Strategy):
    def __init__(self):
        sma5 = bt.indicators.SMA(period=5)
        sma10 = bt.indicators.SMA(period=10)
        self.buycross = bt.And(sma5(-1) <= sma10(-1), sma5 > sma10)
        self.sellcross = bt.And(sma5(-1) >= sma10(-1), sma5 < sma10)
    
    def next(self):
        if self.buycross[0]:
            self.order_target_percent(target=1)

        elif self.sellcross[0]:
            self.order_target_percent(target=0)


class TurtleStrategy(ql.Strategy):
    
    def __init__(self) -> None:
        self.atr = bt.indicators.ATR(period=14)
        self.unit = 0.1
        self.currentpos = 0
        self.order = None
        self.lastbuyprice = np.inf
        self.alreadybuy = False
        high = bt.indicators.Highest(self.data.high, period=20)
        self.buysig = high(-1) <= self.data.close

    def next(self):
        if self.buysig[0] and not self.alreadybuy:
            self.order_target_percent(target=self.currentpos + self.unit)

        elif self.alreadybuy and self.data.close[0] >= self.lastbuyprice + self.atr[0]:
            self.order_target_percent(target=self.currentpos + self.unit)

    def notify_order(self, order):
        if order.status in [order.Created, order.Accepted, order.Submitted]:
            return
        elif order.status in [order.Completed]:
            self.log(f'Trade <{order.executed.size}> at <{order.executed.price}>')
            if order.isbuy():
                self.currentpos += self.unit
                self.lastbuyprice = order.executed.price
                self.alreadybuy = True
                if len(self.broker.pending) > 0:
                    # price = self.broker.pending[0].price + self.atr[0]
                    self.cancel(self.broker.pending[0])
                # else:
                price = order.executed.price - self.atr[0]
                self.sell(size=self.getposition().size, 
                    exectype=bt.Order.Stop, price=price)
            else:
                self.alreadybuy = False
                self.currentpos = 0

class BollingStrategy(ql.Strategy):
    def __init__(self):
        self.bollinger = bt.indicators.BollingerBands(period=20, devfactor=2)
    
    def next(self):
        if self.data.close[0] >= self.bollinger.bot[0] and self.data.close[-1] < self.bollinger.bot[-1]:
            self.order_target_percent(target=0.95)
        elif self.data.close[0] <= self.bollinger.top[0] and self.data.close[-1] > self.bollinger.top[-1]:
            self.order_target_percent(target=0)
