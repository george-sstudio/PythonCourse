"""
MODULE 08 - Exercise 2: an A4 portrait country sheet (and a reusable template)

Most of the layout is GIVEN - read it. Your TODOs are the decisions:
  TODO 1  utm_crs(lon, lat)           the UTM zone CRS for a point
  TODO 2  nice_scale / nice_step      round scales and scale-bar steps
  TODO 3  to_map_extent(...)          the country's extent in the MAP's CRS
  TODO 4  the main map: CRS, extent, nice scale
  TODO 5  the scale bar segment length (about 20 mm on paper)
  TODO 6  the info text
  TODO 7  save the layout as a template (output/country_sheet.qpt)
Run it and open output/sheet_PER.pdf. Then try CODE = "KEN" (fine), and
CODE = "NOR": look closely at that map. What went wrong? (Module 12 explains it
and fixes it - but try to work out the cause first.)
"""
import math
from pathlib import Path

from qgis.core import (Qgis, QgsCoordinateReferenceSystem, QgsLegendStyle, QgsCoordinateTransform,
                       QgsDistanceArea, QgsExpressionContextUtils, QgsFillSymbol,
                       QgsLayoutExporter, QgsLayoutItemLabel, QgsLayoutItemLegend,
                       QgsLayoutItemMap, QgsLayoutItemMapOverview, QgsLayoutItemPage,
                       QgsLayoutItemPicture, QgsLayoutItemScaleBar, QgsLayoutItemShape,
                       QgsLayoutPoint, QgsLayoutSize, QgsLineSymbol, QgsMarkerSymbol,
                       QgsPalLayerSettings, QgsPathResolver, QgsPrintLayout, QgsProject,
                       QgsReadWriteContext, QgsRectangle, QgsRuleBasedRenderer,
                       QgsSingleSymbolRenderer, QgsSymbolLayerUtils, QgsTextBufferSettings,
                       QgsTextFormat, QgsVectorLayer, QgsVectorLayerSimpleLabeling)
from qgis.PyQt.QtGui import QColor

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
OUTPUT = COURSE / "output"
OUTPUT.mkdir(exist_ok=True)
MM = Qgis.LayoutUnit.Millimeters
CODE = "PER"

project = QgsProject.instance()
project.clear()


# ---------------------------------------------------------------------------------
# helpers you write (TODO 1-3 in the exercise)
# ---------------------------------------------------------------------------------
def utm_crs(lon, lat):
    """The WGS 84 / UTM zone CRS for a point."""
    # TODO 1: zone = int((lon + 180) // 6) + 1 ; EPSG 326xx north, 327xx south
    pass


def nice_scale(scale):
    """Round a scale UP to a 'nice' number: 10,650,000 -> 12,500,000."""
    # TODO 2: power = 10 ** math.floor(math.log10(scale)), then the first
    #         step * power that is >= scale
    pass


def nice_step(value):
    """Round DOWN to 1, 2, 2.5 or 5 x 10^n - for scale bar segments: 312 -> 250."""
    # TODO 2: the largest of (1, 2, 2.5, 5, 10) * power that is <= value
    pass


def to_map_extent(geometry, source_crs, map_crs, margin_m):
    """The geometry's bounding box in the map's CRS, grown by margin_m metres."""
    # TODO 3: QgsCoordinateTransform(source_crs, map_crs, project),
    #         .transformBoundingBox(geometry.boundingBox()), then .grow(margin_m)
    pass


# ---------------------------------------------------------------------------------
# data and styles (given)
# ---------------------------------------------------------------------------------
def load(name, display=None):
    lyr = QgsVectorLayer(f"{GPKG}|layername={name}", display or name, "ogr")
    if not lyr.isValid():
        raise RuntimeError(name)
    project.addMapLayer(lyr)
    return lyr


countries = load("countries", "Countries")
lakes = load("lakes", "Lakes")
rivers = load("rivers", "Rivers")
places = load("places", "Cities")

# No ocean layer: a world-wide polygon reprojected to a local UTM zone tears
# into strips. The sea is simply the map item's background colour instead.
SEA = "#e3ebf0"
lakes.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
    {"color": SEA, "outline_color": "#8fb0c7", "outline_width": "0.1"})))
rivers.setRenderer(QgsSingleSymbolRenderer(QgsLineSymbol.createSimple(
    {"color": "#8fb0c7", "width": "0.3"})))

# the country itself warm, its neighbours grey
root_rule = QgsRuleBasedRenderer.Rule(None)
root_rule.appendChild(QgsRuleBasedRenderer.Rule(QgsFillSymbol.createSimple(
    {"color": "#f1e4c9", "outline_color": "#7d6e57", "outline_width": "0.35"}),
    filterExp=f"\"adm0_a3\" = '{CODE}'", label="This country"))
