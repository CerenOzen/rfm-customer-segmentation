"""
Basic data exploration for FLO-like CRM dataset.
This file is for demonstrating that we actually explored and understood the data.
"""

import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1200)
pd.set_option("display.float_format", lambda x: f"{x:.2f}")

# 1. read data
df = pd.read_csv("data/flo_data_20K.csv")
raw_df = df.copy()

# 2. first look
print("Head:")
print(df.head(10))
print("\nShape:", df.shape)
print("\nColumns:", df.columns.tolist())

print("\nDescribe:")
print(df.describe().T)

print("\nMissing values:")
print(df.isnull().sum())

print("\nInfo:")
print(df.info())

# 3. total order & total value
df["order_num_total"] = (
    df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
)
df["customer_value_total"] = (
    df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]
)

# 4. convert date columns
date_cols = df.columns[df.columns.str.contains("date")]
df[date_cols] = df[date_cols].apply(pd.to_datetime)

print("\nOrder channel breakdown:")
order_channel_summary = (
    df.groupby("order_channel")
    .agg(
        customer_count=("master_id", "count"),
        total_orders=("order_num_total", "sum"),
        total_revenue=("customer_value_total", "sum"),
    )
    .sort_values("total_revenue", ascending=False)
)
print(order_channel_summary)

# 5. top customers by revenue
print("\nTop 10 customers by revenue:")
print(df.sort_values("customer_value_total", ascending=False).head(10)[
    ["master_id", "customer_value_total", "order_num_total"]
])

# 6. top customers by order count
print("\nTop 10 customers by order count:")
print(df.sort_values("order_num_total", ascending=False).head(10)[
    ["master_id", "order_num_total", "customer_value_total"]
])
