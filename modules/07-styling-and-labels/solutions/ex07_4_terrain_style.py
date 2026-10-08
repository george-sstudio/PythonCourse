"""MODULE 07 - Solution 4: terrain styling (uses the outputs of Module 06, ex06_4)"""
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
for layer in [dem, hillshade, contours]:
    if not layer.isValid():
        raise RuntimeError(layer.name())
    project.addMapLayer(layer)
project.setCrs(dem.crs())

STOPS = [(-430, "#8fb3c9"), (-200, "#9dbfae"), (0, "#a9c59a"), (300, "#d8d8a8"),
         (600, "#d4bb8c"), (900, "#b9977a"), (1300, "#f2eee6")]

# 1. hypsometric tints
ramp = QgsColorRampShader()
ramp.setColorRampType(QgsColorRampShader.Type.Interpolated)
ramp.setColorRampItemList([QgsColorRampShader.ColorRampItem(v, QColor(c), f"{v} m")
                           for v, c in STOPS])
shader = QgsRasterShader()
shader.setRasterShaderFunction(ramp)
dem.setRenderer(QgsSingleBandPseudoColorRenderer(dem.dataProvider(), 1, shader))

# 2. hillshade as "ink"
hillshade.setBlendMode(QPainter.CompositionMode.CompositionMode_Multiply)
hillshade.setOpacity(0.55)

# 3. contours: index vs ordinary
INDEX = '"elev" % 500 = 0'
root = QgsRuleBasedRenderer.Rule(None)
root.appendChild(QgsRuleBasedRenderer.Rule(
    QgsLineSymbol.createSimple({"color": "#6e5a46", "width": "0.35"}),
    filterExp=INDEX, label="Index (500 m)"))
root.appendChild(QgsRuleBasedRenderer.Rule(
    QgsLineSymbol.createSimple({"color": "#6e5a46", "width": "0.12"}),
    elseRule=True, label="Contour"))
contours.setRenderer(QgsRuleBasedRenderer(root))

# 4. labels along index contours
fmt = QgsTextFormat()
fmt.setSize(6)
fmt.setColor(QColor("#6e5a46"))
buffer = QgsTextBufferSettings()
buffer.setEnabled(True)
buffer.setSize(0.5)
buffer.setColor(QColor("#f2eee6"))
fmt.setBuffer(buffer)
settings = QgsPalLayerSettings()
settings.fieldName = "elev"
settings.placement = Qgis.LabelPlacement.Curved
settings.setFormat(fmt)
label_rule = QgsRuleBasedLabeling.Rule(settings)
label_rule.setFilterExpression(INDEX)
label_root = QgsRuleBasedLabeling.Rule(None)
label_root.appendChild(label_rule)
contours.setLabeling(QgsRuleBasedLabeling(label_root))
contours.setLabelsEnabled(True)

# 5. save styles + project
for layer, file_name in [(dem, "elevation.qml"), (hillshade, "hillshade.qml"),
                         (contours, "contours.qml")]:
    message, ok = layer.saveNamedStyle(str(TERRAIN / file_name))
    if not ok:
        raise RuntimeError(message)
if not project.write(str(TERRAIN / "terrain.qgz")):
    raise RuntimeError("project not saved")
print("Saved terrain.qgz - open it in QGIS to look at the result")

shader = dem.renderer().shader().rasterShaderFunction()
assert len(shader.colorRampItemList()) == 7, "TODO 1"
assert hillshade.blendMode() == QPainter.CompositionMode.CompositionMode_Multiply, "TODO 2"
assert abs(hillshade.opacity() - 0.55) < 1e-9, "TODO 2"
rules = contours.renderer().rootRule().children()
assert len(rules) == 2 and rules[1].isElse(), "TODO 3"
assert contours.labelsEnabled(), "TODO 4"
assert (TERRAIN / "terrain.qgz").exists(), "TODO 5"
print("All checks passed ✔")