root_rule.appendChild(QgsRuleBasedRenderer.Rule(QgsFillSymbol.createSimple(
    {"color": "#ebeae6", "outline_color": "#ffffff", "outline_width": "0.2"}),
    elseRule=True, label="Neighbouring countries"))
countries.setRenderer(QgsRuleBasedRenderer(root_rule))

places.setSubsetString(f"\"adm0_a3\" = '{CODE}'")          # only this country's places
places.setRenderer(QgsSingleSymbolRenderer(QgsMarkerSymbol.createSimple(
    {"name": "circle", "color": "#333333", "size": "1.6", "outline_color": "#ffffff"})))
label_format = QgsTextFormat()
label_format.setSize(7)
label_format.setColor(QColor("#222222"))
halo = QgsTextBufferSettings()
halo.setEnabled(True)
halo.setSize(0.6)
halo.setColor(QColor("#ffffff"))
label_format.setBuffer(halo)
label_settings = QgsPalLayerSettings()
label_settings.fieldName = "name"
label_settings.placement = Qgis.LabelPlacement.AroundPoint
label_settings.setFormat(label_format)
places.setLabeling(QgsVectorLayerSimpleLabeling(label_settings))
places.setLabelsEnabled(True)

country = next(countries.getFeatures(f"\"adm0_a3\" = '{CODE}'"))
geom = country.geometry()
centre = geom.centroid().asPoint()


# ---------------------------------------------------------------------------------
# the layout
# ---------------------------------------------------------------------------------
def text_format(size, colour="#222222"):
    fmt = QgsTextFormat()
    fmt.setSize(size)
    fmt.setColor(QColor(colour))
    return fmt


def add_label(item_id, text, size, x, y, width):
    label = QgsLayoutItemLabel(layout)
    label.setId(item_id)
    label.setText(text)
    label.setTextFormat(text_format(size))
    label.adjustSizeToText()
    label.attemptResize(QgsLayoutSize(width, label.sizeWithUnits().height(), MM))
    label.attemptMove(QgsLayoutPoint(x, y, MM))
    layout.addLayoutItem(label)
    return label


def freeze_legend(legend):
    if hasattr(legend, "setSyncMode"):            # QGIS 4.0+
        legend.setSyncMode(Qgis.LegendSyncMode.Manual)
    else:                                         # QGIS 3.x
        legend.setAutoUpdateModel(False)


manager = project.layoutManager()
layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName("Country sheet")
layout.pageCollection().page(0).setPageSize("A4", QgsLayoutItemPage.Orientation.Portrait)
manager.addLayout(layout)

add_label("title", country["name"], 22, 15, 10, 180)

# main map: UTM zone of the centroid, extent of the country, a nice scale
main = QgsLayoutItemMap(layout)
main.setId("main_map")
main.attemptMove(QgsLayoutPoint(15, 30, MM))
main.attemptResize(QgsLayoutSize(180, 190, MM))
# TODO 4: main.setCrs(...) with utm_crs of the centroid
main.setLayers([places, rivers, lakes, countries])
main.setBackgroundColor(QColor(SEA))
main.setKeepLayerSet(True)
main.setFrameEnabled(True)
# TODO 4: zoom to the country's extent (50 km margin), then set a nice scale
layout.addLayoutItem(main)
add_label("subtitle", f"{country['subregion']} · scale 1:{main.scale():,.0f} · "
          f"{main.crs().description()}", 9, 15, 21, 180)

# inset: where in the continent
inset = QgsLayoutItemMap(layout)
inset.setId("inset_map")
inset.attemptMove(QgsLayoutPoint(153, 226, MM))
inset.attemptResize(QgsLayoutSize(42, 42, MM))
inset.setCrs(countries.crs())
inset.setLayers([countries])
inset.setBackgroundColor(QColor(SEA))
inset.setKeepLayerSet(True)
inset.setFrameEnabled(True)
inset.zoomToExtent(QgsRectangle(-95, -60, -30, 15))
layout.addLayoutItem(inset)
where = QgsLayoutItemMapOverview("where", inset)
where.setLinkedMap(main)
inset.overviews().addOverview(where)

# north arrow
arrow = QgsLayoutItemPicture(layout)
arrow.setId("north_arrow")
arrow.setPicturePath(QgsSymbolLayerUtils.svgSymbolNameToPath("arrows/NorthArrow_02.svg",
                                                             QgsPathResolver()))
