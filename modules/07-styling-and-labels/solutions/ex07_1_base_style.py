"""MODULE 07 - Solution 1: a quiet base map, saved as QML files"""
from pathlib import Path

from qgis.core import (QgsExpressionContextUtils, QgsFillSymbol, QgsLineSymbol,
                       QgsProject, QgsSingleSymbolRenderer, QgsVectorLayer)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
STYLES = COURSE / "output" / "styles"
STYLES.mkdir(parents=True, exist_ok=True)

project = QgsProject.instance()
project.clear()

layers = {}
for name in ["rivers", "lakes", "countries", "ocean"]:
    lyr = QgsVectorLayer(f"{GPKG}|layername={name}", name, "ogr")
    if not lyr.isValid():
        raise RuntimeError(name)
    layers[name] = lyr

for name in ["ocean", "countries", "lakes", "rivers"]:
    project.addMapLayer(layers[name])

# 1-4: one symbol per layer
symbols = {
    "ocean": QgsFillSymbol.createSimple({"color": "#dfe8ee", "outline_style": "no"}),
    "countries": QgsFillSymbol.createSimple({"color": "#f1ede4", "outline_color": "#b8b2a5",
                                             "outline_width": "0.15"}),
    "lakes": QgsFillSymbol.createSimple({"color": "#dfe8ee", "outline_color": "#8fb0c7",
                                         "outline_width": "0.1"}),
    "rivers": QgsLineSymbol.createSimple({"color": "#8fb0c7", "width": "0.25",
                                          "capstyle": "round"}),
}
for name, symbol in symbols.items():
    layers[name].setRenderer(QgsSingleSymbolRenderer(symbol))
    layers[name].triggerRepaint()

# 5: save - and check
for name, lyr in layers.items():
    message, ok = lyr.saveNamedStyle(str(STYLES / f"{name}.qml"))
    if not ok:
        raise RuntimeError(f"{name}: {message}")
    print("saved", name)


def colour(name):
    return layers[name].renderer().symbol().color().name()

assert colour("ocean") == "#dfe8ee"
assert colour("countries") == "#f1ede4"
assert layers["countries"].renderer().symbol().symbolLayer(0).strokeWidth() == 0.15
assert layers["rivers"].renderer().symbol().width() == 0.25
for name in layers:
    qml = STYLES / f"{name}.qml"
    assert qml.exists(), f"missing {qml.name}"
assert 'value="#8fb0c7' in (STYLES / "rivers.qml").read_text() or "143,176,199" in (STYLES / "rivers.qml").read_text()
print("All checks passed ✔")
