"""
MODULE 06 - Exercise 4: a DEM workflow - and the 90-degree slope trap

DEM: data/dem_sample.tif (EPSG:4326, heights in metres)
Results go to output/terrain/
"""
from pathlib import Path

import processing
from qgis.core import QgsExpressionContextUtils, QgsProject, QgsRasterLayer, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DEM = str(COURSE / "data" / "dem_sample.tif")
OUT = COURSE / "output" / "terrain"
OUT.mkdir(parents=True, exist_ok=True)


def raster_stats(path):
    """Mean and max of band 1 of a raster file."""
    s = processing.run("native:rasterlayerstatistics", {"INPUT": path, "BAND": 1})
    return round(s["MEAN"], 1), round(s["MAX"], 1)


# --- Part A: the trap ----------------------------------------------------------------
wrong = processing.run("gdal:slope", {"INPUT": DEM, "BAND": 1,
                                      "OUTPUT": str(OUT / "slope_WRONG.tif")})["OUTPUT"]
print("slope on the EPSG:4326 DEM (mean, max):", raster_stats(wrong))

# --- Part B: do it properly ------------------------------------------------------------
# TODO 1: reproject the DEM with gdal:warpreproject:
#         TARGET_CRS "EPSG:32636", RESAMPLING 1 (bilinear), TARGET_RESOLUTION 90,
#         NODATA -9999, OUTPUT str(OUT / "dem_utm.tif")
dem_utm = None

# TODO 2: gdal:hillshade on dem_utm (BAND 1, Z_FACTOR 1, AZIMUTH 315, ALTITUDE 45)
#         -> OUT / "hillshade.tif"
hillshade = None

# TODO 3: gdal:slope on dem_utm -> OUT / "slope.tif"
slope = None

# TODO 4: gdal:contour on dem_utm, INTERVAL 100, FIELD_NAME "elev"
#         -> OUT / "contours_100m.gpkg"
contours = None

# TODO 5: add hillshade, slope and contours to the project (check isValid first)


slope_mean, slope_max = raster_stats(slope) if slope else (None, None)
contour_layer = QgsVectorLayer(contours, "contours", "ogr") if contours else None
print("slope on the UTM DEM (mean, max):", (slope_mean, slope_max))

# --- Checks (don't edit below this line) ------------------------------------
assert QgsRasterLayer(dem_utm, "d").crs().authid() == "EPSG:32636", "TODO 1"
assert QgsRasterLayer(hillshade, "h").isValid(), "TODO 2"
assert 5 < slope_mean < 9 and slope_max < 70, f"TODO 3: slope looks wrong ({slope_mean}, {slope_max})"
assert contour_layer.featureCount() > 1000, "TODO 4"
elev = contour_layer.fields().indexOf("elev")
assert contour_layer.minimumValue(elev) == -400 and contour_layer.maximumValue(elev) == 1200
print("All checks passed ✔")
