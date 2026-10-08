"""
MODULE 08 - Exercise 3: an atlas of South America from the country-sheet template

Needs output/country_sheet.qpt from exercise 2.
Most of the script is given. TODOs:
  TODO 1  reconnect the map items AND the legend to this project's layers
  TODO 2  set the main map CRS for the whole atlas (ESRI:102033)
  TODO 3  turn the title and info text into per-page expressions
  TODO 4  set up the atlas (coverage, filter, sort) and make the map atlas-driven
  TODO 5  export one multi-page PDF and CHECK the result
"""
from pathlib import Path

from qgis.core import (Qgis, QgsCoordinateReferenceSystem, QgsExpressionContextUtils,
                       QgsFillSymbol, QgsLayoutExporter, QgsLayoutItemMap, QgsLineSymbol,
                       QgsMarkerSymbol, QgsPrintLayout, QgsProject, QgsReadWriteContext,
                       QgsRuleBasedRenderer, QgsSingleSymbolRenderer, QgsVectorLayer)
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtXml import QDomDocument

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
OUTPUT = COURSE / "output"
TEMPLATE = OUTPUT / "country_sheet.qpt"
if not TEMPLATE.exists():
    raise RuntimeError("Run ex08_2_country_sheet.py first - it saves the template")

project = QgsProject.instance()
project.clear()
SEA = "#e3ebf0"


def load(name, display):
    lyr = QgsVectorLayer(f"{GPKG}|layername={name}", display, "ogr")
    if not lyr.isValid():
        raise RuntimeError(name)
    project.addMapLayer(lyr)
    return lyr


countries = load("countries", "Countries")
lakes = load("lakes", "Lakes")
rivers = load("rivers", "Rivers")
places = load("places", "Capitals")

lakes.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
    {"color": SEA, "outline_color": "#8fb0c7", "outline_width": "0.1"})))
rivers.setRenderer(QgsSingleSymbolRenderer(QgsLineSymbol.createSimple(
    {"color": "#8fb0c7", "width": "0.3"})))
places.setSubsetString("\"featurecla\" LIKE 'Admin-0 capital%'")
places.setRenderer(QgsSingleSymbolRenderer(QgsMarkerSymbol.createSimple(
    {"name": "square", "color": "#333333", "size": "1.8", "outline_color": "#ffffff"})))

# 1. highlight "the current atlas country": its feature id equals @atlas_featureid
root = QgsRuleBasedRenderer.Rule(None)
root.appendChild(QgsRuleBasedRenderer.Rule(QgsFillSymbol.createSimple(
    {"color": "#f1e4c9", "outline_color": "#7d6e57", "outline_width": "0.35"}),
    filterExp="$id = @atlas_featureid", label="This country"))
root.appendChild(QgsRuleBasedRenderer.Rule(QgsFillSymbol.createSimple(
    {"color": "#ebeae6", "outline_color": "#ffffff", "outline_width": "0.2"}),
    elseRule=True, label="Neighbouring countries"))
countries.setRenderer(QgsRuleBasedRenderer(root))

# 2. load the template
doc = QDomDocument()
doc.setContent(TEMPLATE.read_text(encoding="utf-8"))
atlas_layout = QgsPrintLayout(project)
items, ok = atlas_layout.loadFromTemplate(doc, QgsReadWriteContext())
if not ok:
    raise RuntimeError("template did not load")
atlas_layout.setName("South America atlas")
manager = project.layoutManager()
old = manager.layoutByName("South America atlas")
if old:
    manager.removeLayout(old)
manager.addLayout(atlas_layout)

main = atlas_layout.itemById("main_map")
inset = atlas_layout.itemById("inset_map")

# 3. reconnect layers: a template stores layers by their ID, and this new
#    project's layers have new IDs, so the map items lost them.
# TODO 1: main.setLayers([...]) top first, inset.setLayers([countries]), then
#         legend = atlas_layout.itemById("legend"); legend_root = legend.model().rootGroup()
#         legend_root.clear() and legend_root.addLayer(...) for each layer
legend_root = None

# 4. one CRS for the whole atlas: South America Albers Equal Area Conic
# TODO 2

# 5. texts become expressions, evaluated per page
# TODO 3: title -> '[% "name" %]'
#         info_text -> three lines using [% format_number("pop_est", 0) %],
#         [% "income_grp" %] and the area:
#         [% format_number(area(transform(@atlas_geometry, 'EPSG:4326', 'ESRI:102033')) / 1e6, 0) %]
#         (the subtitle is given below as an example)
atlas_layout.itemById("subtitle").setText(
    '[% "subregion" %] · page [% @atlas_featurenumber %] of [% @atlas_totalfeatures %]'
    ' · scale 1:[% format_number(map_get(item_variables(\'main_map\'), \'map_scale\'), 0) %]')

# 6. the scale bar can't keep a fixed segment length when the scale changes
bar = atlas_layout.itemById("scalebar")
bar.setSegmentSizeMode(Qgis.ScaleBarSegmentSizeMode.FitWidth)
bar.setMinimumBarWidth(30)
bar.setMaximumBarWidth(45)

# 7. the atlas
atlas = atlas_layout.atlas()
# TODO 4: coverage layer countries, filter continent = 'South America', sort by
#         name, enable the atlas, and main.setAtlasDriven(True)

main.setAtlasScalingMode(QgsLayoutItemMap.AtlasScalingMode.Predefined)  # nice scales only
atlas_layout.renderContext().setPredefinedScales(
    [1_000_000, 2_000_000, 2_500_000, 5_000_000, 7_500_000, 10_000_000,
     12_500_000, 15_000_000, 20_000_000, 25_000_000, 30_000_000])

pages = atlas.updateFeatures()
pdf = QgsLayoutExporter.PdfExportSettings()
pdf.dpi = 200
# TODO 5: result, error = QgsLayoutExporter.exportToPdf(atlas, str(OUTPUT / "atlas_south_america.pdf"), pdf)
#         and raise RuntimeError if result is not Success

# preview one page as PNG (page 3 = Brazil when sorted by name)
atlas.beginRender()
atlas.seekTo(2)
png = QgsLayoutExporter.ImageExportSettings()
png.dpi = 80
QgsLayoutExporter(atlas_layout).exportToImage(str(OUTPUT / "atlas_page3.png"), png)
atlas.endRender()

# --- Checks (don't edit below this line) ------------------------------------
assert pages == 13, f"expected 13 South American countries, got {pages}"
assert main.layers(), "the map items must have layers again"
assert [n.name() for n in legend_root.findLayers()] == ["Capitals", "Rivers", "Lakes", "Countries"]
assert main.atlasDriven()
assert (OUTPUT / "atlas_south_america.pdf").stat().st_size > 50_000
print("All checks passed ✔  - open atlas_south_america.pdf")
