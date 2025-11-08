"""
Step-by-step RFM calculation walkthrough.

This is different from src/ (which is modular/clean).
Here we keep it verbose to show the thinking process.
"""

import pandas as pd
import datetime as dt

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1200)

# 1. load & prep
df = pd.read_csv("data/flo_data_20K.csv")
df["order_num_total"] = (
    df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
)
df["customer_value_total"] = (
    df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]
)

date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)

# 2. analysis date
analysis_date = df["last_order_date"].max() + dt.timedelta(days=2)

# 3. build rfm
rfm = pd.DataFrame()
rfm["customer_id"] = df["master_id"]
rfm["recency"] = (analysis_date - df["last_order_date"]).dt.days
rfm["frequency"] = df["order_num_total"]
rfm["monetary"] = df["customer_value_total"]

# 4. scoring
rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(
    rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]
)
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])

rfm["rf_score"] = (
    rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str)
)
rfm["rfm_score"] = (
    rfm["recency_score"].astype(str)
    + rfm["frequency_score"].astype(str)
    + rfm["monetary_score"].astype(str)
)

seg_map = {
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

rfm["segment"] = rfm["rf_score"].replace(seg_map, regex=True)

print(rfm.head())
print("\nSegment summary:")
print(
    rfm.groupby("segment")[["recency", "frequency", "monetary"]]
    .agg(["mean", "count"])
    .sort_values(("monetary", "mean"), ascending=False)
)

# 5. campaign examples (just like your original)
# case A: women brand
target_segments = rfm[rfm["segment"].isin(["champions", "loyal_customers"])]["customer_id"]
new_brand_customers = df[
    (df["master_id"].isin(target_segments))
    & (df["interested_in_categories_12"].str.contains("KADIN", na=False))
]["master_id"]
new_brand_customers.to_csv("outputs/new_women_brand_customers.csv", index=False)

# case B: men/kids discount
discount_segments = rfm[
    rfm["segment"].isin(["cant_lose", "hibernating", "new_customers"])
]["customer_id"]
discount_customers = df[
    (df["master_id"].isin(discount_segments))
    & (
        df["interested_in_categories_12"].str.contains("ERKEK", na=False)
        | df["interested_in_categories_12"].str.contains("COCUK", na=False)
    )
]["master_id"]
discount_customers.to_csv("outputs/discount_campaign_customers.csv", index=False)
