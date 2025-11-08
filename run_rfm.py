from src.data_prep import load_raw_data, prepare_flo_data
from src.rfm_segmentation import build_rfm_table, score_rfm, assign_segments

DATA_PATH = "data/flo_data_20K.csv"

def main():
    df_raw = load_raw_data(DATA_PATH)
    df = prepare_flo_data(df_raw)

    rfm = build_rfm_table(df)
    rfm = score_rfm(rfm)
    rfm = assign_segments(rfm)

    print(rfm.head())
    print(rfm["segment"].value_counts())

if __name__ == "__main__":
    main()
