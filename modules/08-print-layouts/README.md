# Module 08: Print layouts and export

**Time:** about 4 hours · **Week 3** · *Not in the book. The book stops at the map canvas. For print cartography, this is where automation pays off most.*

## You will

- build an A4 layout by code: map, title, legend, scale bar, north arrow, inset map, info box
- place items precisely in **millimetres**, and set an exact map **scale**
- pick a suitable CRS for each map automatically (UTM zone from the centroid)
- export PDF and PNG, and check the export worked
- save and reuse **layout templates** (`.qpt`), finding items by their **id**
- run an **atlas**: one page per feature, all from one layout

## Key words

| Word | Meaning |
|---|---|
| **Print layout** | QGIS's page designer (*Project → New Print Layout*). Class: `QgsPrintLayout`. |
| **Layout item** | Anything on the page: map, label, legend, scale bar, picture, shape. Classes start with `QgsLayoutItem…`. |
| **Map item** | A window onto the map *inside* the layout, with its own extent, scale, CRS and layers. |
| **Reference point** | The point of an item that its position refers to. Default: top-left. |
| **Item id** | A name you give an item (`"main_map"`) so code can find it later in a template. |
| **Template (`.qpt`)** | A saved layout (positions, styles, text) with no project attached. |
| **Atlas** | A layout that repeats once per feature of a **coverage layer**, moving the map each time. |
| **Overview** | A frame on an inset map showing where the main map's extent is. |

---

## 1. Create a layout and a page

```python
from qgis.core import (Qgis, QgsLayoutItemPage, QgsLayoutPoint, QgsLayoutSize,
                       QgsPrintLayout, QgsProject)

project = QgsProject.instance()
manager = project.layoutManager()

old = manager.layoutByName("Country sheet")      # remove a previous run's layout
if old:
    manager.removeLayout(old)

layout = QgsPrintLayout(project)
layout.initializeDefaults()                      # adds one A4 landscape page
layout.setName("Country sheet")
layout.pageCollection().page(0).setPageSize("A4", QgsLayoutItemPage.Orientation.Portrait)
manager.addLayout(layout)                        # now it's visible in the Layout Manager
```

**Positions and sizes in mm:**

```python
MM = Qgis.LayoutUnit.Millimeters
item.attemptMove(QgsLayoutPoint(15, 30, MM))      # x, y of the top-left corner
item.attemptResize(QgsLayoutSize(180, 200, MM))   # width, height
```

The page is 210 × 297 mm. x runs left → right, and y runs **top → bottom**.

## 2. The map item

```python
from qgis.core import QgsLayoutItemMap

main = QgsLayoutItemMap(layout)
main.setId("main_map")
main.attemptMove(QgsLayoutPoint(15, 30, MM))
main.attemptResize(QgsLayoutSize(180, 200, MM))
main.setCrs(QgsCoordinateReferenceSystem("EPSG:32718"))   # the map's own CRS
main.setLayers([places, rivers, countries])              # which layers, top first
main.setKeepLayerSet(True)                               # don't follow the Layers panel
main.zoomToExtent(extent)                                # a QgsRectangle in the MAP's CRS
main.setScale(8_000_000)                                 # exact scale 1:8,000,000
main.setFrameEnabled(True)
layout.addLayoutItem(main)
```

**Order matters:** set the size and CRS, then the extent, then the scale. `zoomToExtent` sets a scale that fits the extent, and `setScale` then fixes it at a round number (keeping the centre).

### Extent in the right CRS

Layer extents are in the layer's CRS (degrees here), while the map item wants its own CRS:

```python
from qgis.core import QgsCoordinateTransform
to_map = QgsCoordinateTransform(countries.crs(), main.crs(), project)
extent = to_map.transformBoundingBox(feature.geometry().boundingBox())
extent.grow(50_000)                    # 50 km margin (map CRS is in metres)
```

### Choosing a CRS automatically: the UTM zone

```python
def utm_crs(lon, lat):
    """The WGS 84 / UTM zone CRS for a point. Good for maps of one country or region."""
    zone = int((lon + 180) // 6) + 1
    epsg = (32600 if lat >= 0 else 32700) + zone
    return QgsCoordinateReferenceSystem(f"EPSG:{epsg}")
```

