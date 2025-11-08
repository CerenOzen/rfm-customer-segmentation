# RFM-Based Customer Segmentation

This repository contains a modular implementation of RFM (Recency, Frequency, Monetary) analysis on an omnichannel retail dataset.

## Project Structure
- `src/` : source code (data preparation, RFM calculation, segmentation)
- `data/` : put your dataset here (e.g. `flo_data_20K.csv`)
- `outputs/` : exported CSV files for campaigns or target customers
- `README.md` : project description
- `requirements.txt` : Python dependencies

## Features
- Combine online & offline transactions
- Calculate RFM metrics
- Score customers (1–5)
- Map scores to human-readable segments (champions, loyal customers, hibernating, etc.)

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
