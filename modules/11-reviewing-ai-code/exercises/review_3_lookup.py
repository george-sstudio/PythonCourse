"""
MODULE 11 - Review 3: capitals and missing provinces

THE REQUEST
    "For these countries: France, Côte d'Ivoire, Norway, Antarctica - give me
     the number of places, the capital(s), and how many of their places have
     no province (adm1name is empty). QGIS 3.40."

THE AI'S ANSWER is below. It runs and prints a neat table.

YOUR JOB: review (# PROBLEM: ...), run, compare with the checks, fix.
Hint: three problems. One of them only happens in QGIS 3 - the same code
would be right in QGIS 4. Use the context card (Module 10) and data/README.md.
"""
from pathlib import Path

from qgis.core import QgsExpressionContextUtils, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"

# ======================= the AI's code starts here ==============================
countries = QgsVectorLayer(f"{GPKG}|layername=countries", "countries", "ogr")
places = QgsVectorLayer(f"{GPKG}|layername=places", "places", "ogr")

wanted = ["France", "Côte d'Ivoire", "Norway", "Antarctica"]
results = {}

for name in wanted:
    for country in countries.getFeatures(f"\"name\" = '{name}'"):
        code = country["iso_a3"]
        its_places = list(places.getFeatures(f"\"adm0_a3\" = '{code}'"))
        capitals = [p["name"] for p in its_places if p["featurecla"].startswith("Admin-0 capital")]
        no_province = 0
        for p in its_places:
            if p["adm1name"] is None:
                no_province += 1
        results[name] = (len(its_places), capitals, no_province)

for name, (n, caps, missing) in results.items():
    print(f"{name:15} {n:3} places | capital: {', '.join(caps) or '-':25} | no province: {missing}")
# ======================= the AI's code ends here ================================

# --- Checks (don't edit below this line) ------------------------------------
assert set(results) == set(wanted), f"countries missing from the results: {set(wanted) - set(results)}"
assert results["France"][:2] == (28, ["Paris"]), f"France: {results['France']}"
assert results["Norway"][:2] == (6, ["Oslo"]), f"Norway: {results['Norway']}"
assert sorted(results["Côte d'Ivoire"][1]) == ["Abidjan", "Yamoussoukro"]
assert results["Antarctica"][2] == 40, f"Antarctica places with no province: {results['Antarctica'][2]}"
print("All checks passed ✔")
