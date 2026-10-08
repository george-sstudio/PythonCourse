"""MODULE 04 - Solution 3: units, project CRS, transforms, saving"""
from pathlib import Path

from qgis.core import (QgsCoordinateReferenceSystem, QgsCoordinateTransform,
                       QgsDistanceArea, QgsExpressionContextUtils, QgsPointXY,
                       QgsProject, QgsUnitTypes, QgsVectorLayer)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA = COURSE / "data"
OUTPUT = COURSE / "output"
OUTPUT.mkdir(exist_ok=True)
project = QgsProject.instance()
project.clear()

countries = QgsVectorLayer(f"{DATA / 'natural_earth.gpkg'}|layername=countries", "countries", "ogr")
project.addMapLayer(countries)

wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")
laea = QgsCoordinateReferenceSystem("EPSG:3035")

vienna = QgsPointXY(16.3738, 48.2082)
bratislava = QgsPointXY(17.1170, 48.1500)

# 1
units = QgsUnitTypes.toString(countries.crs().mapUnits())

# 2 - a number, but not a distance
deg_distance = vienna.distance(bratislava)

# 3 - project to metres, then measure
to_laea = QgsCoordinateTransform(wgs84, laea, project)
laea_distance = to_laea.transform(vienna).distance(to_laea.transform(bratislava))

# 4 - measure on the curved Earth directly
da = QgsDistanceArea()
da.setSourceCrs(wgs84, project.transformContext())
da.setEllipsoid("EPSG:7030")
ellipsoid_distance = da.measureLine(vienna, bratislava)

print(f"units: {units}")
print(f"degrees  : {deg_distance}")
print(f"EPSG:3035: {laea_distance:,.0f} m")
print(f"ellipsoid: {ellipsoid_distance:,.0f} m")

# 5
project.setCrs(QgsCoordinateReferenceSystem("EPSG:8857"))
print("project:", project.crs().authid(), "| layer:", countries.crs().authid())

# 6
saved = project.write(str(OUTPUT / "module04.qgz"))

assert units == "degrees", f"TODO 1: got {units}"
assert 0.74 < deg_distance < 0.75, "TODO 2"
assert 55_500 < laea_distance < 55_700, f"TODO 3: got {laea_distance}"
assert 55_600 < ellipsoid_distance < 55_700, f"TODO 4: got {ellipsoid_distance}"
assert project.crs().authid() == "EPSG:8857", "TODO 5: project.setCrs(...)"
assert countries.crs().authid() == "EPSG:4326", "TODO 5: the layer keeps its CRS"
assert saved is True and (OUTPUT / "module04.qgz").exists(), "TODO 6"
print("All checks passed ✔")
