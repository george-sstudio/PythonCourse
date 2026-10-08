"""
MODULE 06 - Exercise 3: batch - rivers and places for 5 countries, one GeoPackage

For each code in CODES, make two layers in output/module06_batch.gpkg:
    <code>_rivers   rivers clipped to the country
    <code>_places   places inside the country
then count everything and compare with what we expect.
"""
from pathlib import Path

import processing
from qgis.core import QgsExpressionContextUtils, QgsProviderRegistry, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
OUT_GPKG = COURSE / "output" / "module06_batch.gpkg"
OUT_GPKG.parent.mkdir(exist_ok=True)
if OUT_GPKG.exists():
    OUT_GPKG.unlink()          # start fresh each run

COUNTRIES = f"{GPKG}|layername=countries"
RIVERS = f"{GPKG}|layername=rivers"
PLACES = f"{GPKG}|layername=places"
CODES = ["AUT", "CHE", "NOR", "PER", "KEN"]


def gpkg_target(table):
    """The OUTPUT string meaning 'layer <table> inside OUT_GPKG'."""
    return f"ogr:dbname='{OUT_GPKG}' table=\"{table}\" (geom)"


counts = {}       # e.g. {"AUT": (rivers, places), ...}
for code in CODES:
    # TODO 1: extract the country: native:extractbyattribute with FIELD "adm0_a3",
    #         OPERATOR 0 (=), VALUE code, OUTPUT TEMPORARY_OUTPUT
    country = None

    # TODO 2: native:clip RIVERS by the country (OVERLAY), OUTPUT gpkg_target(f"{code.lower()}_rivers")
    rivers_path = None

    # TODO 3: native:extractbylocation PLACES, PREDICATE [6] (= are within), INTERSECT country,
    #         OUTPUT gpkg_target(f"{code.lower()}_places")
    places_path = None

    # TODO 4: count features in both outputs (make layers from the paths) and
    #         store counts[code] = (n_rivers, n_places); print a progress line


# --- verify -------------------------------------------------------------------------
layers_made = sorted(s.name() for s in QgsProviderRegistry.instance().querySublayers(str(OUT_GPKG)))
print(layers_made)
print(counts)

# --- Checks (don't edit below this line) ------------------------------------
assert len(layers_made) == 10, f"expected 10 layers, got {layers_made}"
assert counts["NOR"] == (4, 6) and counts["PER"] == (5, 11), f"counts: {counts}"
# Kenya really has no river in this 1:50m dataset: a zero can be a true answer.
# Always ask "is this zero real, or a bug?" and look at the map before deciding.
assert counts["KEN"][0] == 0, f"counts: {counts}"
print("All checks passed ✔")
