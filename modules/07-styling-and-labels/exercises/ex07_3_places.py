"""
MODULE 07 - Exercise 3: places - rules, proportional circles, labels

Style the places layer like this:
  * rule "Capital"  : featurecla LIKE 'Admin-0 capital%' -> square, #b03a2e, 2.0 mm
  * rule "Other"    : everything else (elseRule)         -> circle, #444444,
                      SIZE DATA-DEFINED: scale_linear(sqrt("pop_max"), 0, 6000, 0.8, 4)
  * labels only for capitals: field "name", 7 pt, colour #222222,
    white buffer 0.6 mm, placement AroundPoint
Save to output/styles/places.qml
"""
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

# --- 1. symbols --------------------------------------------------------------------------
capital_symbol = QgsMarkerSymbol.createSimple({"name": "square", "color": "#b03a2e",
                                               "size": "2.0", "outline_color": "#ffffff"})
# TODO 1: other_symbol: a circle, #444444, white outline; then make its size
#         data-defined (symbolLayer(0).setDataDefinedProperty(QgsSymbolLayer.Property.Size,
#         QgsProperty.fromExpression(...)))
other_symbol = None

# --- 2. rule-based renderer ------------------------------------------------------------
# TODO 2: root = QgsRuleBasedRenderer.Rule(None); append a "Capital" rule
#         (filterExp=CAPITAL) and an "Other" rule (elseRule=True); set the renderer


# --- 3. labels for capitals only ------------------------------------------------------
# TODO 3: QgsTextFormat (size 7, colour) + QgsTextBufferSettings (enabled, 0.6, white),
#         QgsPalLayerSettings (fieldName "name", placement Qgis.LabelPlacement.AroundPoint),
#         wrapped in a QgsRuleBasedLabeling rule with filter CAPITAL.
#         Don't forget places.setLabelsEnabled(True)


# --- 4. save -----------------------------------------------------------------------------
# TODO 4: save to STYLES / "places.qml"


# --- Checks (don't edit below this line) ------------------------------------
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
