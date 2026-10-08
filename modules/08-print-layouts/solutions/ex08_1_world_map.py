"""MODULE 08 - Solution 1: an A4 landscape world map"""
from pathlib import Path

from qgis.core import (Qgis, QgsCategorizedSymbolRenderer, QgsCoordinateReferenceSystem,
                       QgsExpressionContextUtils, QgsFillSymbol, QgsLayoutExporter,
                       QgsLayoutItemLabel, QgsLayoutItemLegend, QgsLayoutItemMap,
                       QgsLayoutItemPage, QgsLayoutPoint, QgsLayoutSize, QgsLineSymbol,
                       QgsPrintLayout, QgsProject, QgsRectangle, QgsRendererCategory,
                       QgsSingleSymbolRenderer, QgsTextFormat, QgsVectorLayer)
from qgis.PyQt.QtGui import QColor

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


def text_format(size, family=None):
    fmt = QgsTextFormat()
    if family:
        from qgis.PyQt.QtGui import QFont
        fmt.setFont(QFont(family))
    fmt.setSize(size)
    fmt.setColor(QColor("#222222"))
    return fmt


def add_label(text, size, x, y, width=200):
    label = QgsLayoutItemLabel(layout)
    label.setText(text)
    label.setTextFormat(text_format(size))
    label.adjustSizeToText()             # sets a height that fits the text...
    # ...but give it a generous width too: if a font is missing, QGIS measures
    # the fallback font and the title can wrap onto two lines.
    label.attemptResize(QgsLayoutSize(width, label.sizeWithUnits().height(), MM))
    label.attemptMove(QgsLayoutPoint(x, y, MM))
    layout.addLayoutItem(label)
    return label


# 1. layout and page
manager = project.layoutManager()
old = manager.layoutByName("World by continent")
if old:
    manager.removeLayout(old)
layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName("World by continent")
layout.pageCollection().page(0).setPageSize("A4", QgsLayoutItemPage.Orientation.Landscape)
manager.addLayout(layout)

# 2. map
world_map = QgsLayoutItemMap(layout)
world_map.setId("main_map")
world_map.attemptMove(QgsLayoutPoint(10, 22, MM))
world_map.attemptResize(QgsLayoutSize(277, 160, MM))
world_map.setCrs(QgsCoordinateReferenceSystem("EPSG:8857"))
world_map.setLayers([graticule, countries, ocean])
world_map.setKeepLayerSet(True)
world_map.setFrameEnabled(True)
world_map.zoomToExtent(QgsRectangle(-17_250_000, -8_400_000, 17_250_000, 8_400_000))
layout.addLayoutItem(world_map)

# 3. texts
add_label("The world by continent", 18, 10, 8)
add_label("Data: Natural Earth", 7, 10, 196)

# 4. legend
legend = QgsLayoutItemLegend(layout)
legend.setLinkedMap(world_map)
legend.setTitle("")
layout.addLayoutItem(legend)
freeze_legend(legend)
root = legend.model().rootGroup()
root.removeLayer(ocean)
root.removeLayer(graticule)
legend.setSymbolWidth(5)
legend.setSymbolHeight(3.5)
legend.attemptMove(QgsLayoutPoint(13, 118, MM))

# 5. export
exporter = QgsLayoutExporter(layout)
pdf = QgsLayoutExporter.PdfExportSettings()
pdf.dpi = 300
pdf_result = exporter.exportToPdf(str(OUTPUT / "world_continents.pdf"), pdf)
png = QgsLayoutExporter.ImageExportSettings()
png.dpi = 150
png_result = exporter.exportToImage(str(OUTPUT / "world_continents.png"), png)
for name, result in [("PDF", pdf_result), ("PNG", png_result)]:
    if result != QgsLayoutExporter.ExportResult.Success:
        raise RuntimeError(f"{name} export failed: {result}")
print("Exported", OUTPUT / "world_continents.pdf")

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