arrow.attemptResize(QgsLayoutSize(8, 12, MM))
arrow.attemptMove(QgsLayoutPoint(184, 33, MM))
arrow.setLinkedMap(main)
layout.addLayoutItem(arrow)

# scale bar: two segments, each a nice number of km, about 20 mm long
# TODO 5: how many km is 20 mm on paper at this scale? (scale * 0.020 m / 1000)
#         then round it down with nice_step
segment_km = 100
bar = QgsLayoutItemScaleBar(layout)
bar.setId("scalebar")
bar.setStyle("Single Box")
bar.setLinkedMap(main)
bar.setUnits(Qgis.DistanceUnit.Kilometers)
bar.setUnitLabel("km")
bar.setNumberOfSegmentsLeft(0)
bar.setNumberOfSegments(2)
bar.setUnitsPerSegment(segment_km)
bar.setTextFormat(text_format(7))
bar.attemptMove(QgsLayoutPoint(15, 226, MM))
layout.addLayoutItem(bar)

# legend
legend = QgsLayoutItemLegend(layout)
legend.setId("legend")
legend.setTitle("")
legend.setLinkedMap(main)
layout.addLayoutItem(legend)
freeze_legend(legend)
for style, size in [(QgsLegendStyle.Style.SymbolLabel, 7.5), (QgsLegendStyle.Style.Group, 8),
                    (QgsLegendStyle.Style.Subgroup, 8)]:
    legend.rstyle(style).setTextFormat(text_format(size))
legend.setSymbolWidth(5)
legend.setSymbolHeight(3.5)
legend.attemptMove(QgsLayoutPoint(106, 226, MM))

# info box: a shape with a label on top
da = QgsDistanceArea()
da.setSourceCrs(countries.crs(), project.transformContext())
da.setEllipsoid("EPSG:7030")
area_km2 = da.measureArea(geom) / 1e6
capital = next(places.getFeatures("\"featurecla\" LIKE 'Admin-0 capital%'"), None)
# TODO 6: a 4-line text: Area (km², no decimals, thousands separators),
#         Population, Density (1 decimal), Capital   - use "\n" between lines
info = "Area: ?\nPopulation: ?\nDensity: ?\nCapital: ?"

box = QgsLayoutItemShape(layout)
box.setId("info_box")
box.setShapeType(QgsLayoutItemShape.Shape.Rectangle)
box.setSymbol(QgsFillSymbol.createSimple({"color": "#f7f4ee", "outline_color": "#b8b2a5",
                                          "outline_width": "0.2"}))
box.attemptMove(QgsLayoutPoint(15, 240, MM))
box.attemptResize(QgsLayoutSize(85, 28, MM))
layout.addLayoutItem(box)
add_label("info_text", info, 8.5, 19, 243, 78)

add_label("source", "Data: Natural Earth (public domain) · Map: George, PythonCourse",
          6.5, 15, 284, 180)

# ---------------------------------------------------------------------------------
# export + template
# ---------------------------------------------------------------------------------
pdf = QgsLayoutExporter.PdfExportSettings()
pdf.dpi = 300
result = QgsLayoutExporter(layout).exportToPdf(str(OUTPUT / f"sheet_{CODE}.pdf"), pdf)
if result != QgsLayoutExporter.ExportResult.Success:
    raise RuntimeError(f"export failed: {result}")
png = QgsLayoutExporter.ImageExportSettings()
png.dpi = 110
QgsLayoutExporter(layout).exportToImage(str(OUTPUT / f"sheet_{CODE}.png"), png)

# TODO 7: save the layout as a template
template_ok = False
print(f"{country['name']}: {main.crs().authid()}, 1:{main.scale():,.0f}, "
      f"scale bar 2 x {segment_km:g} km")

# --- Checks (don't edit below this line) ------------------------------------
assert utm_crs(-74.4, -9.2).authid() == "EPSG:32718"
assert utm_crs(16.4, 48.2).authid() == "EPSG:32633"
assert nice_scale(10_650_000) == 12_500_000 and nice_scale(1_900_000) == 2_000_000
assert nice_step(312) == 250 and nice_step(99) == 50
assert main.crs().authid() == "EPSG:32718", "main map should be in UTM 18S"
assert round(main.scale()) == 12_500_000, f"scale {main.scale()}"
assert layout.itemById("info_text") is not None and "km²" in layout.itemById("info_text").text()
assert template_ok and (OUTPUT / "country_sheet.qpt").exists()
assert (OUTPUT / f"sheet_{CODE}.pdf").exists()
print("All checks passed ✔  - open sheet_PER.pdf")
