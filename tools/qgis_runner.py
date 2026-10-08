"""
Course maintenance tool - you do NOT need this to take the course.

Runs a course script outside the QGIS window ("headless"), the way the
QGIS Python console would run it, so every solution can be tested
automatically on several QGIS versions.

Usage (from a terminal where QGIS's Python is available):
    python tools/qgis_runner.py modules/04-layers-and-projects/solutions/ex04_1_load_layers.py
"""
import os
import sys
import runpy
from pathlib import Path
from unittest.mock import MagicMock

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from qgis.core import QgsApplication, QgsExpressionContextUtils, QgsProject  # noqa: E402

COURSE = Path(__file__).resolve().parents[1]

app = QgsApplication([], False)
app.initQgis()

# The global variable that 00-setup/setup_course.py creates in real QGIS
QgsExpressionContextUtils.setGlobalVariable("course_root", str(COURSE))

# Make Processing available, as it is inside QGIS
qgis_python = Path(QgsApplication.pkgDataPath()) / "python" / "plugins"
sys.path.append(str(qgis_python))
from processing.core.Processing import Processing  # noqa: E402
from qgis.analysis import QgsNativeAlgorithms  # noqa: E402

Processing.initialize()
if not QgsApplication.processingRegistry().providerById("native"):
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

# A stand-in for `iface` (the QGIS window), which does not exist headless.
import qgis.utils  # noqa: E402

qgis.utils.iface = MagicMock(name="iface")

# Same automatic imports as the QGIS Python console
console_globals = {"__name__": "__main__"}
exec(
    "import sys, os, re, math\n"
    "from pathlib import Path\n"
    "from qgis.core import *\n"
    "from qgis.gui import *\n"
    "from qgis.analysis import *\n"
    "import processing\n"
    "from qgis.utils import iface\n"
    "from qgis.PyQt.QtCore import *\n"
    "from qgis.PyQt.QtGui import *\n"
    "from qgis.PyQt.QtWidgets import *\n",
    console_globals,
)

script = Path(sys.argv[1]).resolve()
console_globals["__file__"] = str(script)
code = compile(script.read_text(encoding="utf-8"), str(script), "exec")
exit_code = 0
try:
    exec(code, console_globals)
except SystemExit as e:
    exit_code = int(e.code or 0)
except Exception:
    import traceback

    traceback.print_exc()
    exit_code = 1
finally:
    QgsProject.instance().clear()
    # exitQgis() can crash some headless builds; leave the process directly
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(exit_code)
