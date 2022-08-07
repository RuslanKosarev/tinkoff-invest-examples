
import click
import pandas as pd
from tinkoff.invest import Client, InstrumentIdType

from examples.utils.secrets import get_secrets


pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


@click.command()
@click.option('-i', '--id_type', type=str, default='share',
              help="ID type of the instrument, i.e. shares, bonds, etfs, currencies, or futures, "
                   "default value is 'share'.")
@click.option('-f', '--figi', type=str, default='BBG004730N88',
              help="FIGI for the instrument, 'BBG004730N88' is default value for SBER.")
def instrument(id_type: str, figi: str):
    """
    Loads data for given FIGI, 'BBG004730N88' is default value for SBER.
    """
    secrets = get_secrets()
    api_key = secrets.get_api_key('tinvest_api_key')

    with Client(api_key) as client:
        instruments = client.instruments

        id_request = f'{id_type}_by'
        request = getattr(instruments, id_request)
        out = request(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi)

        ds = pd.Series(out.instrument.__dict__)

        print(ds)
        print(f"request '{id_request}', {len(ds)} items")


if __name__ == '__main__':
    instrument()
