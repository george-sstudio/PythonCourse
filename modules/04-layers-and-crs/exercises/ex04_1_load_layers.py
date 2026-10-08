"""
MODULE 04 - Exercise 1: build a tidy project by code

Goal (Layers panel, top to bottom):
    Reference            <- group
        places
        rivers
        graticule_10     <- unticked (hidden)
    Base map             <- group
        lakes
        countries
        World relief     <- the raster (world_shaded_relief.tif)
"""
from pathlib import Path

from qgis.core import (QgsExpressionContextUtils, QgsProject, QgsProviderRegistry,
                       QgsRasterLayer, QgsVectorLayer)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA = COURSE / "data"
GPKG = DATA / "natural_earth.gpkg"

project = QgsProject.instance()
project.clear()                      # start from an empty project
root = project.layerTreeRoot()

# --- 1. what's in the GeoPackage? ---------------------------------------------
# TODO: make a list of the layer names inside GPKG
#       (QgsProviderRegistry.instance().querySublayers(str(GPKG)), then .name())
available = []
print("In the GeoPackage:", available)


# --- 2. a helper to load one GeoPackage layer -------------------------------------
def load_gpkg_layer(layer_name):
    """Return a valid QgsVectorLayer for one layer of GPKG, or raise."""
    # TODO: build the URI  f"{GPKG}|layername={layer_name}" , create the
    #       layer with display name = layer_name, check isValid(), raise a
    #       RuntimeError if not, else return it
    pass


# --- 3. groups ------------------------------------------------------------------
reference = root.addGroup("Reference")
base = root.addGroup("Base map")      # added after -> sits BELOW Reference

# --- 4. load and place the layers -------------------------------------------------
# TODO: for each name in ["places", "rivers", "graticule_10"] (in that order):
#           load it, project.addMapLayer(layer, False), reference.addLayer(layer)


# TODO: the same for ["lakes", "countries"] into base


# TODO: load the raster DATA / "world_shaded_relief.tif" as "World relief",
#       check it's valid, add it (False) and put it in base


# --- 5. hide the graticule ------------------------------------------------------
# TODO: find the graticule layer (project.mapLayersByName(...)[0]), then
#       root.findLayer(layer.id()).setItemVisibilityChecked(False)


# --- Checks (don't edit below this line) ------------------------------------
def panel_order(group):
    return [child.name() for child in group.children()]

print("Reference:", panel_order(reference))
print("Base map :", panel_order(base))
assert len(available) == 9, f"step 1: expected 9 layers, got {available}"
assert panel_order(root) == ["Reference", "Base map"]
assert panel_order(reference) == ["places", "rivers", "graticule_10"]
assert panel_order(base) == ["lakes", "countries", "World relief"]
grat = project.mapLayersByName("graticule_10")[0]
assert not root.findLayer(grat.id()).isVisible(), "step 5: graticule should be hidden"
print("All checks passed ✔")
