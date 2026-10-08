"""
MODULE 09 - Exercise 3: make an old script QGIS-4-ready

This script WORKS in QGIS 3.40 (try it), but it's written in the old style that
AI often produces, and it breaks in QGIS 4.

  1. Run tools/check_code.py on this file (set FILE_TO_CHECK to this file's path).
  2. Fix every [QGIS4] finding. Use the table in the module README.
  3. Save, then Run Script: the checks at the bottom re-scan THIS file and
     must find no QGIS4 problems - and the map item must still work.
"""
from pathlib import Path

from PyQt5.QtCore import QVariant, Qt
from PyQt5.QtGui import QColor
from qgis.core import (QgsExpressionContextUtils, QgsFeatureRequest, QgsField,
                       QgsLayoutItemLabel, QgsLayoutPoint, QgsMarkerSymbol, QgsPrintLayout,
                       QgsProject, QgsSimpleMarkerSymbolLayerBase, QgsSingleSymbolRenderer,
                       QgsUnitTypes, QgsVectorLayer, QgsWkbTypes, edit)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"

places = QgsVectorLayer(f"{GPKG}|layername=places", "places", "ogr")
if not places.isValid():
    raise RuntimeError("places did not load")
work = places.materialize(QgsFeatureRequest().setFilterExpression("\"adm0_a3\" = 'PER'"))

# 1. a new text field
with edit(work):
    work.addAttribute(QgsField("label", QVariant.String))

# 2. geometry type check
is_points = work.geometryType() == QgsWkbTypes.PointGeometry

# 3. star markers
symbol = QgsMarkerSymbol.createSimple({"color": "#b03a2e", "size": "2.5"})
symbol.symbolLayer(0).setShape(QgsSimpleMarkerSymbolLayerBase.Star)
work.setRenderer(QgsSingleSymbolRenderer(symbol))

# 4. a centred layout label
layout = QgsPrintLayout(QgsProject.instance())
layout.initializeDefaults()
title = QgsLayoutItemLabel(layout)
title.setText("Cities of Peru")
title.setHAlign(Qt.AlignHCenter)
title.attemptMove(QgsLayoutPoint(10, 10, QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(title)

print("points?", is_points, "| features:", work.featureCount())

# --- Checks (don't edit below this line) ------------------------------------
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
