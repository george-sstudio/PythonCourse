"""MODULE 05 - Solution 1: reading features"""
from pathlib import Path

from qgis.core import QgsExpressionContextUtils, QgsFeatureRequest, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
countries = QgsVectorLayer(f"{GPKG}|layername=countries", "countries", "ogr")

# 1 - counting pattern
per_continent = {}
for f in countries.getFeatures():
    c = f["continent"]
    per_continent[c] = per_continent.get(c, 0) + 1

# 2 - sort tuples; the first item (population) decides the order
pairs = []
for f in countries.getFeatures():
    pairs.append((f["pop_est"], f["name"]))
pairs.sort(reverse=True)
top5 = [name for pop, name in pairs[:5]]

# 3 - a lean request: filter + one attribute + no geometry
request = (QgsFeatureRequest()
           .setFilterExpression("\"continent\" = 'South America'")
           .setSubsetOfAttributes(["pop_est"], countries.fields())
           .setFlags(QgsFeatureRequest.Flag.NoGeometry))
south_america_pop = 0
for f in countries.getFeatures(request):
    south_america_pop += f["pop_est"]

# 4 - Natural Earth's "unknown" marker
iso_missing = 0
for f in countries.getFeatures():
    if f["iso_a3"] == "-99":
        iso_missing += 1

print(per_continent)
print(top5)
print(f"{south_america_pop:,}")
print(iso_missing)

assert per_continent.get("Africa") == 54 and per_continent.get("Europe") == 50, "TODO 1"
assert sum(per_continent.values()) == 242, "TODO 1: every country counted once"
assert top5 == ["China", "India", "United States of America", "Indonesia", "Pakistan"], f"TODO 2: {top5}"
assert south_america_pop == 427_066_661, f"TODO 3: got {south_america_pop}"
assert iso_missing == 8, f"TODO 4: got {iso_missing}"
print("All checks passed ✔")
