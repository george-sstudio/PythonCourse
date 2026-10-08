"""MODULE 09 - Solution: test the safe buffer tool from code (before installing it)"""
import importlib.util
from pathlib import Path

import processing
from qgis.core import QgsDistanceArea, QgsExpressionContextUtils, QgsProject, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
TOOL_FILE = Path(__file__).resolve().parent / "safe_buffer_tool.py"   # this folder

# load the tool file as a module (like `import`, but from any path)
spec = importlib.util.spec_from_file_location("safe_buffer_tool", TOOL_FILE)
tool_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool_module)
alg = tool_module.SafeBufferAlgorithm().create()   # create() also runs initAlgorithm()

# processing.run accepts an algorithm OBJECT as well as an id
lena = processing.run("native:extractbyexpression", {
    "INPUT": f"{GPKG}|layername=rivers", "EXPRESSION": "\"name\" = 'Lena'",
    "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
zone = processing.run(alg, {"INPUT": lena, "DISTANCE": 10_000, "DISSOLVE": True,
                            "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]

places = processing.run("native:extractbylocation", {
    "INPUT": f"{GPKG}|layername=places", "PREDICATE": [0], "INTERSECT": zone,
    "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
names = sorted(f["name"] for f in places.getFeatures())
print("Places within 10 km of the Lena:", names)

# area check: a 10 km buffer around a line of length L is about 2 * 10 km * L
da = QgsDistanceArea()
da.setSourceCrs(lena.crs(), QgsProject.instance().transformContext())
da.setEllipsoid("EPSG:7030")
length_km = sum(da.measureLength(f.geometry()) for f in lena.getFeatures()) / 1000
area_km2 = sum(da.measureArea(f.geometry()) for f in zone.getFeatures()) / 1e6
print(f"river {length_km:,.0f} km, buffer {area_km2:,.0f} km2, "
      f"expected about {2 * 10 * length_km:,.0f} km2")

assert zone.crs().authid() == "EPSG:4326", "the result comes back in the input CRS"
assert names == ["Lensk", "Yakutsk", "Zhigansk"], names
assert 0.9 < area_km2 / (2 * 10 * length_km) < 1.1, "buffer area should be ~2 x d x length"
print("All checks passed ✔")
