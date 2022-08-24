import pandas as pd
from rich import print

from .commons import tier_dict
BASIC_RATES = {
    "summer": tier_dict(0.1081, 0.1254, 0.1317),
    "winter": tier_dict(0.1052, 0.1224, 0.1287),
}

TOU_ON_RATES = {
    "summer": tier_dict(0.1416, 0.1528, 0.1592),
    "winter": tier_dict(0.1112, 0.1225, 0.1288),
}

TOU_OFF_RATES = {
    "summer": tier_dict(0.1056, 0.1169, 0.1232),
    "winter": tier_dict(0.1050, 0.1163, 0.1226),
}


def basic(input_df: pd.DataFrame):
    """Compute usage based on Basic plan"""

    total_usage = df_sum(input_df)
    print(f"Total usage: {total_usage} kWh")

    month = pd.DatetimeIndex(input_df["DATE"]).month
    summer_index = (month <= 9) & (month >= 5)
    summer_df = input_df[summer_index]
    winter_df = input_df[~summer_index]

    usage = tier_sum(summer_df, BASIC_RATES, "summer")
    usage += tier_sum(winter_df, BASIC_RATES, "winter")

    print(f"Estimate cost with Basic plan: ${usage:6.2f}")


def df_sum(i_df: pd.DataFrame):
    """Total usage in kWh"""
    return i_df["USAGE"].sum()


def tier_sum(t_df: pd.DataFrame, rates: dict, period: str):
    """Compute sum for summer/winter month using 3-level tiers"""
    _total = df_sum(t_df)

    _usage = min([_total, 500]) * rates[period]["<=500"]
    if _total >= 500:
        _usage += min([_total-500, 500]) * rates[period]["500-1000"]
    if _total >= 1000:
        _usage += (_total-1000) * rates[period][">1000"]
    return _usage


def tou(input_df: pd.DataFrame):
    """Compute usage based on Time-of-Use (TOU) plan"""

    total_usage = df_sum(input_df)
    print(f"Total usage: {total_usage} kWh")

    month = pd.DatetimeIndex(input_df["DATE"]).month
    start_hour = pd.DatetimeIndex(
        pd.to_datetime(input_df["START TIME"], format="%H:%M")
    ).hour

    summer_index = (month <= 9) & (month >= 5)
    peak_index = (start_hour >= 3) & (start_hour <= 6)

    summer_on_df = input_df[summer_index & peak_index]
    summer_off_df = input_df[summer_index & (~peak_index)]

    winter_on_df = input_df[(~summer_index) & peak_index]
    winter_off_df = input_df[(~summer_index) & (~peak_index)]

    s_on = tier_sum(summer_on_df, TOU_ON_RATES, "summer")
    s_off = tier_sum(summer_off_df, TOU_OFF_RATES, "summer")
    w_on = tier_sum(winter_on_df, TOU_ON_RATES, "winter")
    w_off = tier_sum(winter_off_df, TOU_OFF_RATES, "winter")

    print(
        f"Summer peak: {df_sum(summer_on_df):7.2f} kWh "
        f"({len(summer_on_df):3} hrs)  ${s_on:6.2f}\n"
        f"Summer off:  {df_sum(summer_off_df):7.2f} kWh "
        f"({len(summer_off_df):3} hrs)  ${s_off:6.2f}\n"
        f"Winter peak: {df_sum(winter_on_df):7.2f} kWh "
        f"({len(winter_on_df):3} hrs)  ${w_on:6.2f}\n"
        f"Winter off:  {df_sum(winter_off_df):7.2f} kWh "
        f"({len(winter_off_df):3} hrs)  ${w_off:6.2f}\n"
    )

    usage = s_on + s_off + w_on + w_off
    print(f"Estimate cost with TOU plan: ${usage:6.2f}")
