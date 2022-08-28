# tep-usage-analysis

This Python command-line software estimates usage cost for different
[Tucson Electric Power (TEP)](https://tep.com) plans, including:

- [Basic](https://www.tep.com/basic/)
- [Time-of-use (TOU)](https://www.tep.com/time-of-use/)
- [Peak Demand](https://www.tep.com/peak-demand/)

This tool's primary intent is to be able to evaluate options and
determine if one plan is better for your pocket.

It does not account for taxes and surcharges. Rather it compares
the "Delivery" and "Power Supply" charges of using different plans, based on
actual past usage (kilo-watts-hour).

To install:
```bash
git clone https://github.com/astrochun/tep-usage-analysis
pip install -e .[dev]
```

As a TEP customer, you will need to login and download CSVs of your usage at:
https://account.tep.com/MyAccount/UsageDataDownload

For single billing cycle, you can run the analysis via:
```bash
tep_cost_estimate -i <input_file>.csv
```

For multiple billing cycles (e.g. downloading 12 billing cycles), you can
provide the starting billing period in `billing_dates.txt` and execute as:

```bash
tep_cost_estimate -i <input_multiple_billing_file>.csv --date-file billing_dates.txt
```

As an example, [`billing_dates_example.txt`](billing_dates_example.txt)
is provided.