> **Torn oceans:** a world-wide polygon (like the `ocean` layer) reprojected into a *local* CRS such as a UTM zone often tears into strips, because parts of the world can't be drawn in that CRS. For local maps, leave the ocean layer out and use the map item's background colour as the sea: `main.setBackgroundColor(QColor("#e3ebf0"))`. The same can happen to *other countries*: Russia and Fiji cross the 180° meridian, and in a UTM zone far away they can turn into huge shapes that cover the map. Try the country sheet for Norway and you'll see it. Module 12 shows the fix: clip world-wide layers to a window around the country before drawing.

UTM is fine for a country that fits in a few zones. For big countries (Russia, Canada, Brazil) choose a conic or equal-area CRS by hand. Your atlas uses a national grid (EPSG:2039), which is better still when one exists.

### A "nice" scale

```python
import math
def nice_scale(scale):
    """Round a scale UP to a 'nice' number: 10,650,000 → 12,500,000."""
    power = 10 ** math.floor(math.log10(scale))
    steps = (1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 7.5, 10)
    return next(s * power for s in steps if scale <= s * power)
```

`next(...)` returns the first value from the loop inside it, here the first step that's big enough. Rounding **up** makes the map a little smaller on the page, so the country still fits.

## 3. Text, legend, scale bar, north arrow

### Labels

```python
from qgis.core import QgsLayoutItemLabel, QgsTextFormat
from qgis.PyQt.QtGui import QColor, QFont

title = QgsLayoutItemLabel(layout)
title.setText("Peru")
fmt = QgsTextFormat()
fmt.setFont(QFont("Spectral"))
fmt.setSize(24)
fmt.setColor(QColor("#222222"))
title.setTextFormat(fmt)
title.adjustSizeToText()                                  # a height that fits the text
title.attemptResize(QgsLayoutSize(180, title.sizeWithUnits().height(), MM))   # and a generous width
title.attemptMove(QgsLayoutPoint(15, 12, MM))
layout.addLayoutItem(title)
```

Why the extra width? If the font isn't installed, QGIS measures the fallback font, and the text can wrap onto a second line. A fixed, generous width avoids surprise line breaks.

Label text can contain **expressions** in `[% %]`. They're evaluated when the layout renders, which is essential for atlases:

```python
title.setText('[% "name" %]')
source.setText("Data: Natural Earth · Printed [% format_date(now(), 'd MMMM yyyy') %]")
```

### Legend

```python
from qgis.core import QgsLayoutItemLegend

legend = QgsLayoutItemLegend(layout)
legend.setTitle("")
legend.setLinkedMap(main)
legend.setLegendFilterByMapEnabled(True)     # only show symbols visible on this map
layout.addLayoutItem(legend)
```

To choose **which layers** appear, stop the legend following the project, then edit its own layer list:

```python
def freeze_legend(legend):
    """Stop the legend following the Layers panel - works in QGIS 3 and 4."""
    if hasattr(legend, "setSyncMode"):                 # QGIS 4.0+
        legend.setSyncMode(Qgis.LegendSyncMode.Manual)
    else:                                              # QGIS 3.x
        legend.setAutoUpdateModel(False)

freeze_legend(legend)
group = legend.model().rootGroup()
group.removeLayer(ocean)                     # not needed in the legend
```

`setAutoUpdateModel` is **deprecated in QGIS 4** (it still works, with a warning). The `hasattr` check is the pattern for "use the new method where it exists". More in Module 09.

### Scale bar

```python
from qgis.core import QgsLayoutItemScaleBar

bar = QgsLayoutItemScaleBar(layout)
bar.setStyle("Single Box")                   # also "Line Ticks Up", "Double Box", "Numeric"...
bar.setLinkedMap(main)
bar.setUnits(Qgis.DistanceUnit.Kilometers)
bar.setUnitLabel("km")
bar.setNumberOfSegmentsLeft(0)
bar.setNumberOfSegments(2)
bar.setUnitsPerSegment(100)                  # 2 × 100 km
bar.attemptMove(QgsLayoutPoint(15, 235, MM))
layout.addLayoutItem(bar)
```

> **Cartography check:** a scale bar on a **world** map is wrong almost everywhere on the map, because scale varies hugely across a world projection. Leave it out on small-scale maps. A **north arrow** on a world map is meaningless too. Code makes it easy to add everything, but it's still your job to decide.

### North arrow

