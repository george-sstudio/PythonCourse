# Module 09: Reusable tools, and getting ready for QGIS 4

**Time:** about 3 hours · **Week 3** · Book: Ch. 2–3 mention "Create New Script from Template". This module goes the rest of the way.

A script you rerun by editing paths at the top is half-automation. A **Processing tool** has a dialog, works in **batch mode** and the **Model Designer**, can be shared as one file, and can be called from other scripts. This module also makes your code survive the move from QGIS 3.40 to QGIS 4.

## You will

- turn copy-pasted code into small functions, and import your own helper files
- write a Processing tool (a `QgsProcessingAlgorithm`): parameters, progress, child tools, output
- test the tool from code **before** installing it, then install it in the Toolbox
- know the QGIS 3 → 4 changes that affect scripts, and check code for them automatically

## Key words

| Word | Meaning |
|---|---|
| **Refactor** | Rewrite code so it's clearer, without changing what it does. |
| **Module (your own)** | A `.py` file of functions that other scripts `import`. |
| **Processing tool / algorithm** | A class with fixed parts (`name`, `initAlgorithm`, `processAlgorithm`…) that QGIS turns into a Toolbox tool with a dialog. |
| **Parameter** | One input or output of a tool (layer, number, boolean, output file…). |
| **Sink** | Processing's word for "where the output features go", whatever the user chose: a temporary layer, a GeoPackage, a shapefile. |
| **Child algorithm** | A tool run *inside* your tool (`is_child_algorithm=True`). |
| **Feedback** | The object for talking to the user while running: messages, progress bar, the Cancel button. |
| **Qt5 / Qt6** | The toolkit QGIS is built on. QGIS 3 uses Qt5, QGIS 4 uses Qt6. Most script changes come from that switch. |
| **Deprecated** | Still works, but is marked for removal. Change it before it breaks. |

---

## 1. Functions first

Exercise 1 starts with typical first-draft code: the same five lines copied for every layer. The fix is always the same:

1. Find the lines that repeat.
2. Name what they *do*: `load_layer`, `style_fill`, `save_style`.
3. Turn the parts that change into **parameters**.
4. Put the varying data in a list and **loop**.

```python
PLAN = [("ocean", "#dfe8ee"), ("countries", "#f1ede4"), ("lakes", "#dfe8ee")]
for name, colour in PLAN:
    layer = load_layer(name)
    style_fill(layer, colour)
    save_style(layer)
```

Now a bug fix or a new rule ("every layer gets 0.1 mm white outlines") goes in **one** place.

### Your own helper module

Put functions you reuse in a file, e.g. `D:\PythonCourse\my_tools\map_helpers.py`, then:

```python
import sys, importlib
sys.path.append(r"D:\PythonCourse\my_tools")   # tell Python where to look
import map_helpers
importlib.reload(map_helpers)                  # pick up edits without restarting QGIS
map_helpers.load_layer("rivers")
```

> **The reload trap:** Python imports a module only **once** per QGIS session. If you edit `map_helpers.py` and `import` it again, you still get the *old* version, and your fix "doesn't work". `importlib.reload(...)` loads it again.

## 2. Anatomy of a Processing tool

Open `solutions/safe_buffer_tool.py` beside this section. It's a tool that buffers by a distance in **metres** whatever the layer's CRS, a permanent fix for red flag #1 from Module 04.

```python
class SafeBufferAlgorithm(QgsProcessingAlgorithm):
    INPUT, DISTANCE, DISSOLVE, OUTPUT = "INPUT", "DISTANCE", "DISSOLVE", "OUTPUT"

    def name(self):          return "safebuffer"              # id → script:safebuffer
    def displayName(self):   return "Buffer in metres (safe)"
    def group(self):         return "PythonCourse"
    def groupId(self):       return "pythoncourse"
    def shortHelpString(self): return "Buffers by metres, even on EPSG:4326 layers..."
    def createInstance(self): return SafeBufferAlgorithm()

    def initAlgorithm(self, config=None):          # the dialog: inputs and outputs
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT, "Input layer", [Qgis.ProcessingSourceType.VectorAnyGeometry]))
        self.addParameter(QgsProcessingParameterNumber(
            self.DISTANCE, "Distance (metres)", Qgis.ProcessingNumberParameterType.Double,
            defaultValue=1000, minValue=0))
        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT, "Buffered", Qgis.ProcessingSourceType.VectorPolygon))

    def processAlgorithm(self, parameters, context, feedback):   # the work
        source = self.parameterAsSource(parameters, self.INPUT, context)
        distance = self.parameterAsDouble(parameters, self.DISTANCE, context)
        ...
        return {self.OUTPUT: dest_id}
```

