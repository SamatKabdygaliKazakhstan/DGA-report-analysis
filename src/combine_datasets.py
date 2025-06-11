import pandas as pd
import glob
import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Folder containing the raw CSV files shipped with the repository
INPUT_DIR = os.path.join(BASE_DIR, "original")

# Destination for the combined dataset
OUTPUT_FILE = os.path.join(BASE_DIR, "master_dataset.csv")

def main():
    csv_files = glob.glob(os.path.join(INPUT_DIR, "*.csv"))
    if not csv_files:
        print(f"❌ В папке {INPUT_DIR} нет файлов CSV!")
        return
    dfs = []
    for fp in csv_files:
        print("Загружаю:", fp)
        df = pd.read_csv(fp)
        dfs.append(df)
    master = pd.concat(dfs, ignore_index=True)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    master.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Saved master dataset to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
