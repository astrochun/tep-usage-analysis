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
