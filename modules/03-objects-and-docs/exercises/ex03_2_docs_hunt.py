"""
MODULE 03 - Exercise 2: docs hunt

You have NOT been taught these methods. Find them yourself with
  dir(obj), help(obj.method), autocomplete, or qgis.org/pyqgis/3.40/
Write down HOW you found each one in the comment - that's the real skill.
"""
from pathlib import Path

from qgis.core import QgsExpressionContextUtils, QgsRasterLayer, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA = COURSE / "data"

dem = QgsRasterLayer(str(DATA / "dem_sample.tif"), "dem")
places = QgsVectorLayer(f"{DATA / 'natural_earth.gpkg'}|layername=places", "places", "ogr")

# TODO 1: how many BANDS does the dem raster have?      (found by: ...)
band_count = None

# TODO 2: the raster's width in pixels                    (found by: ...)
width = None

# TODO 3: the size of one pixel in map units (x direction) (found by: ...)
#         hint: search dir(dem) for "units"
pixel_x = None

# TODO 4: the provider type of the places layer, e.g. "ogr" (found by: ...)
provider = None

# TODO 5: is the places layer currently in editing mode? (True/False)
#         (found by: ...)   hint: search for "edit"
editing = None

# TODO 6: the index (position) of the field "pop_max" in places.fields()
#         (found by: ...)   hint: help(places.fields().indexOf)
pop_index = None

print(band_count, width, pixel_x, provider, editing, pop_index)

# --- Checks (don't edit below this line) ------------------------------------
assert band_count == 1
assert width == 1200
assert abs(pixel_x - 1 / 1200) < 1e-12, f"TODO 3: got {pixel_x} (degrees!)"
assert provider == "ogr"
assert editing is False
assert pop_index == 8, f"TODO 6: got {pop_index}"
print("All checks passed ✔")
