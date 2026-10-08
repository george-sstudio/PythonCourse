"""
MODULE 05 - Exercise 3: geometry - which country, which neighbours, how big?
"""
from pathlib import Path

from qgis.core import (QgsDistanceArea, QgsExpressionContextUtils, QgsFeatureRequest,
                       QgsGeometry, QgsPointXY, QgsProject, QgsVectorLayer)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
countries = QgsVectorLayer(f"{GPKG}|layername=countries", "countries", "ogr")

# TODO 1: which country contains this point? (lon -66.0, lat -20.0)
#         Make a QgsGeometry.fromPointXY(QgsPointXY(x, y)) and loop with .contains()
mystery_country = None

# Austria, found by its code
austria = next(countries.getFeatures("\"adm0_a3\" = 'AUT'"))

# TODO 2: the names of Austria's neighbours: every OTHER country whose
#         geometry intersects Austria's. Speed it up with
#         QgsFeatureRequest().setFilterRect(austria.geometry().boundingBox())
neighbours = []

# TODO 3: Austria's area in km2, measured on the ellipsoid (QgsDistanceArea,
#         source CRS = countries.crs(), ellipsoid "EPSG:7030"). Round to whole km2.
area_km2 = None

# This is what NOT to do - "square degrees":
naive = austria.geometry().area()
print(f"naive area: {naive:.2f} (square degrees - meaningless)")

# TODO 4: the centroid of Austria as (lon, lat), each rounded to 1 decimal
centroid = None

print(mystery_country, sorted(neighbours), area_km2, centroid)

# --- Checks (don't edit below this line) ------------------------------------
assert mystery_country == "Bolivia", f"TODO 1: got {mystery_country}"
assert sorted(neighbours) == ["Czechia", "Germany", "Hungary", "Italy", "Liechtenstein",
                              "Slovakia", "Slovenia", "Switzerland"], f"TODO 2: {neighbours}"
assert 84_000 < area_km2 < 84_300, f"TODO 3: got {area_km2}"
assert centroid == (14.1, 47.6), f"TODO 4: got {centroid}"
print("All checks passed ✔")
