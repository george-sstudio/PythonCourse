"""
MODULE 07 - Exercise 4: terrain styling (uses the outputs of Module 06, ex06_4)

Build a small terrain project:
  top     Contours 100 m   rule-based: index contours (elev % 500 = 0) 0.35 mm,
                           others 0.12 mm, colour #6e5a46; labels on index contours only
          Hillshade         multiply, opacity 0.55
  bottom  Elevation         pseudocolour ramp with the stops below
Save each style as QML and the project as output/terrain/terrain.qgz
"""
from pathlib import Path

from qgis.core import (Qgis, QgsColorRampShader, QgsExpressionContextUtils, QgsLineSymbol,
                       QgsPalLayerSettings, QgsProject, QgsRasterLayer, QgsRasterShader,
                       QgsRuleBasedLabeling, QgsRuleBasedRenderer,
                       QgsSingleBandPseudoColorRenderer, QgsTextBufferSettings,
                       QgsTextFormat, QgsVectorLayer)
from qgis.PyQt.QtGui import QColor, QPainter

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
TERRAIN = COURSE / "output" / "terrain"
if not (TERRAIN / "dem_utm.tif").exists():
    raise RuntimeError("Run Module 06 exercise 4 (ex06_4_terrain.py) first")

project = QgsProject.instance()
project.clear()

dem = QgsRasterLayer(str(TERRAIN / "dem_utm.tif"), "Elevation")
hillshade = QgsRasterLayer(str(TERRAIN / "hillshade.tif"), "Hillshade")
contours = QgsVectorLayer(str(TERRAIN / "contours_100m.gpkg"), "Contours 100 m", "ogr")
for layer in [dem, hillshade, contours]:          # bottom first
    if not layer.isValid():
        raise RuntimeError(layer.name())
    project.addMapLayer(layer)
project.setCrs(dem.crs())

STOPS = [(-430, "#8fb3c9"), (-200, "#9dbfae"), (0, "#a9c59a"), (300, "#d8d8a8"),
         (600, "#d4bb8c"), (900, "#b9977a"), (1300, "#f2eee6")]

# TODO 1: pseudocolour renderer for dem from STOPS (Interpolated ramp)


# TODO 2: hillshade blend mode Multiply, opacity 0.55


# TODO 3: contours - rule-based renderer with two rules:
#         "Index (500 m)"  filter  "elev" % 500 = 0   width 0.35
#         "Contour"        elseRule                   width 0.12
#         both colour #6e5a46


# TODO 4: labels on index contours only: field "elev", 6 pt, colour #6e5a46,
#         buffer 0.5 mm in #f2eee6, placement Qgis.LabelPlacement.Curved


# TODO 5: save the three QMLs into TERRAIN and the project as TERRAIN / "terrain.qgz"


# --- Checks (don't edit below this line) ------------------------------------
shader = dem.renderer().shader().rasterShaderFunction()
assert len(shader.colorRampItemList()) == 7, "TODO 1"
assert hillshade.blendMode() == QPainter.CompositionMode.CompositionMode_Multiply, "TODO 2"
assert abs(hillshade.opacity() - 0.55) < 1e-9, "TODO 2"
rules = contours.renderer().rootRule().children()
assert len(rules) == 2 and rules[1].isElse(), "TODO 3"
assert contours.labelsEnabled(), "TODO 4"
assert (TERRAIN / "terrain.qgz").exists(), "TODO 5"
print("All checks passed ✔")
