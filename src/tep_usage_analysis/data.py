from datetime import datetime
from pathlib import Path

import pandas as pd
from rich import print

DATE_PARSE = lambda x: datetime.strptime(x, "%m/%d/%Y")


def load(infile: str | Path) -> pd.DataFrame:
    """
    Load TEP CSV

    :param infile: Input file
    """

    def _to_24(input_time: pd.Series):
        return pd.to_datetime(
            input_time.values, format="%I:%M %p"
        ).strftime("%H:%M")

    if isinstance(infile, str):
        infile = Path(infile)

    print(f"[yellow]Loading: {infile.name}")
    with open(infile, "r") as f:
        header = f.readline()

    if header.startswith("ADDRESS"):
        df = pd.read_csv(
            infile, parse_dates=["DATE"], date_parser=DATE_PARSE, skiprows=2
        )
    else:
        df = pd.read_csv(infile, parse_dates=["DATE"], date_parser=DATE_PARSE)

    df.drop(columns="TYPE", inplace=True)

    df["START TIME"] = _to_24(df["START TIME"])
    df["END TIME"] = _to_24(df["END TIME"])
    return df


def separate_billing_cycle(
    input_df: pd.DataFrame, billing_start_date: list[str]
) -> dict[str, pd.DataFrame]:
    """
    Separate out multiple billing cycles

    :param input_df: DataFrame spanning multiple billing cycles
    :param billing_start_date: The start date for each billing cycle
    """

    billing_start_datetime = [
        datetime.strptime(d, "%m/%d/%Y") for d in billing_start_date
    ]

    dict_df = {}
    for i, bill_date in enumerate(billing_start_datetime):
        if i == len(billing_start_datetime)-1:
            bill_end_date = input_df["DATE"].max()
        else:
            bill_end_date = billing_start_datetime[i+1]
        bill_df = input_df[
            (input_df["DATE"] >= bill_date) &
            (input_df["DATE"] < bill_end_date)
        ]
        if not bill_df.empty:
            dict_df[billing_start_date[i]] = bill_df

    return dict_df
