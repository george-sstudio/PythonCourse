"""
MODULE 10 - Exercise 1: a context card

Part A: write a MINI context card for one layer yourself - so you know what
        the full tool does and why each fact matters.
Part B: run the full tool (tools/describe_project.py) on a small project and
        save the card to output/context_card.md.
"""
import importlib.util
from pathlib import Path

from qgis.core import (QgsExpressionContextUtils, QgsProject, QgsRasterLayer, QgsUnitTypes,
                       QgsVariantUtils, QgsVectorLayer, QgsWkbTypes)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
project = QgsProject.instance()
project.clear()


# --- Part A ----------------------------------------------------------------------
def mini_card(layer):
    """Return a list of text lines describing a vector layer:
        line 1: "<name>: <geometry type>, <n> features"     (QgsWkbTypes.displayString)
        line 2: "CRS: <authid> (units: <units>)"            (QgsUnitTypes.toString)
        then one line per field: "- <field name> (<type name>): <k> NULL"
            (count NULLs with QgsVariantUtils.isNull)
    """
    lines = []
    # TODO
    return lines


places = QgsVectorLayer(f"{GPKG}|layername=places", "places", "ogr")
card_a = mini_card(places)
print("\n".join(card_a))

# --- Part B -------------------------------------------------------------------------
for name in ["places", "rivers", "countries"]:
    project.addMapLayer(QgsVectorLayer(f"{GPKG}|layername={name}", name, "ogr"))
project.addMapLayer(QgsRasterLayer(str(COURSE / "data" / "dem_sample.tif"), "dem"))

spec = importlib.util.spec_from_file_location("describe_project",
                                              COURSE / "tools" / "describe_project.py")
describe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(describe)

# TODO: card_b = describe.context_card(); print it; save it with describe.save_card(card_b)
card_b = ""

# TODO: read the card. Which TWO facts in it would an AI most likely have got
#       wrong if you had described the project from memory? Write them here:
#   1.
#   2.

# --- Checks (don't edit below this line) ------------------------------------
assert card_a[0] == "places: Point, 1251 features", f"line 1: {card_a[:1]}"
assert card_a[1] == "CRS: EPSG:4326 (units: degrees)", f"line 2: {card_a[1:2]}"
assert "- adm1name (String): 87 NULL" in card_a, "count the NULLs in adm1name"
assert "EPSG:4326" in card_b and "dem" in card_b and "Float32" in card_b, "Part B"
assert (COURSE / "output" / "context_card.md").exists(), "save the card"
print("All checks passed ✔")
