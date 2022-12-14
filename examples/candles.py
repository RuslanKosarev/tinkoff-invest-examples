
import click
import pandas as pd
from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.utils import quotation_to_decimal

from examples.utils.secrets import get_secrets


def quote_to_float(x) -> float:
    return float(quotation_to_decimal(x))


pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


@click.command()
@click.option('-f', '--figi', type=str, default='BBG004730N88',
              help="FIGI for the instrument, 'BBG004730N88' is default value for SBER.")
def candles(figi: str):

    secrets = get_secrets()
    api_key = secrets.get_api_key('tinvest_api_key')

    interval = CandleInterval.CANDLE_INTERVAL_DAY

    end = pd.Timestamp.utcnow()
    begin = end - pd.offsets.DateOffset(years=10)

    print(f'Load history for figi={figi} in the period=({begin}, {end})')

    with Client(api_key) as client:
        def generator():
            for candle in client.get_all_candles(figi=figi, from_=begin, to=end, interval=interval):
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
        if not df.empty:
            df.set_index('time', inplace=True)

    print(df)

    # https://github.com/Tinkoff/invest-python/issues/104
    duplicated = df.index.duplicated()
    if any(duplicated):
        print('There are duplicated indexes in the history', df.index[duplicated])


if __name__ == '__main__':
    candles()
