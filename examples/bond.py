
import click
import pandas as pd
from tinkoff.invest import Client, InstrumentIdType

from examples.utils.secrets import get_secrets


pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


@click.command()
@click.option('-f', '--figi', type=str, default='BBG011MLGP84',
              help="FIGI for the instrument, 'BBG011MLGP84' is default value for ОФЗ 26240.")
def bond(figi: str):
    """
    Loads data for given FIGI, 'BBG004730N88' is default value for ОФЗ 26240.
    """
    secrets = get_secrets()
    api_key = secrets.get_api_key('tinvest_api_key')

    # to = pd.Timestamp.utcnow()
    # from_ = to - pd.to_timedelta(30000, unit='d')

    with Client(api_key) as client:
        instruments = client.instruments

        out = instruments.get_instrument_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi)
        ds = pd.Series(out.instrument.__dict__)
        print(ds)

        out = instruments.bond_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi)
        ds = pd.Series(out.instrument.__dict__)

        print(ds)
        print(f"{len(ds)} items")


if __name__ == '__main__':
    bond()