| Part | Job |
|---|---|
| `name()` … `createInstance()` | identity: how the tool is listed and found |
| `initAlgorithm()` | declares the **parameters**, which become the dialog's fields |
| `processAlgorithm()` | does the work, using `parameterAs…()` to read the user's choices |

Common parameter types: `QgsProcessingParameterFeatureSource` (vector input), `…RasterLayer`, `…Number`, `…Boolean`, `…Enum` (a drop-down), `…Field`, `…String`, `…File`, `…FolderDestination`, `…FeatureSink` (vector output), `…RasterDestination`.

### Inside `processAlgorithm`

**Run other tools as children** so they share the user's context and Cancel button:

```python
step1 = processing.run("native:reprojectlayer",
    {"INPUT": parameters[self.INPUT], "TARGET_CRS": local, "OUTPUT": "TEMPORARY_OUTPUT"},
    context=context, feedback=feedback, is_child_algorithm=True)["OUTPUT"]
```

**Talk to the user:**

```python
feedback.pushInfo(f"Buffering by {distance:g} m")   # a line in the log
feedback.setProgress(50)                            # the progress bar, 0-100
if feedback.isCanceled():                           # the user pressed Cancel
    return {}
```

**Write the output to the sink.** That way the user can pick any output format:

```python
sink, dest_id = self.parameterAsSink(parameters, self.OUTPUT, context,
                                     layer.fields(), layer.wkbType(), source.sourceCrs())
for f in layer.getFeatures():
    sink.addFeature(f, QgsFeatureSink.Flag.FastInsert)
return {self.OUTPUT: dest_id}
```

> **Don't use `iface` inside a tool.** Tools can run in the background, in batch mode, or with no QGIS window at all (`qgis_process`). Everything the tool needs must come in through its parameters.

## 3. Test it from code, *then* install it

```python
import importlib.util
spec = importlib.util.spec_from_file_location("safe_buffer_tool", tool_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)                        # like import, from any path

alg = module.SafeBufferAlgorithm().create()            # create() also runs initAlgorithm()
result = processing.run(alg, {"INPUT": lena, "DISTANCE": 10_000, "OUTPUT": "TEMPORARY_OUTPUT"})
```

`processing.run` accepts an algorithm **object** as well as an id. The test (`ex09_2_test_tool.py`) also checks the answer **independently**: a 10 km buffer around a line of length *L* should cover about 2 × 10 km × *L*. A check that doesn't reuse the code under test is worth a lot (Module 11).

### Installing

*Processing Toolbox → Python icon (Scripts) → Add Script to Toolbox…* → pick the file. It's copied to your profile's scripts folder, which on Windows is:

```text
%APPDATA%\QGIS\QGIS3\profiles\default\processing\scripts\
```

The tool then appears under **Scripts → PythonCourse**. Right-click it → **Execute as Batch Process…** to run it on 20 layers with no extra code, or drag it into the **Model Designer**.

## 4. Running without the QGIS window

Three levels, from simplest:

1. **`qgis_process`** (Module 06): any *built-in* tool from the command line.
2. **A standalone script** run with QGIS's Python (in the OSGeo4W Shell: `python-qgis-ltr my_script.py`). It needs a few lines of setup first. `tools/qgis_runner.py` in this course is a complete working example: it starts QGIS without a window, sets up Processing, then runs a script.
3. **Scheduled runs** (e.g. Windows Task Scheduler running level 2 every night). Only worth it for recurring jobs.

For most map work, levels 0 (the editor) and 1 are enough.

## 5. Getting ready for QGIS 4

**Where things stand (October 2026):** QGIS 4.0 (Qt6) came out in March 2026 and 4.2 in July 2026. The first 4.x long-term release is expected around the end of October 2026, based on 4.2. QGIS 3.44 is the last 3.x LTR. You're on 3.40, so you'll move within the next year or so. The QGIS team kept most of the old API working in 4.x, but not all of it.

Everything in this course already runs on **both** 3.40 and 4.2. These are the changes that matter for scripts:

