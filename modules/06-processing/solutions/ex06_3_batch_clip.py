"""MODULE 06 - Solution 3: batch - rivers and places for 5 countries, one GeoPackage"""
from pathlib import Path

import processing
from qgis.core import QgsExpressionContextUtils, QgsProviderRegistry, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
OUT_GPKG = COURSE / "output" / "module06_batch.gpkg"
OUT_GPKG.parent.mkdir(exist_ok=True)
if OUT_GPKG.exists():
    OUT_GPKG.unlink()

COUNTRIES = f"{GPKG}|layername=countries"
RIVERS = f"{GPKG}|layername=rivers"
PLACES = f"{GPKG}|layername=places"
CODES = ["AUT", "CHE", "NOR", "PER", "KEN"]


def gpkg_target(table):
    """The OUTPUT string meaning 'layer <table> inside OUT_GPKG'."""
    return f"ogr:dbname='{OUT_GPKG}' table=\"{table}\" (geom)"


counts = {}
for code in CODES:
    country = processing.run("native:extractbyattribute", {
        "INPUT": COUNTRIES, "FIELD": "adm0_a3", "OPERATOR": 0, "VALUE": code,
        "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
    if country.featureCount() != 1:
        raise RuntimeError(f"{code}: expected 1 country, got {country.featureCount()}")

    rivers_path = processing.run("native:clip", {
        "INPUT": RIVERS, "OVERLAY": country,
        "OUTPUT": gpkg_target(f"{code.lower()}_rivers")})["OUTPUT"]

    places_path = processing.run("native:extractbylocation", {
        "INPUT": PLACES, "PREDICATE": [6], "INTERSECT": country,     # 6 = are within
        "OUTPUT": gpkg_target(f"{code.lower()}_places")})["OUTPUT"]

    n_rivers = QgsVectorLayer(rivers_path, "r", "ogr").featureCount()
    n_places = QgsVectorLayer(places_path, "p", "ogr").featureCount()
    counts[code] = (n_rivers, n_places)
    print(f"{code}: {n_rivers} river parts, {n_places} places")

layers_made = sorted(s.name() for s in QgsProviderRegistry.instance().querySublayers(str(OUT_GPKG)))
print(layers_made)
print(counts)

assert len(layers_made) == 10, f"expected 10 layers, got {layers_made}"
assert counts["NOR"] == (4, 6) and counts["PER"] == (5, 11), f"counts: {counts}"
# Kenya really has no river in this 1:50m dataset: a zero can be a true answer.
# Always ask "is this zero real, or a bug?" and look at the map before deciding.
assert counts["KEN"][0] == 0, f"counts: {counts}"
print("All checks passed ✔")
