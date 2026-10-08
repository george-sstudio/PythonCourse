"""
MODULE 05 - Exercise 2: expressions, selections, filters - and the apostrophe trap
"""
from pathlib import Path

from qgis.core import QgsExpression, QgsExpressionContextUtils, QgsProject, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
countries = QgsVectorLayer(f"{GPKG}|layername=countries", "countries", "ogr")
QgsProject.instance().addMapLayer(countries)

# TODO 1: write an expression (as a Python string) for:
#         countries in Africa with more than 50 million people
expr_big_africa = ""
big_africa = [f["name"] for f in countries.getFeatures(expr_big_africa)]

# TODO 2: SELECT the low-income countries: income_grp is '5. Low income'
#         (countries.selectByExpression(...)), then count the selection
low_income_count = None

# TODO 3: FILTER the layer to Europe with setSubsetString, store the
#         featureCount(), then remove the filter again ("")
europe_count = None


# TODO 4: finish this function so it works for ANY name, including
#         "Côte d'Ivoire". Use QgsExpression.quotedColumnRef("name") and
#         QgsExpression.quotedValue(name).
def name_filter(name):
    """Return an expression that matches the country called `name`."""
    return f"\"name\" = '{name}'"     # <- the naive version: fix it


# This is how you can test an expression before using it
for test_name in ["Peru", "Côte d'Ivoire"]:
    e = QgsExpression(name_filter(test_name))
    print(test_name, "-> parser error?", e.hasParserError())

matches = list(countries.getFeatures(name_filter("Côte d'Ivoire")))

# --- Checks (don't edit below this line) ------------------------------------
assert sorted(big_africa) == ["Dem. Rep. Congo", "Egypt", "Ethiopia", "Kenya",
                              "Nigeria", "South Africa", "Tanzania"], f"TODO 1: {big_africa}"
assert low_income_count == 42, f"TODO 2: got {low_income_count}"
assert europe_count == 50, f"TODO 3: got {europe_count}"
assert countries.subsetString() == "", "TODO 3: remove the filter afterwards"
assert not QgsExpression(name_filter("Côte d'Ivoire")).hasParserError(), "TODO 4"
assert len(matches) == 1, "TODO 4: should find exactly one country"
print("All checks passed ✔")
