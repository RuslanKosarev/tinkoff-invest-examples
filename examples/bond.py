
import click
import pandas as pd
from tinkoff.invest import Client, InstrumentIdType
from tinkoff.invest.utils import quotation_to_decimal # noqa

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

    to = pd.Timestamp.utcnow()
    from_ = to - pd.offsets.DateOffset(years=5)

    with Client(api_key) as client:
        instruments = client.instruments

        # https://tinkoff.github.io/investAPI/instruments/#getinstrumentby
        out = instruments.get_instrument_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi)
        ds = pd.Series(out.instrument.__dict__)
        print(128*'-')
        print(ds)
        print(len(ds), 'rows')

        # https://tinkoff.github.io/investAPI/instruments/#bondby
        out = instruments.bond_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi)
        ds = pd.Series(out.instrument.__dict__)
        print(128*'-')
        print(ds)
        print(len(ds), 'rows')

        # accumulated coupon income
        # https://tinkoff.github.io/investAPI/instruments/#getaccruedinterestsrequest
        aic = instruments.get_accrued_interests(from_=from_, to=to, figi=figi)
        aic = aic.accrued_interests

        def accrued_interests_generator():
            for item in aic:
                yield {
                    'date': item.date.date(),
                    'value': float(quotation_to_decimal(item.value)),
                    'percent': float(quotation_to_decimal(item.value_percent)),
                    'nominal': float(quotation_to_decimal(item.nominal)),
                }

        df = pd.DataFrame(accrued_interests_generator())
        df = df.set_index('date')
        df.sort_index(inplace=True)

        print(128*'-')
        print('accumulated coupon income')
        print(df)

        # https://tinkoff.github.io/investAPI/instruments/#getbondcoupons
        response = instruments.get_bond_coupons(figi=figi, from_=from_, to=to)
        events = response.events

        def coupon_generator():
            for event in events:
                event.pay_one_bond = float(quotation_to_decimal(event.pay_one_bond)) # noqa
                yield event

        df = pd.DataFrame(coupon_generator())

        print(128*'-')
        print('bond coupons')
        print(df)


if __name__ == '__main__':
    bond()
