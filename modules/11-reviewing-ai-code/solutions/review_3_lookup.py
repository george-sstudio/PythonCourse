"""
MODULE 11 - Review 3 (solution): capitals and missing provinces

PROBLEMS FOUND
  1. f"\"name\" = '{name}'" breaks for Côte d'Ivoire: the apostrophe ends the
     text, the expression is invalid, getFeatures() returns NOTHING, and the
     loop silently skips the country.       (checklist 8: edge cases; 6: silent)
  2. iso_a3 is '-99' for France and Norway (see data/README.md), so they get
     0 places and no capital. Use adm0_a3.   (checklist 3: names/values)
  3. `p["adm1name"] is None` is always False in QGIS 3, where NULL is a
     QVariant, not None, so Antarctica shows 0 instead of 40. (In QGIS 4 this
     line happens to work - a version-dependent bug.) Use
     QgsVariantUtils.isNull().              (checklist 2 and 7)
  Bonus: Côte d'Ivoire has TWO places marked 'Admin-0 capital' in the data
  (Yamoussoukro, the official capital, and Abidjan, the economic one). Real
  data is often like that - the request said "capital(s)" for a reason.
"""
from pathlib import Path

from qgis.core import QgsExpression, QgsExpressionContextUtils, QgsVariantUtils, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"

countries = QgsVectorLayer(f"{GPKG}|layername=countries", "countries", "ogr")
places = QgsVectorLayer(f"{GPKG}|layername=places", "places", "ogr")

wanted = ["France", "Côte d'Ivoire", "Norway", "Antarctica"]
results = {}

for name in wanted:
    expr = f"\"name\" = {QgsExpression.quotedValue(name)}"          # fix 1
    matches = list(countries.getFeatures(expr))
    if len(matches) != 1:                                             # fail loudly
        raise RuntimeError(f"{name!r}: expected 1 country, found {len(matches)}")
    country = matches[0]
    code = country["adm0_a3"]                                         # fix 2
    its_places = list(places.getFeatures(f"\"adm0_a3\" = {QgsExpression.quotedValue(code)}"))
    capitals = [p["name"] for p in its_places if p["featurecla"].startswith("Admin-0 capital")]
    no_province = sum(1 for p in its_places if QgsVariantUtils.isNull(p["adm1name"]))   # fix 3
    results[name] = (len(its_places), capitals, no_province)

for name, (n, caps, missing) in results.items():
    print(f"{name:15} {n:3} places | capital: {', '.join(caps) or '-':25} | no province: {missing}")

assert set(results) == set(wanted), f"countries missing from the results: {set(wanted) - set(results)}"
assert results["France"][:2] == (28, ["Paris"]), f"France: {results['France']}"
assert results["Norway"][:2] == (6, ["Oslo"]), f"Norway: {results['Norway']}"
assert sorted(results["Côte d'Ivoire"][1]) == ["Abidjan", "Yamoussoukro"]
assert results["Antarctica"][2] == 40, f"Antarctica places with no province: {results['Antarctica'][2]}"
print("All checks passed ✔")
