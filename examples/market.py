
import pandas as pd
from tinkoff.invest import Client
from tinkoff.invest.services import InstrumentsService

from examples.secrets.secrets import get_secrets


pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def generator(instruments):
    for item in instruments().instruments:
        yield ({
            'ticker': item.ticker,
            'figi': item.figi,
            'type': instruments.__name__,
            'name': item.name,
        })


def market():
    secrets = get_secrets()
    api_key = secrets.get_api_key('tinvest_api_key')

    with Client(api_key) as client:
        shares = client.instruments.shares
        bonds = client.instruments.bonds
        etfs = client.instruments.etfs
        currencies = client.instruments.currencies
        futures = client.instruments.futures

        for instruments in (shares, bonds, etfs, currencies, futures):
            df = pd.DataFrame(generator(instruments))
            df = df.set_index('ticker')

            print()
            print(f'Market instruments for {instruments.__name__} (count {len(df)})')
            print(df)


if __name__ == '__main__':
    market()
