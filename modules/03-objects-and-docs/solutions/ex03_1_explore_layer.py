"""MODULE 03 - Solution 1: ask a layer about itself"""
from pathlib import Path

from qgis.core import Qgis, QgsExpressionContextUtils, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA = COURSE / "data"

layer = QgsVectorLayer(f"{DATA / 'natural_earth.gpkg'}|layername=rivers", "rivers", "ogr")
if not layer.isValid():
    raise RuntimeError("rivers layer did not load - did you run setup_course.py?")

name = layer.name()
n = layer.featureCount()
crs_id = layer.crs().authid()
is_line = layer.geometryType() == Qgis.GeometryType.Line
field_names = layer.fields().names()      # note: GeoPackages add an "fid" field
extent_methods = [m for m in dir(layer) if "extent" in m.lower()]

print(name, n, crs_id, is_line)
print(field_names)
print(extent_methods)

assert name == "rivers"
assert n == 478, f"TODO 2: got {n}"
assert crs_id == "EPSG:4326", f"TODO 3: got {crs_id}"
assert is_line is True, "TODO 4: layer.geometryType() == Qgis.GeometryType.Line"
assert field_names == ["fid", "name", "featurecla", "scalerank"], f"TODO 5: got {field_names}"
assert "extent" in extent_methods, "TODO 6: [m for m in dir(layer) if 'extent' in m.lower()]"
print("All checks passed ✔")
