
import pandas as pd
from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.utils import quotation_to_decimal

from examples.utils.secrets import get_secrets


def quote_to_float(x) -> float:
    return float(quotation_to_decimal(x))


pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def candles():

    figi = 'BBG011MLGP84'
    print(figi)

    secrets = get_secrets()
    api_key = secrets.get_api_key('tinvest_api_key')

    interval = CandleInterval.CANDLE_INTERVAL_DAY

    end = pd.Timestamp.utcnow()
    start = end - pd.to_timedelta(30, unit='d')

    with Client(api_key) as client:
        def generator():
            for candle in client.get_all_candles(figi=figi, from_=start, to=end, interval=interval):
                yield {
                    'open': quote_to_float(candle.open),
                    'high': quote_to_float(candle.high),
                    'low': quote_to_float(candle.low),
                    'close': quote_to_float(candle.close),
                    'volume': candle.volume,
                    'time': candle.time,
                    'is_complete': candle.is_complete,
                }

        df = pd.DataFrame(generator())
        df = df.set_index('time')

    print(df)


if __name__ == '__main__':
    candles()
