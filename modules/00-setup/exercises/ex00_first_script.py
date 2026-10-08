"""
MODULE 00 - Exercise: your first script

Goal: run a script that adds the world's countries to your map,
then change ONE thing and run it again.

Steps:
  1. Open this file in the QGIS Python editor and click Run Script.
     A layer called "countries" should appear.
  2. Read the comments line by line. Every line starting with # is a
     comment: Python ignores it. It's there for humans.
  3. TODO: change the layer name "countries" (inside the quotes on the
     line marked TODO) to "My first layer". Save (Ctrl+S) and run again.
     A second layer with your new name appears.
"""
from pathlib import Path

from qgis.core import QgsExpressionContextUtils, QgsProject, QgsVectorLayer

# Where is the course? (setup_course.py saved this for us)
COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA = COURSE / "data"

# Build the "address" of one layer inside the GeoPackage file
uri = f"{DATA / 'natural_earth.gpkg'}|layername=countries"

# Create a layer object from that address
layer = QgsVectorLayer(uri, "countries", "ogr")  # TODO: change the name

# Check it worked before using it (a habit you'll keep all course)
if layer.isValid():
    QgsProject.instance().addMapLayer(layer)
    print("Added", layer.name(), "with", layer.featureCount(), "countries")
else:
    print("The layer did not load. Did you run setup_course.py?")
