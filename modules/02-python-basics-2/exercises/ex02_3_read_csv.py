"""
MODULE 02 - Exercise 3: read a CSV file and find the nearest capitals

Data: data/capitals.csv  (columns: name, country, adm0_a3, pop_max,
                          latitude, longitude)
Remember: everything read from a CSV is TEXT. Convert with int() / float().
"""
import csv
import math
from pathlib import Path

from qgis.core import QgsExpressionContextUtils

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
csv_path = COURSE / "data" / "capitals.csv"


def distance_km(lat1, lon1, lat2, lon2):
    """Great-circle distance between two lat/lon points, in km
    (the 'haversine' formula). You don't need to understand the maths -
    just READ the function: what goes in, what comes out?"""
    r = 6371.0088  # mean Earth radius in km
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


VIENNA = (48.2082, 16.3738)   # a tuple: (lat, lon)

row_count = 0
megacities = []      # names of capitals with pop_max over 10 million
distances = []       # will hold (distance, name) tuples

with open(csv_path, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row_count += 1
        # TODO 1: convert pop_max to int; if it is over 10_000_000,
        #         append row["name"] to megacities

        # TODO 2: convert latitude and longitude to float, compute the
        #         distance to VIENNA with distance_km(...), and append the
        #         tuple (distance, row["name"]) to distances
        pass

# Sorting a list of tuples sorts by the FIRST item (the distance)
distances.sort()

# TODO 3: the 5 nearest capitals, NOT counting Vienna itself.
#         distances[0] is Vienna (distance ~0). Take a slice of the next 5,
#         and keep only the names.
nearest5 = []

print(row_count, "capitals read")
print("Megacities:", megacities)
print("Nearest to Vienna:", nearest5)

# --- Checks (don't edit below this line) ------------------------------------
assert row_count == 215
assert len(megacities) == 8 and "Tokyo" in megacities, f"TODO 1: got {megacities}"
assert len(distances) == 215, "TODO 2: one (distance, name) per row"
assert nearest5 == ["Bratislava", "Budapest", "Prague", "Zagreb", "Ljubljana"], f"TODO 3: got {nearest5}"
print("All checks passed ✔")
