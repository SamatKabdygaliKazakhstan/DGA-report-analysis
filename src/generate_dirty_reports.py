import pandas as pd
import random
import os

MASTER_CSV = r"C:\Users\dayrb\Desktop\DGA_Project\data\master_dataset.csv"

DIRTY_CSV  = r"C:\Users\dayrb\Desktop\DGA_Project\data\dirty_reports.csv"

N_SAMPLES = 200

TEMPLATES = [
    "Transformer gas analysis: H2={Hydrogen}ppm, CH4={Methane}ppm, C2H2={Acetylene}ppm.",
    "H₂ level at {Hydrogen} ppm; CH₄: {Methane} ppm; C₂H₂ about {Acetylene} ppm.",
    "Gas Readings -> Hydrogen: {Hydrogen}ppm / Methane: {Methane}ppm / Acetylene: {Acetylene}ppm.",
    "Sample results: Hydrogen concentration measured at {Hydrogen} parts per million.",
    "Partial analysis - H2: {Hydrogen}, C2H2: {Acetylene} (ppm).",
    "Detection levels: H2({Hydrogen}ppm), CH4({Methane}ppm), C2H2({Acetylene}ppm).",
    "In the tested sample, hydrogen gas concentration was {Hydrogen} ppm, ethylene detected at {Ethylene} ppm.",
    "Результаты анализа масла: H2={Hydrogen} ppm, C2H4={Ethylene} ppm, C2H2={Acetylene} ppm."
]

def main():
    df = pd.read_csv(MASTER_CSV)
    cols = ["Red: Hydrogen (ppm)", "Red: Methane (ppm)", "Red: Acetylene (ppm)", "Red: Ethylene (ppm)"]
    rename = {cols[i]: v for i, v in enumerate(["Hydrogen", "Methane", "Acetylene", "Ethylene"])}
    df = df.dropna(subset=cols).rename(columns=rename)[list(rename.values())]

    reports = []
    for row in df.sample(n=N_SAMPLES, replace=True).to_dict(orient="records"):
        tpl = random.choice(TEMPLATES)
        reports.append(tpl.format(**row))

    os.makedirs(os.path.dirname(DIRTY_CSV), exist_ok=True)
    pd.DataFrame({"dirty_report": reports}).to_csv(DIRTY_CSV, index=False)
    print(f"✅ Сгенерированы грязные отчёты в {DIRTY_CSV}")

if __name__ == "__main__":
    main()
