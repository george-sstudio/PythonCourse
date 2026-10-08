"""MODULE 00 - Solution: your first script (only the layer name changed)."""
from pathlib import Path

from qgis.core import QgsExpressionContextUtils, QgsProject, QgsVectorLayer

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA = COURSE / "data"

uri = f"{DATA / 'natural_earth.gpkg'}|layername=countries"
layer = QgsVectorLayer(uri, "My first layer", "ogr")

if layer.isValid():
    QgsProject.instance().addMapLayer(layer)
    print("Added", layer.name(), "with", layer.featureCount(), "countries")
else:
    print("The layer did not load. Did you run setup_course.py?")