```python
from qgis.core import QgsLayoutItemPicture, QgsPathResolver, QgsSymbolLayerUtils

arrow = QgsLayoutItemPicture(layout)
arrow.setPicturePath(QgsSymbolLayerUtils.svgSymbolNameToPath(
    "arrows/NorthArrow_02.svg", QgsPathResolver()))      # one of QGIS's built-in SVGs
arrow.attemptResize(QgsLayoutSize(8, 12, MM))
arrow.attemptMove(QgsLayoutPoint(185, 33, MM))
arrow.setLinkedMap(main)                                  # rotates if the map is rotated
layout.addLayoutItem(arrow)
```

Your own SVG works the same way: `arrow.setPicturePath(r"D:\Maps\symbols\my_north.svg")`.

## 4. Inset (locator) map and info boxes

```python
from qgis.core import QgsLayoutItemMapOverview

inset = QgsLayoutItemMap(layout)
inset.attemptMove(QgsLayoutPoint(150, 180, MM))
inset.attemptResize(QgsLayoutSize(45, 45, MM))
inset.setCrs(countries.crs())
inset.setLayers([countries])
inset.setKeepLayerSet(True)
inset.zoomToExtent(QgsRectangle(-95, -60, -30, 15))       # South America, in degrees
inset.setFrameEnabled(True)
layout.addLayoutItem(inset)

frame = QgsLayoutItemMapOverview("where", inset)
frame.setLinkedMap(main)                                   # draws main's extent on the inset
inset.overviews().addOverview(frame)
```

An **info box** is a shape with a label on top of it:

```python
from qgis.core import QgsFillSymbol, QgsLayoutItemShape

box = QgsLayoutItemShape(layout)
box.setShapeType(QgsLayoutItemShape.Shape.Rectangle)
box.setSymbol(QgsFillSymbol.createSimple({"color": "255,255,255,230",
                                          "outline_color": "#9a958a", "outline_width": "0.2"}))
box.attemptMove(QgsLayoutPoint(15, 245, MM))
box.attemptResize(QgsLayoutSize(85, 35, MM))
layout.addLayoutItem(box)       # add the box BEFORE its text, so the text is on top
```

## 5. Export, and check it

```python
from qgis.core import QgsLayoutExporter

exporter = QgsLayoutExporter(layout)

pdf = QgsLayoutExporter.PdfExportSettings()
pdf.dpi = 300
result = exporter.exportToPdf(str(OUTPUT / "peru.pdf"), pdf)

png = QgsLayoutExporter.ImageExportSettings()
png.dpi = 150
result_png = exporter.exportToImage(str(OUTPUT / "peru.png"), png)

if result != QgsLayoutExporter.ExportResult.Success:
    raise RuntimeError(f"PDF export failed: {result}")
```

`exportToPdf` doesn't raise an error when it fails. It **returns** a code. Code that ignores the return value can report success while no PDF exists. Check it, and check the file exists.

Useful PDF settings: `pdf.rasterizeWholeImage = False` (keep vectors), `pdf.forceVectorOutput = True`, `pdf.appendGeoreference = True` (a GeoPDF), `pdf.exportMetadata = True`.

> A harmless `ERROR 6: The PNG driver does not support update access` message may appear in the console when exporting PNGs. It comes from GDAL trying to write georeferencing into the PNG. The image is still fine. Set `png.generateWorldFile = False` and `png.exportMetadata = False` if you don't need them.

## 6. Templates (`.qpt`): design once, fill by code

Save the finished layout as a template:

```python
from qgis.core import QgsReadWriteContext
layout.saveAsTemplate(str(OUTPUT / "country_sheet.qpt"), QgsReadWriteContext())
```

Then load it and change only what differs:

```python
from qgis.PyQt.QtXml import QDomDocument

doc = QDomDocument()
doc.setContent((OUTPUT / "country_sheet.qpt").read_text(encoding="utf-8"))
sheet = QgsPrintLayout(project)
items, ok = sheet.loadFromTemplate(doc, QgsReadWriteContext())

main = sheet.itemById("main_map")          # ← why you give items an id
title = sheet.itemById("title")
title.setText("Kenya")
```

**Templates remember layers by their internal ID.** If you load a template into a *different* project (or after reloading the layers), the map items and a frozen legend point to IDs that no longer exist, so the map comes out empty. Reconnect them after loading:

