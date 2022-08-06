
import pandas as pd
from tinkoff.invest import CandleInterval, Client
from examples.secrets.secrets import get_secrets


def price_value(x) -> float:
    return x.units + x.nano/1000000000


def candles():

    figi = 'BBG011MLGP84'
    print(figi)

    secrets = get_secrets()
    interval = CandleInterval.CANDLE_INTERVAL_DAY

    end = pd.Timestamp.utcnow()
    start = end - pd.to_timedelta(30, unit='d')

    with Client(secrets.get_api_key('tinvest_api_key')) as client:
        def generator():
            for candle in client.get_all_candles(
                    figi=figi,
                    from_=start,
                    to=end,
                    interval=interval
            ):

                if candle.is_complete:
                    yield {
                        'open': price_value(candle.open),
                        'high': price_value(candle.high),
                        'low': price_value(candle.low),
                        'close': price_value(candle.close),
                        'volume': candle.volume,
                        'time': candle.time,
                    }

    df = pd.DataFrame(generator())
    print(df)


if __name__ == '__main__':
    candles()
