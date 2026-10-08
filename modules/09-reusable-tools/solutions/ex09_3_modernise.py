"""MODULE 09 - Solution 3: the same script, QGIS-4-ready (runs in 3.40 and 4.x)"""
from pathlib import Path

from qgis.PyQt.QtCore import QMetaType, Qt                    # was: PyQt5 + QVariant
from qgis.PyQt.QtGui import QColor
from qgis.core import (Qgis, QgsExpressionContextUtils, QgsFeatureRequest, QgsField,
                       QgsLayoutItemLabel, QgsLayoutPoint, QgsMarkerSymbol, QgsPrintLayout,
                       QgsProject, QgsSingleSymbolRenderer, QgsVectorLayer, edit)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"

places = QgsVectorLayer(f"{GPKG}|layername=places", "places", "ogr")
if not places.isValid():
    raise RuntimeError("places did not load")
work = places.materialize(QgsFeatureRequest().setFilterExpression("\"adm0_a3\" = 'PER'"))

# 1. QVariant.String -> QMetaType.Type.QString
with edit(work):
    work.addAttribute(QgsField("label", QMetaType.Type.QString))

# 2. QgsWkbTypes.PointGeometry -> Qgis.GeometryType.Point
is_points = work.geometryType() == Qgis.GeometryType.Point

# 3. QgsSimpleMarkerSymbolLayerBase.Star -> Qgis.MarkerShape.Star
symbol = QgsMarkerSymbol.createSimple({"color": "#b03a2e", "size": "2.5"})
symbol.symbolLayer(0).setShape(Qgis.MarkerShape.Star)
work.setRenderer(QgsSingleSymbolRenderer(symbol))

# 4. Qt.AlignHCenter -> Qt.AlignmentFlag.AlignHCenter,
#    QgsUnitTypes.LayoutMillimeters -> Qgis.LayoutUnit.Millimeters
layout = QgsPrintLayout(QgsProject.instance())
layout.initializeDefaults()
title = QgsLayoutItemLabel(layout)
title.setText("Cities of Peru")
title.setHAlign(Qt.AlignmentFlag.AlignHCenter)
title.attemptMove(QgsLayoutPoint(10, 10, Qgis.LayoutUnit.Millimeters))
layout.addLayoutItem(title)

print("points?", is_points, "| features:", work.featureCount())

import importlib.util
spec = importlib.util.spec_from_file_location("check_code", COURSE / "tools" / "check_code.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
problems = [f for f in checker.check_file(__file__) if f[1] == "QGIS4"
            and "check_code" not in f[3]]
for line_no, kind, message, code in problems:
    print(f"  still to fix - line {line_no}: {message}")
assert not problems, f"{len(problems)} QGIS 4 problem(s) left (see above). Did you save?"
assert is_points and work.featureCount() == 11
assert work.fields().indexOf("label") >= 0
assert title.hAlign() == Qt.AlignmentFlag.AlignHCenter
print("All checks passed ✔  - this script now runs in QGIS 3.40 and 4.x")
