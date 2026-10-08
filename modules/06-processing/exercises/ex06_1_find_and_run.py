"""
MODULE 06 - Exercise 1: find tools and run them
"""
from pathlib import Path

import processing
from qgis.core import QgsApplication, QgsExpressionContextUtils, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
countries = f"{GPKG}|layername=countries"      # a path string works as INPUT

# TODO 1: list the IDs of all algorithms whose id contains "dissolve"
dissolve_ids = []

# TODO 2: print the help for native:centroids (read it!)


# TODO 3: run native:centroids on countries with OUTPUT "TEMPORARY_OUTPUT".
#         Store the resulting LAYER in `centroids`
centroids = None

# TODO 4: run native:dissolve on countries, FIELD ["continent"],
#         OUTPUT "TEMPORARY_OUTPUT". Store the layer in `continents`
continents = None

# TODO 5: run native:centroids again, but this time OUTPUT to the file
#         COURSE / "output" / "centroids.gpkg"   (as a str).
#         What TYPE is result["OUTPUT"] now? Store it in `file_result`
file_result = None
print("type of file result:", type(file_result))

print(dissolve_ids)
print(centroids.featureCount() if centroids else None,
      continents.featureCount() if continents else None)

# --- Checks (don't edit below this line) ------------------------------------
assert "native:dissolve" in dissolve_ids, "TODO 1"
assert isinstance(centroids, QgsVectorLayer) and centroids.featureCount() == 242, "TODO 3"
assert continents.featureCount() == 8, "TODO 4: 8 continents (incl. 'Seven seas')"
assert isinstance(file_result, str), "TODO 5: a file output comes back as a path (str)"
assert QgsVectorLayer(file_result, "c", "ogr").featureCount() == 242
print("All checks passed ✔")
