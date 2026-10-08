"""
MODULE 05 - Exercise 1: reading features

Questions about the 'countries' layer, answered with loops.
"""
from pathlib import Path

from qgis.core import QgsExpressionContextUtils, QgsFeatureRequest, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
countries = QgsVectorLayer(f"{GPKG}|layername=countries", "countries", "ogr")

# TODO 1: count countries per continent in a dictionary
#         {continent: number}. Use the .get(key, 0) + 1 pattern.
per_continent = {}


# TODO 2: the 5 most populous countries, as a list of names, biggest first.
#         Build a list of (pop_est, name) tuples, sort it with
#         .sort(reverse=True), then take the first 5 names.
top5 = []


# TODO 3: total population of South America, using a QgsFeatureRequest with
#         a filter expression, only the "pop_est" attribute, and NoGeometry
south_america_pop = 0


# TODO 4: how many countries have the -99 "unknown" code in iso_a3?
#         (loop and compare  f["iso_a3"] == "-99")
iso_missing = 0


print(per_continent)
print(top5)
print(f"{south_america_pop:,}")
print(iso_missing)

# --- Checks (don't edit below this line) ------------------------------------
assert per_continent.get("Africa") == 54 and per_continent.get("Europe") == 50, "TODO 1"
assert sum(per_continent.values()) == 242, "TODO 1: every country counted once"
assert top5 == ["China", "India", "United States of America", "Indonesia", "Pakistan"], f"TODO 2: {top5}"
assert south_america_pop == 427_066_661, f"TODO 3: got {south_america_pop}"
assert iso_missing == 8, f"TODO 4: got {iso_missing}"
print("All checks passed ✔")
