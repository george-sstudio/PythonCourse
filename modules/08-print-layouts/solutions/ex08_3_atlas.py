"""MODULE 08 - Solution 3: an atlas of South America from the country-sheet template"""
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
main.setLayers([places, rivers, lakes, countries])
inset.setLayers([countries])
legend = atlas_layout.itemById("legend")          # its frozen layer list is stale too
legend_root = legend.model().rootGroup()
legend_root.clear()
for lyr in [places, rivers, lakes, countries]:
    legend_root.addLayer(lyr)

# 4. one CRS for the whole atlas: South America Albers Equal Area Conic
main.setCrs(QgsCoordinateReferenceSystem("ESRI:102033"))

# 5. texts become expressions, evaluated per page
atlas_layout.itemById("title").setText('[% "name" %]')
atlas_layout.itemById("subtitle").setText(
    '[% "subregion" %] · page [% @atlas_featurenumber %] of [% @atlas_totalfeatures %]'
    ' · scale 1:[% format_number(map_get(item_variables(\'main_map\'), \'map_scale\'), 0) %]')
atlas_layout.itemById("info_text").setText(
    "Area: [% format_number(area(transform(@atlas_geometry, 'EPSG:4326', 'ESRI:102033')) / 1e6, 0) %] km²\n"
    "Population: [% format_number(\"pop_est\", 0) %]\n"
    "Income group: [% \"income_grp\" %]")

# 6. the scale bar can't keep a fixed segment length when the scale changes
bar = atlas_layout.itemById("scalebar")
bar.setSegmentSizeMode(Qgis.ScaleBarSegmentSizeMode.FitWidth)
bar.setMinimumBarWidth(30)
bar.setMaximumBarWidth(45)

# 7. the atlas
atlas = atlas_layout.atlas()
atlas.setCoverageLayer(countries)
atlas.setFilterFeatures(True)
atlas.setFilterExpression("\"continent\" = 'South America'")
atlas.setSortFeatures(True)
atlas.setSortExpression('"name"')
atlas.setEnabled(True)

main.setAtlasDriven(True)
main.setAtlasScalingMode(QgsLayoutItemMap.AtlasScalingMode.Predefined)  # nice scales only
atlas_layout.renderContext().setPredefinedScales(
    [1_000_000, 2_000_000, 2_500_000, 5_000_000, 7_500_000, 10_000_000,
     12_500_000, 15_000_000, 20_000_000, 25_000_000, 30_000_000])

pages = atlas.updateFeatures()
pdf = QgsLayoutExporter.PdfExportSettings()
pdf.dpi = 200
result, error = QgsLayoutExporter.exportToPdf(atlas, str(OUTPUT / "atlas_south_america.pdf"), pdf)
if result != QgsLayoutExporter.ExportResult.Success:
    raise RuntimeError(f"atlas export failed: {error}")
print(f"Exported {pages} pages to atlas_south_america.pdf")

# preview one page as PNG (page 3 = Brazil when sorted by name)
atlas.beginRender()
atlas.seekTo(2)
png = QgsLayoutExporter.ImageExportSettings()
png.dpi = 80
QgsLayoutExporter(atlas_layout).exportToImage(str(OUTPUT / "atlas_page3.png"), png)
atlas.endRender()

# --- Checks ------------------------------------------------------------------
assert pages == 13, f"expected 13 South American countries, got {pages}"
assert main.layers(), "the map items must have layers again"
assert [n.name() for n in legend_root.findLayers()] == ["Capitals", "Rivers", "Lakes", "Countries"]
assert main.atlasDriven()
assert (OUTPUT / "atlas_south_america.pdf").stat().st_size > 50_000
print("All checks passed ✔  - open atlas_south_america.pdf")
