"""MODULE 02 - Solution 3: read a CSV file and find the nearest capitals"""
import csv
import math
from pathlib import Path

from qgis.core import QgsExpressionContextUtils

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
csv_path = COURSE / "data" / "capitals.csv"


def distance_km(lat1, lon1, lat2, lon2):
    """Great-circle distance between two lat/lon points, in km."""
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


VIENNA = (48.2082, 16.3738)

row_count = 0
megacities = []
distances = []

with open(csv_path, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row_count += 1
        pop = int(row["pop_max"])
        if pop > 10_000_000:
            megacities.append(row["name"])

        lat = float(row["latitude"])
        lon = float(row["longitude"])
        d = distance_km(VIENNA[0], VIENNA[1], lat, lon)
        distances.append((d, row["name"]))

distances.sort()

nearest5 = []
for d, name in distances[1:6]:      # skip index 0 (Vienna itself)
    nearest5.append(name)
# same thing as a list comprehension:
# nearest5 = [name for d, name in distances[1:6]]

print(row_count, "capitals read")
print("Megacities:", megacities)
print("Nearest to Vienna:", nearest5)

assert row_count == 215
assert len(megacities) == 8 and "Tokyo" in megacities, f"TODO 1: got {megacities}"
assert len(distances) == 215, "TODO 2: one (distance, name) per row"
assert nearest5 == ["Bratislava", "Budapest", "Prague", "Zagreb", "Ljubljana"], f"TODO 3: got {nearest5}"
print("All checks passed ✔")
