"""
MODULE 04 - Exercise 2: points from a CSV - and the x/y swap

Part A: load capitals.csv correctly.
Part B: load it again with x and y SWAPPED and see what changes.
"""
from pathlib import Path

from qgis.core import QgsExpressionContextUtils, QgsProject, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
CSV = COURSE / "data" / "capitals.csv"
project = QgsProject.instance()

# --- Part A ----------------------------------------------------------------------
# TODO: build the delimited-text URI with xField=longitude and yField=latitude
#       and crs=EPSG:4326  (start with CSV.as_uri())
uri = None
if uri is None:
    raise RuntimeError("Part A: build the uri first (see the TODO above)")
capitals = QgsVectorLayer(uri, "Capitals", "delimitedtext")
# TODO: check it is valid (raise if not) and add it to the project


# Where is Vienna? Look it up through an expression filter (Module 05 explains)
vienna = next(capitals.getFeatures("name = 'Vienna'"))
pt = vienna.geometry().asPoint()
print("Vienna x (lon) =", round(pt.x(), 2), " y (lat) =", round(pt.y(), 2))

# --- Part B: the classic swap ---------------------------------------------------
# TODO: copy your uri but swap: xField=latitude, yField=longitude
swapped_uri = None
swapped = QgsVectorLayer(swapped_uri, "Capitals (swapped!)", "delimitedtext")
project.addMapLayer(swapped)

v2 = next(swapped.getFeatures("name = 'Vienna'")).geometry().asPoint()
print("Swapped Vienna x =", round(v2.x(), 2), " y =", round(v2.y(), 2))

# TODO: in one sentence, what does the swap do to the map?
#       Write it here as a comment:
#

# --- Checks (don't edit below this line) ------------------------------------
assert capitals.isValid() and capitals.featureCount() == 215
assert capitals.crs().authid() == "EPSG:4326"
assert round(pt.x(), 1) == 16.4 and round(pt.y(), 1) == 48.2, "Part A: x must be longitude"
assert round(v2.x(), 1) == 48.2, "Part B: swap the two fields"
print("All checks passed ✔")
