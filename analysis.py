import os
import pandas as pd
from types import SimpleNamespace
import re
from scipy import stats
from collections import defaultdict

data_location = "data"
data = defaultdict(dict)

pattern = re.compile(r"(?P<type>.*)_(?P<cam>.*)_formula.csv")
for fname in os.listdir("data"):
    record = SimpleNamespace()
    record.filename = fname
    record.df = pd.read_csv(os.path.join("data", fname))
    record.df.fillna(0)
    match = pattern.match(fname)
    record.type = match.group("type")
    record.cam = match.group("cam")
    data[record.cam][record.type] = record

for camera, record in data.items():
    print(f"Analysis for camera {camera}...")

    active, inactive = (
        record["active"].df["result"].values,
        record["inactive"].df["result"].values,
    )
    print(f"{len(active)} vs {len(inactive)}")
    results = stats.mannwhitneyu(active, inactive, alternative="greater")
    print(results)
