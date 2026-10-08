"""
MODULE 11 - Review 6: methods that don't exist

THE REQUEST
    "For Peru: how many places are there, which is the biggest (by pop_max),
     and what is Peru's area in km2? Then count places per country for all of
     South America with a Processing tool. QGIS 3.40."

THE AI'S ANSWER is below. This time it CRASHES - several times. The AI
invented names that sound right. Your tools: dir(), help(), the registry
search from Module 06, processing.algorithmHelp(), and your context card.

YOUR JOB: run, read each traceback (bottom line first), find the REAL
method / tool / field, fix, run again. Write each finding as # PROBLEM: ...
Hint: five invented or wrong names.
"""
from pathlib import Path

import processing
from qgis.core import QgsExpressionContextUtils, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"

# ======================= the AI's code starts here ==============================
countries = QgsVectorLayer(f"{GPKG}|layername=countries", "countries", "ogr")
places = QgsVectorLayer(f"{GPKG}|layername=places", "places", "ogr")

peru = countries.getFeatureByAttribute("adm0_a3", "PER")
n_places = places.getFeatureCount("\"adm0_a3\" = 'PER'")
biggest = max(places.getFeatures("\"adm0_a3\" = 'PER'"), key=lambda f: f["population"])["name"]
area_km2 = peru.geometry().areaKm2()

result = processing.run("native:countpointsinpolygons", {
    "POLYGONS": f"{GPKG}|layername=countries", "POINTS": f"{GPKG}|layername=places",
    "FIELD": "n_places", "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
per_country = {f["name"]: f["n_places"] for f in result.getFeatures("\"continent\" = 'South America'")}

print(f"Peru: {n_places} places, biggest {biggest}, area {area_km2:,.0f} km2")
print(per_country)
# ======================= the AI's code ends here ================================

# --- Checks (don't edit below this line) ------------------------------------
assert n_places == 11, n_places
assert biggest == "Lima", biggest
assert 1_290_000 < area_km2 < 1_300_000, area_km2
assert per_country["Peru"] == 11 and per_country["Brazil"] == 43, per_country
print("All checks passed ✔")
