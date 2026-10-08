"""
MODULE 11 - Review 2: population density

THE REQUEST
    "Make a copy of the countries layer in output/countries_density.gpkg and add
     a 'density' field: people per km2. Leave it empty where population is 0.
     QGIS 3.40, and it should keep working in QGIS 4."

THE AI'S ANSWER is below. It prints "Density added!".

YOUR JOB: review (# PROBLEM: ...), run, then fix until the checks pass.
Hint: there are FOUR problems. One of them means nothing is saved at all.
"""
import shutil
from pathlib import Path

from PyQt5.QtCore import QVariant
from qgis.core import QgsExpressionContextUtils, QgsField, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA = COURSE / "data"
OUTPUT = COURSE / "output"
OUTPUT.mkdir(exist_ok=True)

# ======================= the AI's code starts here ==============================
src = DATA / "natural_earth.gpkg"
dst = OUTPUT / "countries_density.gpkg"
shutil.copy(src, dst)

layer = QgsVectorLayer(f"{dst}|layername=countries", "countries", "ogr")
layer.startEditing()
layer.addAttribute(QgsField("density", QVariant.Double))
layer.updateFields()
idx = layer.fields().indexOf("density")

for f in layer.getFeatures():
    try:
        density = f["pop_est"] / f.geometry().area()
        layer.changeAttributeValue(f.id(), idx, density)
    except:
        pass

print("Density added!")
# ======================= the AI's code ends here ================================

# --- Checks (don't edit below this line) ------------------------------------
check = QgsVectorLayer(f"{OUTPUT / 'countries_density.gpkg'}|layername=countries", "check", "ogr")
assert check.fields().indexOf("density") >= 0, "the field was never SAVED to the file"
peru = next(check.getFeatures("\"adm0_a3\" = 'PER'"))
assert 24 < peru["density"] < 26, f"Peru density {peru['density']} (should be ~25 people/km2)"
assert len(list(check.getFeatures('"density" IS NULL'))) == 2, "zero-population -> NULL"
print("All checks passed ✔")
