"""MODULE 07 - Solution 2: categorized, then graduated - and the -99 trap"""
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

# Part A
by_continent = QgsVectorLayer(f"{GPKG}|layername=countries", "Continents", "ogr")
project.addMapLayer(by_continent)

palette = {"Africa": "#e3c9a5", "Asia": "#e8d9a9", "Europe": "#c7d3e3",
           "North America": "#cfdcc0", "South America": "#d9c7dd", "Oceania": "#c6e0dc"}

existing = by_continent.uniqueValues(by_continent.fields().indexOf("continent"))
not_in_palette = set(existing) - set(palette.keys())
print("Will fall into 'Other':", not_in_palette)


def fill(colour):
    return QgsFillSymbol.createSimple({"color": colour, "outline_color": "#ffffff",
                                       "outline_width": "0.1"})


categories = [QgsRendererCategory(value, fill(colour), value) for value, colour in palette.items()]
categories.append(QgsRendererCategory(None, fill("#e4e4e4"), "Other"))
by_continent.setRenderer(QgsCategorizedSymbolRenderer("continent", categories))

# Part B
gdp = QgsVectorLayer(f"{GPKG}|layername=countries", "GDP per person", "ogr")
project.addMapLayer(gdp)

naive_expr = '"gdp_md" * 1000000 / "pop_est"'
naive = QgsGraduatedSymbolRenderer(naive_expr)
naive.setClassificationMethod(QgsClassificationJenks())
naive.updateClasses(gdp, 5)
print("naive lowest class starts at:", round(naive.ranges()[0].lowerValue()))

safe_expr = ('CASE WHEN "gdp_md" > 0 AND "pop_est" > 0 '
             'THEN "gdp_md" * 1000000 / "pop_est" END')       # otherwise NULL

safe = QgsGraduatedSymbolRenderer(safe_expr)
safe.setClassificationMethod(QgsClassificationJenks())
safe.updateClasses(gdp, 5)
safe.updateColorRamp(QgsStyle.defaultStyle().colorRamp("YlGnBu"))
gdp.setRenderer(safe)
for rng in safe.ranges():
    print(f"{rng.lowerValue():>10,.0f} – {rng.upperValue():>10,.0f}")

message, ok = gdp.saveNamedStyle(str(STYLES / "gdp_per_person.qml"))
if not ok:
    raise RuntimeError(message)

assert not_in_palette == {"Antarctica", "Seven seas (open ocean)"}, f"TODO 1: {not_in_palette}"
cats = by_continent.renderer().categories()
assert len(cats) == 7 and cats[-1].label() == "Other", "TODO 2"
assert naive.ranges()[0].lowerValue() < 0, "(the naive version really is broken)"
assert safe.ranges()[0].lowerValue() > 0, "TODO 3/4: the lowest class must start above 0"
assert len(safe.ranges()) == 5
assert (STYLES / "gdp_per_person.qml").exists(), "TODO 4: save the QML"
print("All checks passed ✔")
