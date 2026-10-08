"""
check_code.py - a small "second pair of eyes" for PyQGIS scripts.

It scans a .py file for:
  * QGIS 4 problems   - code that works in QGIS 3 but breaks (or is deprecated) in 4.x
  * AI red flags      - patterns that often mean a silent bug (Modules 04-08, 11)

It is a simple text scan, not a real code analyser: it can miss problems and it
can flag lines that are actually fine. Treat every finding as a QUESTION to check,
not a verdict.

How to use it in QGIS:
  1. Open this file in the Python editor.
  2. Put the path of the script you want to check on the FILE_TO_CHECK line.
  3. Run Script.

From another script:
    findings = check_file(path)        # list of (line_number, kind, message, code)
"""
import re
from pathlib import Path

FILE_TO_CHECK = r""   # e.g. r"D:\PythonCourse\modules\09-reusable-tools\exercises\ex09_3_modernise.py"

# (regular expression, kind, message)
RULES = [
    # --- QGIS 4 / Qt6 compatibility -------------------------------------------------
    (r"\b(from|import)\s+PyQt5\b", "QGIS4",
     "PyQt5 import - use qgis.PyQt (works in QGIS 3 and 4)"),
    (r"\bQVariant\.(Int|Double|String|LongLong|Bool|Date|DateTime|UInt)\b", "QGIS4",
     "QVariant field type - use QMetaType.Type.Int / .Double / .QString ..."),
    (r"\.exec_\(", "QGIS4", "exec_() - use exec() (Qt6 removed exec_)"),
    (r"\bQt\.(?!\w+\.)[A-Z]\w*", "QGIS4",
     "unscoped Qt enum - use the full name, e.g. Qt.AlignmentFlag.AlignLeft"),
    (r"\bQgsWkbTypes\.(Point|Line|Polygon|Unknown|Null)Geometry\b", "QGIS4",
     "old geometry type enum - use Qgis.GeometryType.Point / .Line / .Polygon"),
    (r"\bQgsSimpleMarkerSymbolLayerBase\.[A-Z]\w+", "QGIS4",
     "old marker shape enum - use Qgis.MarkerShape.Star / .Circle ..."),
    (r"\bQgsUnitTypes\.(Distance|Area|Layout|Render)[A-Z]\w+", "QGIS4",
     "old unit enum - use Qgis.DistanceUnit.Meters / Qgis.LayoutUnit.Millimeters ..."),
    (r"\bQgsProcessing\.Type\w+", "QGIS4",
     "old source type - use Qgis.ProcessingSourceType.VectorAnyGeometry ..."),
    (r"\bQgsProcessingParameterNumber\.(Double|Integer)\b", "QGIS4",
     "old number type - use Qgis.ProcessingNumberParameterType.Double / .Integer"),
    (r"\bQgsMapLayerRegistry\b", "QGIS4", "QGIS 2 API - use QgsProject.instance()"),
    (r"\bprocessing\.runalg\b", "QGIS4", "QGIS 2 API - use processing.run()"),
    (r"\bwriteAsVectorFormat\(", "QGIS4",
     "old writer - use QgsVectorFileWriter.writeAsVectorFormatV3(...)"),
    (r"\bsetAutoUpdateModel\(", "QGIS4",
     "deprecated in QGIS 4 - use setSyncMode(Qgis.LegendSyncMode.Manual) where it exists"),
    (r"QtWidgets\s+import\s+.*\bQAction\b", "QGIS4", "QAction lives in QtGui in Qt6"),
    # --- AI red flags ----------------------------------------------------------------
    (r"except\s*(Exception)?\s*:\s*(pass)?\s*$", "RED FLAG",
     "catches every error - make sure it is not hiding failures (except: pass)"),
    (r"[\"']DISTANCE[\"']\s*:\s*0?\.\d+", "RED FLAG",
     "buffer distance below 1 - degrees? Buffer in a projected CRS (metres)"),
    (r"\.buffer\(\s*0?\.\d+", "RED FLAG",
     "geometry.buffer() below 1 - degrees? Buffer in a projected CRS (metres)"),
    (r"\.area\(\)|\.length\(\)", "CHECK",
     "geometry.area()/length() use the layer's units - in EPSG:4326 that's degrees; "
     "use QgsDistanceArea or a projected CRS"),
    (r"#[0-9a-fA-F]{8}\b", "RED FLAG",
     "8-digit hex colour - QGIS reads #AARRGGBB (alpha FIRST), not CSS #RRGGBBAA"),
    (r"(?<![rRbBfF])[\"'][A-Za-z]:\\", "RED FLAG",
     "Windows path without r\"...\" - backslashes like \\n or \\t will break it"),
    (r"\]\s+is\s+(not\s+)?None\b", "RED FLAG",
     "attribute 'is None' - in QGIS 3 NULL is not None; use QgsVariantUtils.isNull()"),
    (r"\bstartEditing\(\)", "RED FLAG",
     "startEditing() - is there a commitChanges()? Prefer 'with edit(layer):'"),
    (r"exportTo(Pdf|Image|Svg)\(", "CHECK",
     "export call - is the returned result checked against ExportResult.Success?"),
    (r"\bQgsVectorLayer\(", "CHECK", "layer created - is isValid() checked?"),
]


def check_file(path):
    """Return a list of (line_number, kind, message, code_line) for one .py file."""
    findings = []
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    for number, line in enumerate(lines, start=1):
        code = re.sub(r"(^|\s)#\s.*$", "", line)      # drop "# comments" (keeps "#ff0000")
        if not code.strip():
            continue
        for pattern, kind, message in RULES:
            if re.search(pattern, code):
                findings.append((number, kind, message, line.strip()))
    return findings


def print_report(path):
    findings = check_file(path)
    print(f"Checked {Path(path).name}: {len(findings)} finding(s)")
    for number, kind, message, code in findings:
        print(f"  line {number:>4}  [{kind}]  {message}")
        print(f"             {code[:90]}")
    if not findings:
        print("  nothing found - which does NOT prove the code is right. Run it and verify.")
    return findings


if __name__ in ("__main__", "__console__") and FILE_TO_CHECK:
    print_report(FILE_TO_CHECK)
