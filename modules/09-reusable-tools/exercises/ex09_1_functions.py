"""
MODULE 09 - Exercise 1: from copy-paste to functions

The BEFORE block below (commented out) is typical first-draft code: the same
five lines copied four times. Rewrite it as three small functions, then use
them in a loop. Same result, a quarter of the code, one place to fix things.
"""
from pathlib import Path

from qgis.core import (QgsExpressionContextUtils, QgsFillSymbol, QgsProject,
                       QgsSingleSymbolRenderer, QgsVectorLayer)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
STYLES = COURSE / "output" / "styles"
STYLES.mkdir(parents=True, exist_ok=True)
project = QgsProject.instance()
project.clear()

# ---- BEFORE (don't run - read) -------------------------------------------------
# ocean = QgsVectorLayer(f"{GPKG}|layername=ocean", "ocean", "ogr")
# ocean.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
#     {"color": "#dfe8ee", "outline_color": "#dfe8ee", "outline_width": "0"})))
# project.addMapLayer(ocean)
# ocean.saveNamedStyle(str(STYLES / "ocean.qml"))
# countries = QgsVectorLayer(f"{GPKG}|layername=countries", "countries", "ogr")
# countries.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
#     {"color": "#f1ede4", "outline_color": "#b8b2a5", "outline_width": "0.15"})))
# project.addMapLayer(countries)
# countries.saveNamedStyle(str(STYLES / "countries.qml"))
# ... and the same again for lakes and admin1


# ---- AFTER: your functions ----------------------------------------------------------
def load_layer(name):
    """Load layer `name` from GPKG, check it is valid (raise if not), add it to
    the project and return it."""
    pass  # TODO


def style_fill(layer, colour, outline="#ffffff", width=0.1):
    """Give `layer` a single fill symbol. Width is in mm."""
    pass  # TODO  (hint: the dictionary values must be text: str(width))


def save_style(layer):
    """Save the layer's style as STYLES/<layer name>.qml; raise if it fails."""
    pass  # TODO


PLAN = [  # (layer, fill, outline, width)
    ("ocean", "#dfe8ee", "#dfe8ee", 0),
    ("countries", "#f1ede4", "#b8b2a5", 0.15),
    ("admin1", "#f1ede4", "#d6d0c4", 0.1),
    ("lakes", "#dfe8ee", "#8fb0c7", 0.1),
]

# TODO: one loop over PLAN that calls your three functions


# --- Checks (don't edit below this line) ------------------------------------
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
