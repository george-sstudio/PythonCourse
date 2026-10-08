"""MODULE 09 - Solution 1: from copy-paste to functions"""
from pathlib import Path

from qgis.core import (QgsExpressionContextUtils, QgsFillSymbol, QgsProject,
                       QgsSingleSymbolRenderer, QgsVectorLayer)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
STYLES = COURSE / "output" / "styles"
STYLES.mkdir(parents=True, exist_ok=True)
project = QgsProject.instance()
project.clear()


def load_layer(name):
    """Load layer `name` from GPKG, check it, add it to the project, return it."""
    layer = QgsVectorLayer(f"{GPKG}|layername={name}", name, "ogr")
    if not layer.isValid():
        raise RuntimeError(f"Could not load {name!r} from {GPKG.name}")
    project.addMapLayer(layer)
    return layer


def style_fill(layer, colour, outline="#ffffff", width=0.1):
    """Give `layer` a single fill symbol. Width is in mm."""
    symbol = QgsFillSymbol.createSimple(
        {"color": colour, "outline_color": outline, "outline_width": str(width)})
    layer.setRenderer(QgsSingleSymbolRenderer(symbol))
    layer.triggerRepaint()


def save_style(layer):
    """Save the layer's style as STYLES/<layer name>.qml; raise if it fails."""
    message, ok = layer.saveNamedStyle(str(STYLES / f"{layer.name()}.qml"))
    if not ok:
        raise RuntimeError(f"{layer.name()}: {message}")


PLAN = [
    ("ocean", "#dfe8ee", "#dfe8ee", 0),
    ("countries", "#f1ede4", "#b8b2a5", 0.15),
    ("admin1", "#f1ede4", "#d6d0c4", 0.1),
    ("lakes", "#dfe8ee", "#8fb0c7", 0.1),
]

for name, fill, outline, width in PLAN:
    layer = load_layer(name)
    style_fill(layer, fill, outline, width)
    save_style(layer)
    print("done:", name)

names = [lyr.name() for lyr in project.mapLayers().values()]
assert sorted(names) == ["admin1", "countries", "lakes", "ocean"], names
assert project.mapLayersByName("countries")[0].renderer().symbol().color().name() == "#f1ede4"
assert all((STYLES / f"{n}.qml").exists() for n in names)
try:
    load_layer("glaciers")
    raise AssertionError("load_layer should raise for a layer that doesn't exist")
except RuntimeError:
    pass
print("All checks passed ✔")
