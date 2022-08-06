
import pandas as pd
from tinkoff.invest import Client, InstrumentStatus, SharesResponse, InstrumentIdType
from tinkoff.invest.services import InstrumentsService, MarketDataService

from examples.secrets.secrets import get_secrets


pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def generator(instruments, method: str):
    for item in getattr(instruments, method)().instruments:
        yield ({
            'ticker': item.ticker,
            'figi': item.figi,
            'type': method,
            'name': item.name,
        })


def market():
    secrets = get_secrets()
    api_key = secrets.get_api_key('tinvest_api_key')

    with Client(api_key) as client:
        instruments: InstrumentsService = client.instruments

        for method in ('shares', 'bonds', 'etfs', 'currencies', 'futures'):
            df = pd.DataFrame(generator(instruments, method))
            df = df.set_index('ticker')

            print()
            print(f'Market instruments for {method}')
            print(df)


if __name__ == '__main__':
    market()
