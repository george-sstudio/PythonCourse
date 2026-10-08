"""
MODULE 03 - Exercise 1: ask a layer about itself

Each TODO needs ONE method call on `layer` (sometimes a chain of two).
Use the console + dir()/help() to find the methods if you're unsure.
"""
from pathlib import Path

from qgis.core import Qgis, QgsExpressionContextUtils, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA = COURSE / "data"

layer = QgsVectorLayer(f"{DATA / 'natural_earth.gpkg'}|layername=rivers", "rivers", "ogr")
if not layer.isValid():
    raise RuntimeError("rivers layer did not load - did you run setup_course.py?")

# TODO 1: the layer's name (a str)
name = None

# TODO 2: how many features it has (an int)
n = None

# TODO 3: the CRS authority id, e.g. "EPSG:4326"  (chain: crs() then authid())
crs_id = None

# TODO 4: the geometry type. Compare it with Qgis.GeometryType.Line
#         -> is_line should be True or False
is_line = None

# TODO 5: a list of the field names.
#         Hint: layer.fields() gives a QgsFields object; it has .names()
field_names = None

# TODO 6: use dir() and a filter to find every method name that contains
#         the word "extent" (lower case comparison). Store the list.
extent_methods = None

print(name, n, crs_id, is_line)
print(field_names)
print(extent_methods)

# --- Checks (don't edit below this line) ------------------------------------
assert name == "rivers"
assert n == 478, f"TODO 2: got {n}"
assert crs_id == "EPSG:4326", f"TODO 3: got {crs_id}"
assert is_line is True, "TODO 4: layer.geometryType() == Qgis.GeometryType.Line"
assert field_names == ["fid", "name", "featurecla", "scalerank"], f"TODO 5: got {field_names}"
assert "extent" in extent_methods, "TODO 6: [m for m in dir(layer) if 'extent' in m.lower()]"
print("All checks passed ✔")
