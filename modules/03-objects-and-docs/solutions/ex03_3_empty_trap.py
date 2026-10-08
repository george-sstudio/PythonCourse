"""MODULE 03 - Solution 3: the "came back empty" trap"""
from pathlib import Path

from qgis.core import QgsExpressionContextUtils, QgsProject, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA = COURSE / "data"
project = QgsProject.instance()

lakes = QgsVectorLayer(f"{DATA / 'natural_earth.gpkg'}|layername=lakes", "lakes", "ogr")
project.addMapLayer(lakes)

print(project.mapLayersByName("lakes"))
print(project.mapLayersByName("Lakes"))

missing = QgsVectorLayer(f"{DATA / 'natural_earth.gpkg'}|layername=glaciers", "glaciers", "ogr")
print("valid?", missing.isValid(), "features:", missing.featureCount())


def get_layer(name):
    """Return the ONE layer in the current project called `name`, or fail clearly."""
    found = project.mapLayersByName(name)
    if not found:
        names = [lyr.name() for lyr in project.mapLayers().values()]
        raise RuntimeError(f"No layer called {name!r}. Layers: {names}")
    return found[0]


assert get_layer("lakes").name() == "lakes", "get_layer should return the layer"
try:
    get_layer("Lakes")
    raise AssertionError("get_layer('Lakes') should have raised a RuntimeError")
except RuntimeError as err:
    print("Good, a clear error:", err)
    assert "lakes" in str(err), "the message should list the existing layer names"
print("All checks passed ✔")
