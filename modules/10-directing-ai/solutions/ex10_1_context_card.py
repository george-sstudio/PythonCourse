"""MODULE 10 - Solution 1: a context card"""
import importlib.util
from pathlib import Path

from qgis.core import (QgsExpressionContextUtils, QgsProject, QgsRasterLayer, QgsUnitTypes,
                       QgsVariantUtils, QgsVectorLayer, QgsWkbTypes)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
project = QgsProject.instance()
project.clear()


def mini_card(layer):
    """Return a list of text lines describing a vector layer."""
    lines = [f"{layer.name()}: {QgsWkbTypes.displayString(layer.wkbType())}, "
             f"{layer.featureCount()} features",
             f"CRS: {layer.crs().authid()} "
             f"(units: {QgsUnitTypes.toString(layer.crs().mapUnits())})"]
    for field in layer.fields():
        nulls = sum(1 for f in layer.getFeatures() if QgsVariantUtils.isNull(f[field.name()]))
        lines.append(f"- {field.name()} ({field.typeName()}): {nulls} NULL")
    return lines


places = QgsVectorLayer(f"{GPKG}|layername=places", "places", "ogr")
card_a = mini_card(places)
print("\n".join(card_a))

for name in ["places", "rivers", "countries"]:
    project.addMapLayer(QgsVectorLayer(f"{GPKG}|layername={name}", name, "ogr"))
project.addMapLayer(QgsRasterLayer(str(COURSE / "data" / "dem_sample.tif"), "dem"))

spec = importlib.util.spec_from_file_location("describe_project",
                                              COURSE / "tools" / "describe_project.py")
describe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(describe)

card_b = describe.context_card()
print(card_b)
print("saved:", describe.save_card(card_b))

# Facts an AI would likely get wrong from memory:
#   1. field names: it's "pop_max" (places) / "pop_est" (countries), not "population"
#   2. units: everything is in degrees (EPSG:4326), and adm1name has 87 NULLs

assert card_a[0] == "places: Point, 1251 features", f"line 1: {card_a[:1]}"
assert card_a[1] == "CRS: EPSG:4326 (units: degrees)", f"line 2: {card_a[1:2]}"
assert "- adm1name (String): 87 NULL" in card_a, "count the NULLs in adm1name"
assert "EPSG:4326" in card_b and "dem" in card_b and "Float32" in card_b, "Part B"
assert (COURSE / "output" / "context_card.md").exists(), "save the card"
print("All checks passed ✔")