| QGIS 3 style (old) | Works in 3.40 **and** 4.x |
|---|---|
| `from PyQt5.QtCore import ...` | `from qgis.PyQt.QtCore import ...` |
| `QgsField("x", QVariant.Double)` | `QgsField("x", QMetaType.Type.Double)` (`.QString`, `.Int`, `.LongLong`…) |
| `Qt.AlignLeft`, `Qt.red` | `Qt.AlignmentFlag.AlignLeft`, `Qt.GlobalColor.red` |
| `QgsWkbTypes.PolygonGeometry` | `Qgis.GeometryType.Polygon` |
| `QgsSimpleMarkerSymbolLayerBase.Star` | `Qgis.MarkerShape.Star` |
| `QgsUnitTypes.LayoutMillimeters` | `Qgis.LayoutUnit.Millimeters` |
| `QgsProcessing.TypeVectorPolygon` | `Qgis.ProcessingSourceType.VectorPolygon` |
| `QgsProcessingParameterNumber.Double` | `Qgis.ProcessingNumberParameterType.Double` |
| `dialog.exec_()` | `dialog.exec()` |
| `from qgis.PyQt.QtWidgets import QAction` | `from qgis.PyQt.QtGui import QAction` (Qt6) |
| `if value is None` on attributes | `QgsVariantUtils.isNull(value)` (NULL was `QVariant` in 3, is `None` in 4) |
| `legend.setAutoUpdateModel(False)` | `legend.setSyncMode(Qgis.LegendSyncMode.Manual)` where available (see below) |

### When the new way doesn't exist in 3.40 yet

Check for it, and fall back:

```python
if hasattr(legend, "setSyncMode"):                 # QGIS 4.0+
    legend.setSyncMode(Qgis.LegendSyncMode.Manual)
else:                                              # QGIS 3.x
    legend.setAutoUpdateModel(False)

# or by version number: 34000 = 3.40, 40200 = 4.2
if Qgis.QGIS_VERSION_INT >= 40000:
    ...
```

### `tools/check_code.py`

The course includes a small checker that scans a script for the old patterns above, plus the AI red flags from Weeks 2–3. Open it in the editor, set `FILE_TO_CHECK`, and run it:

```text
Checked ex09_3_modernise.py: 7 finding(s)
  line   14  [QGIS4]  PyQt5 import - use qgis.PyQt (works in QGIS 3 and 4)
  line   31  [QGIS4]  QVariant field type - use QMetaType.Type.Int / .Double / .QString ...
  ...
```

It's a plain text search, so treat each finding as a **question** ("is this OK here?"), not a verdict. Example: it flags `setAutoUpdateModel` even inside the `hasattr` fallback above, where it's correct.

### Moving day checklist

- [ ] Install QGIS 4.x **alongside** 3.40 (the OSGeo4W installer allows both).
- [ ] QGIS 4 has its **own profile folder**, separate from QGIS 3. Copy your Processing scripts, styles and templates across (on first launch it copies the old configuration **once**).
- [ ] Run `check_code.py` on every script you keep.
- [ ] Run each script once in QGIS 4 *on a copy of the data*, and compare outputs with 3.40 (counts, a visual check).

---

## Exercises

| File | Practises |
|---|---|
| `ex09_1_functions.py` | refactor copy-paste into `load_layer`, `style_fill`, `save_style` + a loop |
| `safe_buffer_tool.py` + `ex09_2_test_tool.py` | finish the tool's three steps, test it on the Lena, then install it |
| `ex09_3_modernise.py` | run the checker on an old-style script and make it QGIS-4-ready |

## Checkpoint

1. You edited `map_helpers.py`, re-ran `import map_helpers`, and nothing changed. Why?
2. What are the three main parts of a `QgsProcessingAlgorithm`?
3. Why must a tool not use `iface`?
4. What does `is_child_algorithm=True` do?
5. Name three QGIS 3 → 4 changes that affect scripts.

<details><summary>Answers</summary>

1. Modules load once per session. Use `importlib.reload(map_helpers)`.
2. Identity (`name`, `displayName`…), `initAlgorithm` (the parameters) and `processAlgorithm` (the work).
3. Tools may run in the background, in batch mode, or with no window at all.
4. It runs the inner tool as part of yours, sharing the context, the feedback and the Cancel button.
5. Any three from the table: PyQt5 → `qgis.PyQt`; `QVariant` → `QMetaType` field types; scoped enums (`Qt.AlignmentFlag.AlignLeft`, `Qgis.GeometryType.Polygon`…); `exec_()` → `exec()`; NULL is `None` in 4; `QAction` moved to `QtGui`.

</details>

## 🤖 With Claude

Ask Claude for a Processing tool you'd actually use, e.g. *"a QGIS 3.40 Processing script that applies a QML style file to every layer in the project whose name matches a pattern, with a dry-run option that only lists the matches."* Before running it: run `check_code.py` on it, read every line, and test it on a project **copy**.

**Next:** [Module 10: Briefing the AI](../10-directing-ai/README.md)
