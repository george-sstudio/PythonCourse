"""
MODULE 07 - Exercise 2: categorized, then graduated - and the -99 trap
"""
from pathlib import Path

from qgis.core import (QgsCategorizedSymbolRenderer, QgsClassificationJenks,
                       QgsExpressionContextUtils, QgsFillSymbol,
                       QgsGraduatedSymbolRenderer, QgsProject, QgsRendererCategory,
                       QgsStyle, QgsVectorLayer)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
STYLES = COURSE / "output" / "styles"
STYLES.mkdir(parents=True, exist_ok=True)
project = QgsProject.instance()

# --- Part A: categorized by continent --------------------------------------------
by_continent = QgsVectorLayer(f"{GPKG}|layername=countries", "Continents", "ogr")
project.addMapLayer(by_continent)

palette = {"Africa": "#e3c9a5", "Asia": "#e8d9a9", "Europe": "#c7d3e3",
           "North America": "#cfdcc0", "South America": "#d9c7dd", "Oceania": "#c6e0dc"}

# TODO 1: which continent values exist in the data that are NOT in the palette?
#         (by_continent.uniqueValues(index) gives a set; compare with palette.keys())
not_in_palette = set()
print("Will fall into 'Other':", not_in_palette)

# TODO 2: build the categories (one per palette entry + an "Other" catch-all
#         with value None, colour #e4e4e4), white 0.1 mm outlines, and set a
#         QgsCategorizedSymbolRenderer("continent", categories)


# --- Part B: graduated GDP per person ------------------------------------------------
gdp = QgsVectorLayer(f"{GPKG}|layername=countries", "GDP per person", "ogr")
project.addMapLayer(gdp)

naive_expr = '"gdp_md" * 1000000 / "pop_est"'
naive = QgsGraduatedSymbolRenderer(naive_expr)
naive.setClassificationMethod(QgsClassificationJenks())
naive.updateClasses(gdp, 5)
print("naive lowest class starts at:", round(naive.ranges()[0].lowerValue()))   # look!

# TODO 3: write safe_expr: the same calculation, but NULL when gdp_md <= 0
#         or pop_est <= 0   (CASE WHEN ... THEN ... END)
safe_expr = naive_expr

# TODO 4: a graduated renderer on safe_expr: Jenks, 5 classes, colour ramp "YlGnBu".
#         Set it on the gdp layer, print each range, save STYLES / "gdp_per_person.qml"
safe = None

# --- Checks (don't edit below this line) ------------------------------------
assert not_in_palette == {"Antarctica", "Seven seas (open ocean)"}, f"TODO 1: {not_in_palette}"
cats = by_continent.renderer().categories()
assert len(cats) == 7 and cats[-1].label() == "Other", "TODO 2"
assert naive.ranges()[0].lowerValue() < 0, "(the naive version really is broken)"
assert safe.ranges()[0].lowerValue() > 0, "TODO 3/4: the lowest class must start above 0"
assert len(safe.ranges()) == 5
assert (STYLES / "gdp_per_person.qml").exists(), "TODO 4: save the QML"
print("All checks passed ✔")
