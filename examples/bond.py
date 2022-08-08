
import click
import pandas as pd
from tinkoff.invest import Client, InstrumentIdType

from examples.utils.secrets import get_secrets


pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def price_value(x) -> float:
    return x.units + x.nano/1000000000


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
        print(128*'-')
        print(ds)
        print(len(ds), 'rows')

        out = instruments.bond_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi)
        ds = pd.Series(out.instrument.__dict__)
        print(128*'-')
        print(ds)
        print(len(ds), 'rows')

        # accrued interests value
        to = pd.Timestamp.utcnow()
        from_ = to - pd.offsets.DateOffset(years=10)

        aic = instruments.get_accrued_interests(from_=from_, to=to, figi=figi)
        aic = aic.accrued_interests

        def accrued_interests_generator():
            for item in aic:
                yield {
                    'date': item.date.date(),
                    'value': price_value(item.value),
                    'percent': price_value(item.value_percent),
                    'nominal': price_value(item.nominal)
                }

        df = pd.DataFrame(accrued_interests_generator())
        df = df.set_index('date')
        df.sort_index(inplace=True)

        print(128*'-')
        print(df)


if __name__ == '__main__':
    bond()
