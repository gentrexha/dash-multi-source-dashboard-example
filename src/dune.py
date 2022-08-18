from duneapi.api import DuneAPI
from duneapi.types import Network, DuneRecord, DuneQuery
import pandas as pd


def fetch_records(dune: DuneAPI) -> list[DuneRecord]:
    sample_query = DuneQuery.from_environment(
        raw_sql="select block_time::date, count(distinct trader_a) from dex.trades where project = 'CoW Protocol' and block_time::date >= '2022-03-01'::date group by block_time::date",
        name="Sample Query",
        network=Network.MAINNET,
    )
    return dune.fetch(sample_query)


def return_dataframe() -> pd.DataFrame:
    dune_connection = DuneAPI.new_from_environment()
    records = fetch_records(dune_connection)
    df = pd.DataFrame(records)
    df["block_time"] = pd.to_datetime(df["block_time"])
    return df


if __name__ == "__main__":
    return_dataframe()
