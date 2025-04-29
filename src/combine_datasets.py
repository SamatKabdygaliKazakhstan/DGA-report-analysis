import pandas as pd
import glob
import os


INPUT_DIR = r"C:\Users\dayrb\Desktop\DGA_Project\data\original"
OUTPUT_FILE = r"C:\Users\dayrb\Desktop\DGA_Project\data\master_dataset.csv"

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
