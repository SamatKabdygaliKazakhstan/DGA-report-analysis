import pandas as pd
import re
import os
import spacy
from spacy.pipeline import EntityRuler


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Location of the generated textual reports
DIRTY_CSV = os.path.join(BASE_DIR, "dirty_reports.csv")

# File that will store the parsed numerical values
PARSED_CSV = os.path.join(BASE_DIR, "parsed_table.csv")

GAS_NAMES = {
    "Hydrogen": ["H2", "H₂", "Hydrogen", "Водород"],
    "Methane": ["CH4", "CH₄", "Methane"],
    "Acetylene": ["C2H2", "C₂H₂", "Acetylene", "Ацетилен"],
    "Ethylene": ["C2H4", "C₂H₄", "Ethylene", "Этилен"],
}

def build_nlp():
    nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger"])
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = []
    for label, variants in GAS_NAMES.items():
        for v in variants:
            patterns.append({"label": label, "pattern": [{"LOWER": v.lower()}]})
    ruler.add_patterns(patterns)
    return nlp


def extract_values(text, nlp):
    doc = nlp(text)
    found = {}
    for ent in doc.ents:
        m = re.search(rf"{re.escape(ent.text)}\s*[:=]?\s*([\d\.]+)\s*ppm", text, re.IGNORECASE)
        if m:
            found[ent.label_] = float(m.group(1))
    for name, variants in GAS_NAMES.items():
        if name in found:
            continue
        for v in variants:
            m = re.search(rf"{re.escape(v)}\s*[:=]?\s*([\d\.]+)", text, re.IGNORECASE)
            if m:
                found[name] = float(m.group(1))
                break
    return found

def main():
    nlp = build_nlp()
    df = pd.read_csv(DIRTY_CSV)
    records = []
    for txt in df["dirty_report"].fillna(""):
        vals = extract_values(txt, nlp)
        records.append({g: vals.get(g) for g in GAS_NAMES})
    os.makedirs(os.path.dirname(PARSED_CSV), exist_ok=True)
    pd.DataFrame(records).to_csv(PARSED_CSV, index=False)
    print(f"✅ Распарсенные данные сохранены в {PARSED_CSV}")

if __name__ == "__main__":
    main()
