"""
MODULE 11 - Review 2 (solution): population density

PROBLEMS FOUND
  1. startEditing() with no commitChanges(): the edits live only in memory and
     are thrown away when the script ends. NOTHING is saved, yet it prints
     "Density added!".                         (checklist 6: silent failure)
  2. f.geometry().area() on EPSG:4326 = square DEGREES. Peru would get
     ~32,000,000 "people per km2".             (checklist 4: units)
  3. Bare `except: pass` hides the ZeroDivisionError for pop_est = 0 - and
     would hide ANY other error too. Handle the zero case on purpose.
                                               (checklist 6)
  4. PyQt5 + QVariant.Double break in QGIS 4 (the request asked for both).
     Use qgis.PyQt and QMetaType.Type.Double.  (checklist 2: version)
  Also fine to note: shutil.copy copies all nine layers of the GeoPackage.
  That's harmless here; writing just the countries layer would be leaner.
"""
import shutil
from pathlib import Path

from qgis.core import (QgsDistanceArea, QgsExpressionContextUtils, QgsField, QgsProject,
                       QgsVectorLayer, edit)
from qgis.PyQt.QtCore import QMetaType

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA = COURSE / "data"
OUTPUT = COURSE / "output"
OUTPUT.mkdir(exist_ok=True)

src = DATA / "natural_earth.gpkg"
dst = OUTPUT / "countries_density.gpkg"
shutil.copy(src, dst)                       # a copy - the source stays untouched

layer = QgsVectorLayer(f"{dst}|layername=countries", "countries", "ogr")
if not layer.isValid():
    raise RuntimeError(f"could not open {dst}")

da = QgsDistanceArea()
da.setSourceCrs(layer.crs(), QgsProject.instance().transformContext())
da.setEllipsoid("EPSG:7030")

with edit(layer):                           # commits at the end (or rolls back on error)
    layer.addAttribute(QgsField("density", QMetaType.Type.Double))
layer.updateFields()
idx = layer.fields().indexOf("density")

with edit(layer):
    for f in layer.getFeatures():
        km2 = da.measureArea(f.geometry()) / 1e6
        pop = f["pop_est"]
        density = round(pop / km2, 2) if pop > 0 and km2 > 0 else None   # None -> NULL
        layer.changeAttributeValue(f.id(), idx, density)

print("Density added and saved to", dst.name)

check = QgsVectorLayer(f"{OUTPUT / 'countries_density.gpkg'}|layername=countries", "check", "ogr")
assert check.fields().indexOf("density") >= 0, "the field was never SAVED to the file"
peru = next(check.getFeatures("\"adm0_a3\" = 'PER'"))
assert 24 < peru["density"] < 26, f"Peru density {peru['density']} (should be ~25 people/km2)"
assert len(list(check.getFeatures('"density" IS NULL'))) == 2, "zero-population -> NULL"
print("All checks passed ✔")
