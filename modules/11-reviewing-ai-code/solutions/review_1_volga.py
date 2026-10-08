"""
MODULE 11 - Review 1 (solution): cities along the Volga

PROBLEMS FOUND
  1. Buffer in DEGREES (0.045). The Volga runs at 45-58 N, where 0.045 degrees
     of longitude is only 2.7-3.5 km east-west. The buffer is squashed and
     misses Astrakhan.                                  (checklist 4: CRS/units)
  2. "square degrees * 111 * 111" is not km2: a degree of longitude shrinks
     with latitude, so this conversion over-counts east-west. It reports
     ~43,900 km2 for a zone that is really narrower than 5 km - two errors
     that don't cancel. The real 5 km zone is ~32,000 km2.
                                                        (checklist 4)
  3. The comment "1 degree = 111 km" sounds authoritative - it's only true
     north-south. Comments in AI code are claims, not facts.
  4. Minor: 'memory:' still works, but 'TEMPORARY_OUTPUT' is the current form;
     no isValid() check on the layers.                   (checklist 6)
FIX: reproject the river to a local metric CRS (azimuthal equidistant centred
on the river), buffer 5000 m there, measure the zone there (or with
QgsDistanceArea).
"""
from pathlib import Path

import processing
from qgis.core import (QgsCoordinateReferenceSystem, QgsExpressionContextUtils,
                       QgsVectorLayer)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"

rivers = QgsVectorLayer(f"{GPKG}|layername=rivers", "rivers", "ogr")
places = QgsVectorLayer(f"{GPKG}|layername=places", "places", "ogr")
for layer in (rivers, places):
    if not layer.isValid():
        raise RuntimeError(f"{layer.name()} did not load")

volga = processing.run("native:extractbyexpression", {
    "INPUT": rivers, "EXPRESSION": "\"name\" = 'Volga'",
    "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]

# a CRS in metres, centred on the river
centre = volga.extent().center()
local = QgsCoordinateReferenceSystem.fromProj(
    f"+proj=aeqd +lat_0={centre.y():.4f} +lon_0={centre.x():.4f} +datum=WGS84 +units=m +no_defs")
volga_m = processing.run("native:reprojectlayer", {
    "INPUT": volga, "TARGET_CRS": local, "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]

zone = processing.run("native:buffer", {
    "INPUT": volga_m, "DISTANCE": 5000, "SEGMENTS": 8, "DISSOLVE": True,
    "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]

near = processing.run("native:extractbylocation", {
    "INPUT": places, "PREDICATE": [0], "INTERSECT": zone,
    "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
names = sorted(f["name"] for f in near.getFeatures())

zone_km2 = sum(f.geometry().area() for f in zone.getFeatures()) / 1e6   # zone is in metres

print(f"{len(names)} cities within 5 km of the Volga: {', '.join(names)}")
print(f"The 5 km zone covers {zone_km2:,.0f} km2")

from qgis.core import QgsDistanceArea, QgsProject
da = QgsDistanceArea()
da.setSourceCrs(rivers.crs(), QgsProject.instance().transformContext())
da.setEllipsoid("EPSG:7030")
length_km = sum(da.measureLength(f.geometry()) for f in volga.getFeatures()) / 1000
expected_km2 = 2 * 5 * length_km
print(f"(independent estimate of the zone: {expected_km2:,.0f} km2)")
assert names == ["Astrakhan", "Nizhny Novgorod", "Samara", "Tver", "Ulyanovsk", "Yaroslavl"], \
    f"cities: {names}"
assert 0.9 < zone_km2 / expected_km2 < 1.1, f"zone area {zone_km2:,.0f} vs about {expected_km2:,.0f}"
print("All checks passed ✔")
