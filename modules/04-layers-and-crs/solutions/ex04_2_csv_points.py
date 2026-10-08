"""MODULE 04 - Solution 2: points from a CSV - and the x/y swap"""
from pathlib import Path

from qgis.core import QgsExpressionContextUtils, QgsProject, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
CSV = COURSE / "data" / "capitals.csv"
project = QgsProject.instance()

# Part A
uri = f"{CSV.as_uri()}?delimiter=,&xField=longitude&yField=latitude&crs=EPSG:4326"
capitals = QgsVectorLayer(uri, "Capitals", "delimitedtext")
if not capitals.isValid():
    raise RuntimeError(f"CSV did not load: {uri}")
project.addMapLayer(capitals)

vienna = next(capitals.getFeatures("name = 'Vienna'"))
pt = vienna.geometry().asPoint()
print("Vienna x (lon) =", round(pt.x(), 2), " y (lat) =", round(pt.y(), 2))

# Part B
swapped_uri = f"{CSV.as_uri()}?delimiter=,&xField=latitude&yField=longitude&crs=EPSG:4326"
swapped = QgsVectorLayer(swapped_uri, "Capitals (swapped!)", "delimitedtext")
project.addMapLayer(swapped)

v2 = next(swapped.getFeatures("name = 'Vienna'")).geometry().asPoint()
print("Swapped Vienna x =", round(v2.x(), 2), " y =", round(v2.y(), 2))

# The swap mirrors the world across the diagonal line x = y: every capital
# moves to (lat, lon), so the map looks rotated and squashed, and points
# whose longitude is beyond +-90 get a "latitude" that cannot exist.

assert capitals.isValid() and capitals.featureCount() == 215
assert capitals.crs().authid() == "EPSG:4326"
assert round(pt.x(), 1) == 16.4 and round(pt.y(), 1) == 48.2, "Part A: x must be longitude"
assert round(v2.x(), 1) == 48.2, "Part B: swap the two fields"
print("All checks passed ✔")
