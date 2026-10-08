"""
MODULE 11 - Review 5: a map of Kenya

THE REQUEST
    "A4 portrait PDF of Kenya at exactly 1:5,000,000 in UTM zone 37N, with a
     title and a semi-transparent WHITE box (70% opaque) for notes in the lower
     left. Save as output/kenya.pdf. QGIS 3.40."

THE AI'S ANSWER is below. It prints "Map exported to kenya.pdf".

YOUR JOB: review (# PROBLEM: ...), run, open the PDF, then fix until the
checks pass. Hint: four problems. Look at the ORDER of the map-item lines.
"""
from pathlib import Path

from qgis.core import (Qgis, QgsCoordinateReferenceSystem, QgsExpressionContextUtils,
                       QgsFillSymbol, QgsLayoutExporter, QgsLayoutItemLabel, QgsLayoutItemMap,
                       QgsLayoutItemPage, QgsLayoutItemShape, QgsLayoutPoint, QgsLayoutSize,
                       QgsPrintLayout, QgsProject, QgsVectorLayer)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
OUTPUT = COURSE / "output"
OUTPUT.mkdir(exist_ok=True)
MM = Qgis.LayoutUnit.Millimeters
project = QgsProject.instance()
project.clear()

# ======================= the AI's code starts here ==============================
countries = QgsVectorLayer(f"{GPKG}|layername=countries", "countries", "ogr")
project.addMapLayer(countries)
kenya = next(countries.getFeatures("\"adm0_a3\" = 'KEN'"))

layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.pageCollection().page(0).setPageSize("A4", QgsLayoutItemPage.Orientation.Portrait)

main = QgsLayoutItemMap(layout)
main.attemptMove(QgsLayoutPoint(10, 25, MM))
main.attemptResize(QgsLayoutSize(190, 240, MM))
main.setCrs(QgsCoordinateReferenceSystem("EPSG:32637"))
main.setScale(5_000_000)
main.zoomToExtent(kenya.geometry().boundingBox())
main.setLayers([countries])
layout.addLayoutItem(main)

title = QgsLayoutItemLabel(layout)
title.setText("Kenya")
title.attemptMove(QgsLayoutPoint(10, 8, MM))
title.attemptResize(QgsLayoutSize(150, 12, MM))
layout.addLayoutItem(title)

box = QgsLayoutItemShape(layout)
box.setShapeType(QgsLayoutItemShape.Shape.Rectangle)
box.setSymbol(QgsFillSymbol.createSimple({"color": "#ffffffb3", "outline_style": "no"}))
box.attemptMove(QgsLayoutPoint(15, 230, MM))
box.attemptResize(QgsLayoutSize(70, 30, MM))
layout.addLayoutItem(box)

QgsLayoutExporter(layout).exportToPdf(str(OUTPUT / "kenya.pdf"),
                                      QgsLayoutExporter.PdfExportSettings())
print("Map exported to kenya.pdf")
# ======================= the AI's code ends here ================================

# --- Checks (don't edit below this line) ------------------------------------
from qgis.core import QgsCoordinateTransform, QgsPointXY
to_map = QgsCoordinateTransform(countries.crs(), main.crs(), project)
nairobi = to_map.transform(QgsPointXY(36.82, -1.29))
fill = box.symbol().color()
print(f"map scale 1:{main.scale():,.0f} | Nairobi on the map? {main.extent().contains(nairobi)}"
      f" | box colour {fill.name()} alpha {fill.alpha()}")
assert main.crs().authid() == "EPSG:32637"
assert main.extent().contains(nairobi), "Nairobi is not on the map - check the extent's CRS"
assert round(main.scale()) == 5_000_000, f"scale is 1:{main.scale():,.0f}"
assert fill.name() == "#ffffff" and 175 <= fill.alpha() <= 180, "white at 70% (alpha ~179)"
assert (OUTPUT / "kenya.pdf").exists()
print("All checks passed ✔")
