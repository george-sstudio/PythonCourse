"""
MODULE 06 - Exercise 2: "cities along a river" - the book's way vs the right way

The book buffers in DEGREES. Write one function that does it in METRES,
then compare both methods on the Amazon (equator) and the Lena (Siberia).
"""
from pathlib import Path

import processing
from qgis.core import QgsExpression, QgsExpressionContextUtils

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
RIVERS = f"{GPKG}|layername=rivers"
PLACES = f"{GPKG}|layername=places"


def extract_river(name):
    expr = f"\"name\" = {QgsExpression.quotedValue(name)}"
    return processing.run("native:extractbyexpression", {
        "INPUT": RIVERS, "EXPRESSION": expr, "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]


def places_near_degrees(river_name, degrees):
    """The book's method (buffer in degrees). Kept as it is - don't fix this one."""
    river = extract_river(river_name)
    zone = processing.run("native:buffer", {
        "INPUT": river, "DISTANCE": degrees, "DISSOLVE": True,
        "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
    near = processing.run("native:extractbylocation", {
        "INPUT": PLACES, "PREDICATE": [0], "INTERSECT": zone,
        "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
    return sorted(f["name"] for f in near.getFeatures())


def places_near_metres(river_name, metres, crs):
    """The right way: reproject the river to `crs` (in metres), buffer, extract."""
    river = extract_river(river_name)
    # TODO: 1. native:reprojectlayer  (INPUT river, TARGET_CRS crs)
    #       2. native:buffer          (DISTANCE metres, DISSOLVE True)
    #       3. native:extractbylocation (INPUT PLACES, PREDICATE [0], INTERSECT zone)
    #       4. return the sorted list of names (like the function above)
    return []


amazon_deg = places_near_degrees("Amazonas", 0.1)
amazon_m = places_near_metres("Amazonas", 10_000, "EPSG:5880")   # SIRGAS 2000 / Brazil Polyconic
lena_deg = places_near_degrees("Lena", 0.1)
lena_m = places_near_metres("Lena", 10_000, "ESRI:102027")       # Asia North Lambert Conformal Conic

print("Amazon  degrees:", amazon_deg)
print("Amazon  metres :", amazon_m)
print("Lena    degrees:", lena_deg)
print("Lena    metres :", lena_m)

# TODO: in a comment, explain in your own words why the two methods agree on
#       the Amazon but not on the Lena.
#

# --- Checks (don't edit below this line) ------------------------------------
assert amazon_deg == ["Iquitos", "Leticia", "Santarém"]
assert amazon_m == ["Iquitos", "Leticia", "Santarém"], f"Amazon metres: {amazon_m}"
assert lena_deg == ["Lensk"]
assert lena_m == ["Lensk", "Yakutsk", "Zhigansk"], f"Lena metres: {lena_m}"
print("All checks passed ✔")
