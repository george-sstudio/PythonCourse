"""MODULE 06 - Solution 4: a DEM workflow - and the 90-degree slope trap"""
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


# Part A - heights in metres, pixel sizes in degrees -> nonsense slopes
wrong = processing.run("gdal:slope", {"INPUT": DEM, "BAND": 1,
                                      "OUTPUT": str(OUT / "slope_WRONG.tif")})["OUTPUT"]
print("slope on the EPSG:4326 DEM (mean, max):", raster_stats(wrong))

# Part B
dem_utm = processing.run("gdal:warpreproject", {
    "INPUT": DEM, "TARGET_CRS": "EPSG:32636", "RESAMPLING": 1,
    "TARGET_RESOLUTION": 90, "NODATA": -9999,
    "OUTPUT": str(OUT / "dem_utm.tif")})["OUTPUT"]

hillshade = processing.run("gdal:hillshade", {
    "INPUT": dem_utm, "BAND": 1, "Z_FACTOR": 1, "AZIMUTH": 315, "ALTITUDE": 45,
    "OUTPUT": str(OUT / "hillshade.tif")})["OUTPUT"]

slope = processing.run("gdal:slope", {
    "INPUT": dem_utm, "BAND": 1, "OUTPUT": str(OUT / "slope.tif")})["OUTPUT"]

contours = processing.run("gdal:contour", {
    "INPUT": dem_utm, "BAND": 1, "INTERVAL": 100, "FIELD_NAME": "elev",
    "OUTPUT": str(OUT / "contours_100m.gpkg")})["OUTPUT"]

project = QgsProject.instance()
for layer in [QgsRasterLayer(hillshade, "Hillshade"),
              QgsRasterLayer(slope, "Slope (degrees)"),
              QgsVectorLayer(contours, "Contours 100 m", "ogr")]:
    if not layer.isValid():
        raise RuntimeError(f"{layer.name()} did not load")
    project.addMapLayer(layer)

slope_mean, slope_max = raster_stats(slope)
contour_layer = QgsVectorLayer(contours, "contours", "ogr")
print("slope on the UTM DEM (mean, max):", (slope_mean, slope_max))
print("contour lines:", contour_layer.featureCount())

assert QgsRasterLayer(dem_utm, "d").crs().authid() == "EPSG:32636", "TODO 1"
assert QgsRasterLayer(hillshade, "h").isValid(), "TODO 2"
assert 5 < slope_mean < 9 and slope_max < 70, f"TODO 3: slope looks wrong ({slope_mean}, {slope_max})"
assert contour_layer.featureCount() > 1000, "TODO 4"
elev = contour_layer.fields().indexOf("elev")
assert contour_layer.minimumValue(elev) == -400 and contour_layer.maximumValue(elev) == 1200
print("All checks passed ✔")
