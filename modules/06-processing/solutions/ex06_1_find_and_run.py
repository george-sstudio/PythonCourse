"""MODULE 06 - Solution 1: find tools and run them"""
from pathlib import Path

import processing
from qgis.core import QgsApplication, QgsExpressionContextUtils, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
(COURSE / "output").mkdir(exist_ok=True)
countries = f"{GPKG}|layername=countries"

# 1
dissolve_ids = [alg.id() for alg in QgsApplication.processingRegistry().algorithms()
                if "dissolve" in alg.id()]

# 2
processing.algorithmHelp("native:centroids")

# 3 - TEMPORARY_OUTPUT from a native vector tool -> a layer object
centroids = processing.run("native:centroids", {
    "INPUT": countries, "ALL_PARTS": False, "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]

# 4
continents = processing.run("native:dissolve", {
    "INPUT": countries, "FIELD": ["continent"], "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]

# 5 - a file output -> the path, as text
file_result = processing.run("native:centroids", {
    "INPUT": countries, "OUTPUT": str(COURSE / "output" / "centroids.gpkg")})["OUTPUT"]
print("type of file result:", type(file_result))

print(dissolve_ids)
print(centroids.featureCount(), continents.featureCount())

assert "native:dissolve" in dissolve_ids, "TODO 1"
assert isinstance(centroids, QgsVectorLayer) and centroids.featureCount() == 242, "TODO 3"
assert continents.featureCount() == 8, "TODO 4: 8 continents (incl. 'Seven seas')"
assert isinstance(file_result, str), "TODO 5: a file output comes back as a path (str)"
assert QgsVectorLayer(file_result, "c", "ogr").featureCount() == 242
print("All checks passed ✔")
