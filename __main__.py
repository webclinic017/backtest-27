from backtest.core import BackTest
from .data import *
from .indicators import *
from .strategies import *


config = dict(
    datafetcher = marketdaily,
    cash = 1000000,
    fetcherargs = dict(
        code = '600362',
        start = '20190101',
        end = '20220701',
    ),
    indicators = None,
    strategy = None,
    observers = None,
    analyzers = None,
)

if __name__ == "__main__":
    runner = BackTest(config)
    runner()
    