import argparse

import numpy as np
import pandas as pd
from rich import print
from rich.console import Console
from rich.table import Table
from . import data, commons, cost_estimate

console = Console()


def run_all_plans(
    infile: str, billing_start_dates: list[str] = None, silent: bool = False
):
    """
    Estimate cost for all TEP plans

    :param infile: Input TEP CSV file
    :param silent: Flag to run silently and only print final result
    :param billing_start_dates: Starting billing period.
           Do not specify if infile is a single billing period

    """

    df0 = data.load(infile)
    if not billing_start_dates:
        billing_start_dates = [f"{df0.iloc[0]['DATE']:%m/%d/%Y}"]

    dict_df = data.separate_billing_cycle(df0, billing_start_dates)

    df_summary = pd.DataFrame()
    for billing_period, bill_df in dict_df.items():
        basic = cost_estimate.basic(bill_df, silent=silent)
        tou = cost_estimate.tou(bill_df, silent=silent)
        peak_demand = cost_estimate.peak_demand(bill_df, silent=silent)

        d_sum = {
            "Billing Period": billing_period,
            "Basic": basic,
            "Time-of-Use": tou,
            "Peak Demand": peak_demand,
        }
        df_t = pd.DataFrame([d_sum])
        df_summary = pd.concat([df_summary, df_t], ignore_index=True)

    table = Table(show_header=True, header_style="bold magenta")
    table = commons.df_to_table(df_summary, table)

    console.print(table)

    return df_summary


def tep_cost_estimate():
    """Script to run all TEP plans"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", type=str, required=True)
    parser.add_argument("-d", "--dates", type=str, required=False, default="")
    parser.add_argument("--date-file", type=str, required=False, default="")
    parser.add_argument(
        "-s", "--silent", action="store_true", required=False, default=False
    )
    args = parser.parse_args()

    if args.dates and args.date_file:
        print("[bold red]SystemExit: Specify either --dates or --date-file!")
        raise SystemExit()

    billing_start_dates = args.dates.split(",") if args.dates else None

    if args.date_file:
        billing_start_dates = np.loadtxt(args.date_file, dtype=str).tolist()

    run_all_plans(args.infile, billing_start_dates, silent=args.silent)
