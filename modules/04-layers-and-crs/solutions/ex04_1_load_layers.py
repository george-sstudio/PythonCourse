"""MODULE 04 - Solution 1: build a tidy project by code"""
from pathlib import Path

from qgis.core import (QgsExpressionContextUtils, QgsProject, QgsProviderRegistry,
                       QgsRasterLayer, QgsVectorLayer)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA = COURSE / "data"
GPKG = DATA / "natural_earth.gpkg"

project = QgsProject.instance()
project.clear()
root = project.layerTreeRoot()

# 1. what's in the GeoPackage?
available = [sub.name() for sub in QgsProviderRegistry.instance().querySublayers(str(GPKG))]
print("In the GeoPackage:", available)


# 2. helper
def load_gpkg_layer(layer_name):
    """Return a valid QgsVectorLayer for one layer of GPKG, or raise."""
    layer = QgsVectorLayer(f"{GPKG}|layername={layer_name}", layer_name, "ogr")
    if not layer.isValid():
        raise RuntimeError(f"Could not load {layer_name!r} from {GPKG}")
    return layer


# 3. groups
reference = root.addGroup("Reference")
base = root.addGroup("Base map")

# 4. layers
for name in ["places", "rivers", "graticule_10"]:
    layer = load_gpkg_layer(name)
    project.addMapLayer(layer, False)
    reference.addLayer(layer)

for name in ["lakes", "countries"]:
    layer = load_gpkg_layer(name)
    project.addMapLayer(layer, False)
    base.addLayer(layer)

relief = QgsRasterLayer(str(DATA / "world_shaded_relief.tif"), "World relief")
if not relief.isValid():
    raise RuntimeError("relief raster did not load")
project.addMapLayer(relief, False)
base.addLayer(relief)

# 5. hide the graticule
graticule = project.mapLayersByName("graticule_10")[0]
root.findLayer(graticule.id()).setItemVisibilityChecked(False)


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