```python
main.setLayers([places, rivers, lakes, countries])
legend_root = sheet.itemById("legend").model().rootGroup()
legend_root.clear()
for lyr in [places, rivers, lakes, countries]:
    legend_root.addLayer(lyr)
```

**A powerful split of work:** design the template **by hand** in the Layout designer (fonts, boxes, exact positions, which is where your eye matters), give each item an id (*Item Properties → Id*), and let code fill in extents, scales, texts and exports. In practice this is often better than building the whole layout in code.

## 7. Atlas: one page per feature

```python
atlas = sheet.atlas()
atlas.setCoverageLayer(countries)
atlas.setFilterFeatures(True)
atlas.setFilterExpression("\"continent\" = 'South America'")
atlas.setSortFeatures(True)
atlas.setSortExpression('"name"')
atlas.setFilenameExpression("'sheet_' || \"adm0_a3\"")
atlas.setEnabled(True)

main.setAtlasDriven(True)
main.setAtlasScalingMode(QgsLayoutItemMap.AtlasScalingMode.Auto)   # fit each feature
main.setAtlasMargin(0.10)                                           # 10% margin

count = atlas.updateFeatures()                   # how many pages it will make
result, error = QgsLayoutExporter.exportToPdf(atlas, str(OUTPUT / "atlas.pdf"), pdf)    # one file
result, error = QgsLayoutExporter.exportToPdfs(atlas, str(OUTPUT / "sheets"), pdf)      # one per page
```

Two settings make atlas pages look designed rather than automatic:

```python
# only "nice" scales: each page uses the first one that fits
main.setAtlasScalingMode(QgsLayoutItemMap.AtlasScalingMode.Predefined)
sheet.renderContext().setPredefinedScales([1_000_000, 2_500_000, 5_000_000, 10_000_000, 25_000_000])

# a scale bar whose segments adapt to each page's scale
bar.setSegmentSizeMode(Qgis.ScaleBarSegmentSizeMode.FitWidth)
bar.setMinimumBarWidth(30)
bar.setMaximumBarWidth(45)
```

To highlight "this page's country", give the coverage layer a rule-based style whose rule is `$id = @atlas_featureid`.

On atlas pages, labels with `[% "name" %]` show the current feature's value. The expression variable `@atlas_featurenumber` gives the page number.

**Atlas limits:** every page shares one map CRS. For pages that each need their own CRS or a hand-picked scale (like your 1:85,000 atlas frame), loop in Python instead: for each feature, set the extent, CRS and texts, then export. Exercise 08_2 builds exactly that loop's body.

---

## Exercises

| File | Practises |
|---|---|
| `ex08_1_world_map.py` | an A4 landscape world map in Equal Earth: title, legend, source note, PDF + PNG (and *no* scale bar, on purpose) |
| `ex08_2_country_sheet.py` | a full A4 portrait country sheet: UTM, nice scale, inset, scale bar, north arrow, info box, template |
| `ex08_3_atlas.py` | load the template and export an atlas of South America (13 pages) |

Open the PDFs and *look*. Your eye is the final test of any map, however it was made.

## Checkpoint

1. In layout coordinates, where is y = 0?
2. You set a map item's extent with a rectangle taken straight from the countries layer, but the map item is in EPSG:32718. What goes wrong?
3. Why give layout items ids?
4. `exportToPdf` returned a value and no error appeared. Why check the return value anyway?
5. When should you loop in Python instead of using an atlas?

<details><summary>Answers</summary>

1. The top edge of the page. y grows downwards.
2. The rectangle is in degrees (−81…−68), but the map expects metres, so the map shows a tiny area near the UTM origin. Transform the extent to the map's CRS first.
3. So code can find them in a template with `layout.itemById("...")`.
4. Failures are reported through the return value, not as exceptions.
5. When each page needs a different CRS, a fixed hand-picked scale, or other per-page logic the atlas can't express.

</details>

## 🤖 With Claude

Make a template **by hand** in the Layout designer (your own fonts and boxes) and give the items ids. Then ask Claude: *"Here are the item ids in my template: main_map, title, info_text, inset. Write PyQGIS (3.40, 4.x compatible) that loads the template and exports one PDF per country in this list, setting the title and the info text, with the map in each country's UTM zone at a nice scale."* Review its code before you run it, using Module 11's checklist.

**Next:** [Module 09: Reusable tools and QGIS 4](../09-reusable-tools/README.md)
