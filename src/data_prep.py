import pandas as pd


def load_raw_data(path: str) -> pd.DataFrame:
    """
    Load raw CRM dataset from given path.
    """
    df = pd.read_csv(path)
    return df


def prepare_flo_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare FLO-like omnichannel customer data.
    - create total order count
    - create total customer value
    - convert date columns to datetime
    """
    df = df.copy()

    df["order_num_total"] = (
        df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
    )
    df["customer_value_total"] = (
        df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]
    )

    date_columns = df.columns[df.columns.str.contains("date")]
    df[date_columns] = df[date_columns].apply(pd.to_datetime)

    return df
