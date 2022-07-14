import backtrader as bt


class KShape(bt.Indicator):
    lines = ('hammer', 'hangingman', 'piercing', )
    plotinfo = dict(subplot=True)

    def __init__(self):
        self.lines.hammer = bt.talib.CDLHAMMER(self.data.open, 
            self.data.high, self.data.low, self.data.close)
        self.lines.hangingman = bt.talib.CDLHANGINGMAN(self.data.open,
            self.data.high, self.data.low, self.data.close)
        self.lines.piercing = bt.talib.CDLPIERCING(self.data.open,
            self.data.high, self.data.low, self.data.close)
