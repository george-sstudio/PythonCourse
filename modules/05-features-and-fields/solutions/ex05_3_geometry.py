"""MODULE 05 - Solution 3: geometry - which country, which neighbours, how big?"""
from pathlib import Path

from qgis.core import (QgsDistanceArea, QgsExpressionContextUtils, QgsFeatureRequest,
                       QgsGeometry, QgsPointXY, QgsProject, QgsVectorLayer)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
countries = QgsVectorLayer(f"{GPKG}|layername=countries", "countries", "ogr")

# 1 - point in polygon
point = QgsGeometry.fromPointXY(QgsPointXY(-66.0, -20.0))     # x = lon first
mystery_country = None
for f in countries.getFeatures():
    if f.geometry().contains(point):
        mystery_country = f["name"]
        break                     # found it - stop looping

austria = next(countries.getFeatures("\"adm0_a3\" = 'AUT'"))
a_geom = austria.geometry()

# 2 - quick bounding-box filter first, then the exact (slower) test
neighbours = []
request = QgsFeatureRequest().setFilterRect(a_geom.boundingBox())
for f in countries.getFeatures(request):
    if f.id() != austria.id() and f.geometry().intersects(a_geom):
        neighbours.append(f["name"])

# 3 - ellipsoidal area
da = QgsDistanceArea()
da.setSourceCrs(countries.crs(), QgsProject.instance().transformContext())
da.setEllipsoid("EPSG:7030")
area_km2 = round(da.measureArea(a_geom) / 1_000_000)

naive = a_geom.area()
print(f"naive area: {naive:.2f} (square degrees - meaningless)")

# 4 - centroid
c = a_geom.centroid().asPoint()
centroid = (round(c.x(), 1), round(c.y(), 1))

print(mystery_country, sorted(neighbours), area_km2, centroid)

assert mystery_country == "Bolivia", f"TODO 1: got {mystery_country}"
assert sorted(neighbours) == ["Czechia", "Germany", "Hungary", "Italy", "Liechtenstein",
                              "Slovakia", "Slovenia", "Switzerland"], f"TODO 2: {neighbours}"
assert 84_000 < area_km2 < 84_300, f"TODO 3: got {area_km2}"
assert centroid == (14.1, 47.6), f"TODO 4: got {centroid}"
print("All checks passed ✔")
