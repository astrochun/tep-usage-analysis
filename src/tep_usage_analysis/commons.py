import pandas as pd
from rich.table import Table


def df_to_table(
    df0: pd.DataFrame,
    rich_table: Table,
    show_index: bool = False,
    index_name: str = None,
) -> Table:
    """
    Convert a pandas.DataFrame obj into a rich.Table obj.

    :param df0: Dataframe to convert to rich table
    :param rich_table: Rich Table populated with DataFrame values.
    :param show_index: Include a row count to table. Defaults to False.
    :param index_name: The column name to give to the index column. Defaults to None, showing no value.
    """

    if show_index:
        index_name = str(index_name) if index_name else ""
        rich_table.add_column(index_name)

    for column in df0.columns:
        rich_table.add_column(str(column))

    for index, value_list in enumerate(df0.values.tolist()):
        row = [str(index)] if show_index else []
        row += [str(x) for x in value_list]
        rich_table.add_row(*row)

    return rich_table


def tier_dict(low: float, med: float, high: float) -> dict[str, float]:
    return {
        "<=500": low,
        "500-1000": med,
        ">1000": high,
    }
