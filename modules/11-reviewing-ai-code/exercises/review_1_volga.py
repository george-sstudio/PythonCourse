"""
MODULE 11 - Review 1: cities along the Volga

THE REQUEST (what George asked Claude)
    "Which cities are within 5 km of the Volga? Also tell me the area of that
     5 km zone in km2. QGIS 3.40."

THE AI'S ANSWER is below. It runs without errors and prints a confident result.

YOUR JOB
    1. Review it with the checklist (AI_PLAYBOOK.md §4) BEFORE running it.
       Write each problem you find as a comment: # PROBLEM: ...
    2. Run it. Do the checks at the bottom agree with the AI's printout?
    3. Fix the code until the checks pass. Don't edit the checks.
"""
from pathlib import Path

import processing
from qgis.core import QgsExpressionContextUtils, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"

# ======================= the AI's code starts here ==============================
rivers = QgsVectorLayer(f"{GPKG}|layername=rivers", "rivers", "ogr")
places = QgsVectorLayer(f"{GPKG}|layername=places", "places", "ogr")

volga = processing.run("native:extractbyexpression", {
    "INPUT": rivers, "EXPRESSION": "\"name\" = 'Volga'", "OUTPUT": "memory:"})["OUTPUT"]

# 5 km is about 0.045 degrees (1 degree = 111 km)
zone = processing.run("native:buffer", {
    "INPUT": volga, "DISTANCE": 0.045, "SEGMENTS": 8, "DISSOLVE": True,
    "OUTPUT": "memory:"})["OUTPUT"]

near = processing.run("native:extractbylocation", {
    "INPUT": places, "PREDICATE": [0], "INTERSECT": zone, "OUTPUT": "memory:"})["OUTPUT"]
names = sorted(f["name"] for f in near.getFeatures())

# convert square degrees to km2
zone_km2 = sum(f.geometry().area() for f in zone.getFeatures()) * 111 * 111

print(f"{len(names)} cities within 5 km of the Volga: {', '.join(names)}")
print(f"The 5 km zone covers {zone_km2:,.0f} km2")
# ======================= the AI's code ends here ================================

# --- Checks (don't edit below this line) ------------------------------------
from qgis.core import QgsDistanceArea, QgsProject
da = QgsDistanceArea()
da.setSourceCrs(rivers.crs(), QgsProject.instance().transformContext())
da.setEllipsoid("EPSG:7030")
length_km = sum(da.measureLength(f.geometry()) for f in volga.getFeatures()) / 1000
expected_km2 = 2 * 5 * length_km           # a 5 km buffer around a line of length L
print(f"(independent estimate of the zone: {expected_km2:,.0f} km2)")
assert names == ["Astrakhan", "Nizhny Novgorod", "Samara", "Tver", "Ulyanovsk", "Yaroslavl"], \
    f"cities: {names}"
assert 0.9 < zone_km2 / expected_km2 < 1.1, f"zone area {zone_km2:,.0f} vs about {expected_km2:,.0f}"
print("All checks passed ✔")
