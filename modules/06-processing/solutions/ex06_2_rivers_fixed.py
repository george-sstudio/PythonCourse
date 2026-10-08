"""MODULE 06 - Solution 2: "cities along a river" - the book's way vs the right way"""
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
    """The book's method (buffer in degrees)."""
    river = extract_river(river_name)
    zone = processing.run("native:buffer", {
        "INPUT": river, "DISTANCE": degrees, "DISSOLVE": True,
        "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
    near = processing.run("native:extractbylocation", {
        "INPUT": PLACES, "PREDICATE": [0], "INTERSECT": zone,
        "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
    return sorted(f["name"] for f in near.getFeatures())


def places_near_metres(river_name, metres, crs):
    """Reproject the river to a metric CRS, buffer in metres, extract places."""
    river = extract_river(river_name)
    river_m = processing.run("native:reprojectlayer", {
        "INPUT": river, "TARGET_CRS": crs, "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
    zone = processing.run("native:buffer", {
        "INPUT": river_m, "DISTANCE": metres, "SEGMENTS": 8, "DISSOLVE": True,
        "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
    near = processing.run("native:extractbylocation", {
        "INPUT": PLACES, "PREDICATE": [0], "INTERSECT": zone,
        "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]     # places (EPSG:4326) vs zone: reprojected on the fly
    return sorted(f["name"] for f in near.getFeatures())


amazon_deg = places_near_degrees("Amazonas", 0.1)
amazon_m = places_near_metres("Amazonas", 10_000, "EPSG:5880")
lena_deg = places_near_degrees("Lena", 0.1)
lena_m = places_near_metres("Lena", 10_000, "ESRI:102027")

print("Amazon  degrees:", amazon_deg)
print("Amazon  metres :", amazon_m)
print("Lena    degrees:", lena_deg)
print("Lena    metres :", lena_m)

# Near the equator 0.1 degree is ~11 km both north-south and east-west, so a
# 0.1-degree buffer is close to a 10 km buffer. At 60-70 degrees N a degree of
# longitude is only ~38-55 km, so 0.1 degree east-west is just 4-5 km: the
# buffer is squashed and misses Yakutsk and Zhigansk, which lie east/west of
# the river line.

assert amazon_deg == ["Iquitos", "Leticia", "Santarém"]
assert amazon_m == ["Iquitos", "Leticia", "Santarém"], f"Amazon metres: {amazon_m}"
assert lena_deg == ["Lensk"]
assert lena_m == ["Lensk", "Yakutsk", "Zhigansk"], f"Lena metres: {lena_m}"
print("All checks passed ✔")
