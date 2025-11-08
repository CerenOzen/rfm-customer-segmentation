# RFM-Based Customer Segmentation

This project performs customer segmentation using the **RFM (Recency, Frequency, Monetary)** model on an omnichannel retail dataset.

---

## Project Structure

rfm-customer-segmentation/
│
├── data/ # raw CSV data (e.g., flo_data_20K.csv)
├── outputs/ # generated CSV outputs
├── src/ # modular and clean RFM code
├── notebooks/ # exploratory and step-by-step analysis
│ ├── 01_data_exploration.py
│ └── 02_rfm_walkthrough.py
├── README.md # project documentation
└── requirements.txt # dependencies

---

## Project Overview

The goal is to segment customers based on their shopping behavior using RFM metrics:

- **Recency (R):** Days since the last purchase  
- **Frequency (F):** Total number of purchases  
- **Monetary (M):** Total amount spent  

By scoring these metrics (1–5) and combining them, customers are grouped into segments like:
`Champions`, `Loyal Customers`, `At Risk`, `Hibernating`, etc.

---

## Notebooks

- `notebooks/01_data_exploration.py` → Data exploration & basic analysis  
- `notebooks/02_rfm_walkthrough.py` → Full RFM workflow and marketing use cases  

These scripts show the analytical steps before creating the final modular code in `src/`.

---

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt

2. Place the dataset under the data/ folder (e.g., flo_data_20K.csv).

3. Run the main script:
   python run_rfm.py

## Example Outputs

After running the analysis, you’ll get:
* outputs/new_women_brand_customers.csv
* outputs/discount_campaign_customers.csv
These files contain customer IDs targeted for different marketing scenarios.

## Key Insights

This project demonstrates how RFM analysis can:
* Identify the most valuable customers,
* Detect customers at risk of churn,
* Support personalized marketing campaigns.

