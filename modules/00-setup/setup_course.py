"""
MODULE 00 - Run this once.

What it does:
  1. Works out where the course folder is on your computer.
  2. Saves that location in a QGIS *global variable* called  course_root
     (you can see it in Settings > Options > Variables).
  3. Checks that the course data is there and creates the output folder.

How to run it:
  In QGIS: Plugins > Python Console > "Show Editor" button > "Open Script..."
  > choose this file > click the green "Run Script" triangle.

If it says it can't find the course folder, type the folder path between
the quotes on the COURSE_FOLDER line below, save, and run again.
"""
from pathlib import Path

from qgis.core import Qgis, QgsExpressionContextUtils

COURSE_FOLDER = r""  # e.g. r"D:\PythonCourse"  (leave empty to detect automatically)

# --- 1. find the course folder ---------------------------------------------
if COURSE_FOLDER:
    course = Path(COURSE_FOLDER)
else:
    # __file__ is the path of this script, when it is run from a saved file
    course = Path(__file__).resolve().parents[2]

data_file = course / "data" / "natural_earth.gpkg"

if not data_file.exists():
    print("I could not find the course data at:", data_file)
    print("Fix: type your course folder on the COURSE_FOLDER line, save, run again.")
else:
    # --- 2. remember it in QGIS -------------------------------------------
    QgsExpressionContextUtils.setGlobalVariable("course_root", str(course))

    # --- 3. make the output folder ------------------------------------------
    output = course / "output"
    output.mkdir(exist_ok=True)

    print("Course folder :", course)
    print("Data found    :", data_file.name)
    print("Output folder :", output)
    print("QGIS version  :", Qgis.version())
    print()
    print("All set. Every exercise starts by reading 'course_root',")
    print("so you never need to type the folder path again.")
