"""MODULE 07 - Solution 3: places - rules, proportional circles, labels"""
from pathlib import Path

from qgis.core import (Qgis, QgsExpressionContextUtils, QgsMarkerSymbol, QgsPalLayerSettings,
                       QgsProject, QgsProperty, QgsRuleBasedLabeling, QgsRuleBasedRenderer,
                       QgsSymbolLayer, QgsTextBufferSettings, QgsTextFormat, QgsVectorLayer)
from qgis.PyQt.QtGui import QColor

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
STYLES = COURSE / "output" / "styles"
STYLES.mkdir(parents=True, exist_ok=True)

places = QgsVectorLayer(f"{GPKG}|layername=places", "places", "ogr")
QgsProject.instance().addMapLayer(places)
CAPITAL = "\"featurecla\" LIKE 'Admin-0 capital%'"

# 1. symbols
capital_symbol = QgsMarkerSymbol.createSimple({"name": "square", "color": "#b03a2e",
                                               "size": "2.0", "outline_color": "#ffffff"})
other_symbol = QgsMarkerSymbol.createSimple({"name": "circle", "color": "#444444",
                                             "outline_color": "#ffffff", "outline_width": "0.1"})
other_symbol.symbolLayer(0).setDataDefinedProperty(
    QgsSymbolLayer.Property.Size,
    QgsProperty.fromExpression('scale_linear(sqrt("pop_max"), 0, 6000, 0.8, 4)'))

# 2. rules
root = QgsRuleBasedRenderer.Rule(None)
root.appendChild(QgsRuleBasedRenderer.Rule(capital_symbol, filterExp=CAPITAL, label="Capital"))
root.appendChild(QgsRuleBasedRenderer.Rule(other_symbol, elseRule=True, label="Other"))
places.setRenderer(QgsRuleBasedRenderer(root))

# 3. labels
fmt = QgsTextFormat()
fmt.setSize(7)
fmt.setColor(QColor("#222222"))
buffer = QgsTextBufferSettings()
buffer.setEnabled(True)
buffer.setSize(0.6)
buffer.setColor(QColor("#ffffff"))
fmt.setBuffer(buffer)

settings = QgsPalLayerSettings()
settings.fieldName = "name"
settings.placement = Qgis.LabelPlacement.AroundPoint
settings.setFormat(fmt)

label_rule = QgsRuleBasedLabeling.Rule(settings)
label_rule.setFilterExpression(CAPITAL)
label_root = QgsRuleBasedLabeling.Rule(None)
label_root.appendChild(label_rule)
places.setLabeling(QgsRuleBasedLabeling(label_root))
places.setLabelsEnabled(True)
places.triggerRepaint()

# 4. save
message, ok = places.saveNamedStyle(str(STYLES / "places.qml"))
if not ok:
    raise RuntimeError(message)

rules = places.renderer().rootRule().children()
assert [r.label() for r in rules] == ["Capital", "Other"], "TODO 2"
assert rules[1].isElse(), "TODO 2: the second rule should be the else-rule"
size_prop = rules[1].symbol().symbolLayer(0).dataDefinedProperties().property(QgsSymbolLayer.Property.Size)
assert size_prop.isActive() and "sqrt" in size_prop.expressionString(), "TODO 1"
assert places.labelsEnabled(), "TODO 3: enable labels"
labeling = places.labeling()
first_rule = labeling.rootRule().children()[0]
assert "Admin-0 capital" in first_rule.filterExpression(), "TODO 3: capitals only"
label_format = QgsPalLayerSettings(first_rule.settings()).format()
assert label_format.buffer().enabled(), "TODO 3: buffer"
assert (STYLES / "places.qml").exists(), "TODO 4"
print("All checks passed ✔")
