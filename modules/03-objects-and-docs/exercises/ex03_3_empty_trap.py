"""
MODULE 03 - Exercise 3: the "came back empty" trap

Part A shows the trap. Part B: write a helper that fails CLEARLY.
"""
from pathlib import Path

from qgis.core import QgsExpressionContextUtils, QgsProject, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA = COURSE / "data"
project = QgsProject.instance()

lakes = QgsVectorLayer(f"{DATA / 'natural_earth.gpkg'}|layername=lakes", "lakes", "ogr")
project.addMapLayer(lakes)

# --- Part A: see the trap (just read and run) -------------------------------
print(project.mapLayersByName("lakes"))   # a list with one layer
print(project.mapLayersByName("Lakes"))   # [] - wrong case, EMPTY list, no error

missing = QgsVectorLayer(f"{DATA / 'natural_earth.gpkg'}|layername=glaciers", "glaciers", "ogr")
print("valid?", missing.isValid(), "features:", missing.featureCount())   # no error!


# --- Part B: your helper -------------------------------------------------------
def get_layer(name):
    """Return the ONE layer in the current project called `name`.
    If there is none, raise a RuntimeError whose message lists the layer
    names that DO exist, so the user can spot the typo.
    """
    # TODO: 1. found = project.mapLayersByName(name)
    #       2. if found is empty (hint: `if not found:`), build a list of the
    #          existing names:  [lyr.name() for lyr in project.mapLayers().values()]
    #          and  raise RuntimeError(f"No layer called {name!r}. Layers: {names}")
    #       3. otherwise return found[0]
    pass


# --- Checks (don't edit below this line) ------------------------------------
assert get_layer("lakes").name() == "lakes", "get_layer should return the layer"
try:
    get_layer("Lakes")
    raise AssertionError("get_layer('Lakes') should have raised a RuntimeError")
except RuntimeError as err:
    print("Good, a clear error:", err)
    assert "lakes" in str(err), "the message should list the existing layer names"
print("All checks passed ✔")
