"""
MODULE 08 - Exercise 1: an A4 landscape world map

Page: A4 landscape (297 x 210 mm). Map CRS: Equal Earth (EPSG:8857).
Items (all positions in mm):
    map     x 10, y 22, 277 x 160, layers [graticule, countries, ocean], frame on
    title   "The world by continent", 18 pt, at x 10, y 8
    legend  continents only (no ocean, no graticule), at x 13, y 118,
            symbols 5 x 3.5 mm (setSymbolWidth / setSymbolHeight)
    source  "Data: Natural Earth", 7 pt, at x 10, y 196
NO scale bar and NO north arrow (both are misleading on a world map).
Export output/world_continents.pdf (300 dpi) and .png (150 dpi), and CHECK both.
"""
from pathlib import Path

from qgis.core import (Qgis, QgsCategorizedSymbolRenderer, QgsCoordinateReferenceSystem,
                       QgsExpressionContextUtils, QgsFillSymbol, QgsLayoutExporter,
                       QgsLayoutItemLabel, QgsLayoutItemLegend, QgsLayoutItemMap,
                       QgsLayoutItemPage, QgsLayoutPoint, QgsLayoutSize, QgsLineSymbol,
                       QgsPrintLayout, QgsProject, QgsRectangle, QgsRendererCategory,
                       QgsSingleSymbolRenderer, QgsTextFormat, QgsVectorLayer)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
OUTPUT = COURSE / "output"
OUTPUT.mkdir(exist_ok=True)
MM = Qgis.LayoutUnit.Millimeters

project = QgsProject.instance()
project.clear()


def load(name):
    lyr = QgsVectorLayer(f"{GPKG}|layername={name}", name, "ogr")
    if not lyr.isValid():
        raise RuntimeError(name)
    return lyr


ocean, countries, graticule = load("ocean"), load("countries_110m"), load("graticule_10")
countries.setName("Continent")          # the legend shows the layer name as a heading
for lyr in [ocean, countries, graticule]:
    project.addMapLayer(lyr)

# --- styles (given) ------------------------------------------------------------
ocean.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
    {"color": "#e3ebf0", "outline_style": "no"})))
graticule.setRenderer(QgsSingleSymbolRenderer(QgsLineSymbol.createSimple(
    {"color": "#c5d3dc", "width": "0.1"})))
palette = {"Africa": "#e3c9a5", "Asia": "#e8d9a9", "Europe": "#c7d3e3",
           "North America": "#cfdcc0", "South America": "#d9c7dd", "Oceania": "#c6e0dc",
           "Antarctica": "#eeeeee"}
countries.setRenderer(QgsCategorizedSymbolRenderer("continent", [
    QgsRendererCategory(k, QgsFillSymbol.createSimple(
        {"color": v, "outline_color": "#ffffff", "outline_width": "0.1"}), k)
    for k, v in palette.items()]))


def freeze_legend(legend):
    """Stop the legend following the Layers panel - works in QGIS 3 and 4."""
    if hasattr(legend, "setSyncMode"):
        legend.setSyncMode(Qgis.LegendSyncMode.Manual)
    else:
        legend.setAutoUpdateModel(False)


# --- 1. layout and page ------------------------------------------------------------
manager = project.layoutManager()
layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName("World by continent")
# TODO: set the page to A4 landscape, and add the layout to the manager


# --- 2. map ----------------------------------------------------------------------------
world_map = QgsLayoutItemMap(layout)
world_map.setId("main_map")
# TODO: position + size, CRS EPSG:8857, layers [graticule, countries, ocean],
#       keep layer set, frame on, then zoom to the whole world:
#       the Equal Earth extent is roughly QgsRectangle(-17_250_000, -8_400_000, 17_250_000, 8_400_000)
#       and add it to the layout


# --- 3. title and source -------------------------------------------------------------
# TODO: two QgsLayoutItemLabel items (setText, setTextFormat, adjustSizeToText, attemptMove)


# --- 4. legend -------------------------------------------------------------------------
legend = QgsLayoutItemLegend(layout)
legend.setLinkedMap(world_map)
legend.setTitle("")
layout.addLayoutItem(legend)
freeze_legend(legend)
# TODO: remove ocean and graticule from legend.model().rootGroup(), set the
#       symbol size and move the legend


# --- 5. export -------------------------------------------------------------------------
exporter = QgsLayoutExporter(layout)
# TODO: export the PDF (300 dpi) and PNG (150 dpi); raise if a result is not Success
pdf_result = None
png_result = None

# --- Checks (don't edit below this line) ------------------------------------
page = layout.pageCollection().page(0)
assert (page.pageSize().width(), page.pageSize().height()) == (297, 210), "1: A4 landscape"
assert manager.layoutByName("World by continent") is not None, "1: add to the manager"
assert world_map.crs().authid() == "EPSG:8857", "2: Equal Earth"
legend_layers = [n.name() for n in legend.model().rootGroup().findLayers()]
assert legend_layers == ["Continent"], f"4: legend shows {legend_layers}"
assert pdf_result == QgsLayoutExporter.ExportResult.Success, "5: PDF export"
assert (OUTPUT / "world_continents.pdf").stat().st_size > 10_000
assert (OUTPUT / "world_continents.png").exists()
print("All checks passed ✔  - now open the PDF and look at it")
