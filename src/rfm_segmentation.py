import datetime as dt
import pandas as pd

SEGMENT_MAP = {
    r"[1-2][1-2]": "hibernating",
    r"[1-2][3-4]": "at_risk",
    r"[1-2]5": "cant_lose",
    r"3[1-2]": "about_to_sleep",
    r"33": "need_attention",
    r"[3-4][4-5]": "loyal_customers",
    r"41": "promising",
    r"51": "new_customers",
    r"[4-5][2-3]": "potential_loyalists",
    r"5[4-5]": "champions",
}


def build_rfm_table(
    df: pd.DataFrame,
    customer_id_col: str = "master_id",
    last_order_date_col: str = "last_order_date",
    total_order_col: str = "order_num_total",
    total_value_col: str = "customer_value_total",
    analysis_date: dt.datetime | None = None,
) -> pd.DataFrame:
    if analysis_date is None:
        max_date = df[last_order_date_col].max()
        analysis_date = max_date + dt.timedelta(days=1)

    rfm = pd.DataFrame()
    rfm["customer_id"] = df[customer_id_col]
    rfm["recency"] = (analysis_date - df[last_order_date_col]).dt.days
    rfm["frequency"] = df[total_order_col]
    rfm["monetary"] = df[total_value_col]

    return rfm


def score_rfm(rfm: pd.DataFrame) -> pd.DataFrame:
    rfm = rfm.copy()

    rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(
        rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]
    )
    rfm["monetary_score"] = pd.qcut(
        rfm["monetary"], 5, labels=[1, 2, 3, 4, 5]
    )

    rfm["rf_score"] = (
        rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str)
    )
    rfm["rfm_score"] = (
        rfm["recency_score"].astype(str)
        + rfm["frequency_score"].astype(str)
        + rfm["monetary_score"].astype(str)
    )

    return rfm


def assign_segments(rfm: pd.DataFrame) -> pd.DataFrame:
    rfm = rfm.copy()
    rfm["segment"] = rfm["rf_score"].replace(SEGMENT_MAP, regex=True)
    return rfm
