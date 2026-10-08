"""
MODULE 07 - Exercise 1: a quiet base map, saved as QML files

Layers (top to bottom): rivers, lakes, countries, ocean.
Palette (use exactly these):
    ocean      fill  #dfe8ee, no outline
    countries  fill  #f1ede4, outline #b8b2a5, 0.15 mm
    lakes      fill  #dfe8ee, outline #8fb0c7, 0.1 mm
    rivers     line  #8fb0c7, 0.25 mm, round caps
Then save each style to output/styles/<layer>.qml
"""
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
for name in ["rivers", "lakes", "countries", "ocean"]:      # top first
    lyr = QgsVectorLayer(f"{GPKG}|layername={name}", name, "ogr")
    if not lyr.isValid():
        raise RuntimeError(name)
    layers[name] = lyr

# addMapLayer puts each new layer on TOP, so add them bottom-first
for name in ["ocean", "countries", "lakes", "rivers"]:
    project.addMapLayer(layers[name])

# TODO 1: ocean - QgsFillSymbol.createSimple({...}) with "outline_style": "no"
#         then layers["ocean"].setRenderer(QgsSingleSymbolRenderer(symbol))


# TODO 2: countries


# TODO 3: lakes


# TODO 4: rivers - QgsLineSymbol.createSimple({"color": ..., "width": ..., "capstyle": "round"})


# TODO 5: save each layer's style to STYLES / f"{name}.qml" and check ok is True


# --- Checks (don't edit below this line) ------------------------------------
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
