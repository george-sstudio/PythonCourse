"""
MODULE 04 - Exercise 3: units, project CRS, transforms, saving

The question: how far is Vienna from Bratislava?
You'll get three answers. Only two are real distances.
"""
from pathlib import Path

from qgis.core import (QgsCoordinateReferenceSystem, QgsCoordinateTransform,
                       QgsDistanceArea, QgsExpressionContextUtils, QgsPointXY,
                       QgsProject, QgsUnitTypes, QgsVectorLayer)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA = COURSE / "data"
OUTPUT = COURSE / "output"
project = QgsProject.instance()
project.clear()

countries = QgsVectorLayer(f"{DATA / 'natural_earth.gpkg'}|layername=countries", "countries", "ogr")
project.addMapLayer(countries)

wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")
laea = QgsCoordinateReferenceSystem("EPSG:3035")      # ETRS89 / LAEA Europe

vienna = QgsPointXY(16.3738, 48.2082)       # (lon, lat)  x first!
bratislava = QgsPointXY(17.1170, 48.1500)

# TODO 1: the map units of the countries layer's CRS as text
#         (QgsUnitTypes.toString(...mapUnits()))
units = None

# TODO 2: the "distance" in degrees: vienna.distance(bratislava)
deg_distance = None

# TODO 3: transform both points to EPSG:3035 with a QgsCoordinateTransform
#         (wgs84 -> laea, project) and measure the distance in metres
laea_distance = None

# TODO 4: measure on the ellipsoid with QgsDistanceArea
#         (setSourceCrs(wgs84, project.transformContext()), setEllipsoid("EPSG:7030"),
#          then measureLine(vienna, bratislava))
ellipsoid_distance = None

print(f"units: {units}")
print(f"degrees  : {deg_distance}")
print(f"EPSG:3035: {laea_distance:,.0f} m" if laea_distance else "EPSG:3035: ?")
print(f"ellipsoid: {ellipsoid_distance:,.0f} m" if ellipsoid_distance else "ellipsoid: ?")

# TODO 5: set the PROJECT CRS to Equal Earth (EPSG:8857). Then check that
#         the countries layer's own CRS did NOT change.


# TODO 6: save the project to OUTPUT / "module04.qgz" (project.write needs str)
saved = None

# --- Checks (don't edit below this line) ------------------------------------
assert units == "degrees", f"TODO 1: got {units}"
assert 0.74 < deg_distance < 0.75, "TODO 2"
assert 55_500 < laea_distance < 55_700, f"TODO 3: got {laea_distance}"
assert 55_600 < ellipsoid_distance < 55_700, f"TODO 4: got {ellipsoid_distance}"
assert project.crs().authid() == "EPSG:8857", "TODO 5: project.setCrs(...)"
assert countries.crs().authid() == "EPSG:4326", "TODO 5: the layer keeps its CRS"
assert saved is True and (OUTPUT / "module04.qgz").exists(), "TODO 6"
print("All checks passed ✔")
