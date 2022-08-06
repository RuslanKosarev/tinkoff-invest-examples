
import pandas as pd
from tinkoff.invest import Client, InstrumentIdType

from examples.secrets.secrets import get_secrets


pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def instrument():
    secrets = get_secrets()
    api_key = secrets.get_api_key('tinvest_api_key')

    with Client(api_key) as client:
        instruments = client.instruments

        r = instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id="BBG004S683W7")

        ds = pd.Series(r.instrument.__dict__)
        print(ds)


if __name__ == '__main__':
    instrument()
