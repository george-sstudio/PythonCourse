"""MODULE 03 - Solution 2: docs hunt"""
from pathlib import Path

from qgis.core import QgsExpressionContextUtils, QgsRasterLayer, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA = COURSE / "data"

dem = QgsRasterLayer(str(DATA / "dem_sample.tif"), "dem")
places = QgsVectorLayer(f"{DATA / 'natural_earth.gpkg'}|layername=places", "places", "ogr")

band_count = dem.bandCount()                # dir(dem) -> filter "band"
width = dem.width()                         # autocomplete on dem.w...
pixel_x = dem.rasterUnitsPerPixelX()        # [m for m in dir(dem) if "units" in m.lower()]
provider = places.providerType()            # filter "provider"
editing = places.isEditable()               # filter "edit"
pop_index = places.fields().indexOf("pop_max")   # help(places.fields().indexOf)

print(band_count, width, pixel_x, provider, editing, pop_index)
# pixel_x is 0.000833... DEGREES (EPSG:4326), about 90 m on the ground.
# Units always depend on the CRS - Module 04.

assert band_count == 1
assert width == 1200
assert abs(pixel_x - 1 / 1200) < 1e-12, f"TODO 3: got {pixel_x} (degrees!)"
assert provider == "ogr"
assert editing is False
assert pop_index == 8, f"TODO 6: got {pop_index}"
print("All checks passed ✔")
