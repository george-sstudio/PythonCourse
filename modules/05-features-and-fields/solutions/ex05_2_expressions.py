"""MODULE 05 - Solution 2: expressions, selections, filters - and the apostrophe trap"""
from pathlib import Path

from qgis.core import QgsExpression, QgsExpressionContextUtils, QgsProject, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
countries = QgsVectorLayer(f"{GPKG}|layername=countries", "countries", "ogr")
QgsProject.instance().addMapLayer(countries)

# 1 - single quotes for Python outside, so the expression's quotes read naturally
expr_big_africa = '"continent" = \'Africa\' AND "pop_est" > 50000000'
big_africa = [f["name"] for f in countries.getFeatures(expr_big_africa)]

# 2 - selection
countries.selectByExpression('"income_grp" = \'5. Low income\'')
low_income_count = countries.selectedFeatureCount()
countries.removeSelection()

# 3 - filter (subset string), then clear it
countries.setSubsetString('"continent" = \'Europe\'')
europe_count = countries.featureCount()
countries.setSubsetString("")


# 4 - let QGIS do the quoting
def name_filter(name):
    """Return an expression that matches the country called `name`."""
    return f"{QgsExpression.quotedColumnRef('name')} = {QgsExpression.quotedValue(name)}"


for test_name in ["Peru", "Côte d'Ivoire"]:
    e = QgsExpression(name_filter(test_name))
    print(test_name, "->", name_filter(test_name), "| parser error?", e.hasParserError())

matches = list(countries.getFeatures(name_filter("Côte d'Ivoire")))

assert sorted(big_africa) == ["Dem. Rep. Congo", "Egypt", "Ethiopia", "Kenya",
                              "Nigeria", "South Africa", "Tanzania"], f"TODO 1: {big_africa}"
assert low_income_count == 42, f"TODO 2: got {low_income_count}"
assert europe_count == 50, f"TODO 3: got {europe_count}"
assert countries.subsetString() == "", "TODO 3: remove the filter afterwards"
assert not QgsExpression(name_filter("Côte d'Ivoire")).hasParserError(), "TODO 4"
assert len(matches) == 1, "TODO 4: should find exactly one country"
print("All checks passed ✔")
