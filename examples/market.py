
import pandas as pd
from tinkoff.invest import Client

from examples.utils.secrets import get_secrets


pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


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
            df = pd.DataFrame(instruments().instruments)
            df = df.set_index('ticker')

            print()
            print(instruments)
            print(df)


if __name__ == '__main__':
    market()
