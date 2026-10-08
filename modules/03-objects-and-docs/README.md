# Module 03: Objects and the PyQGIS docs

**Time:** about 3 hours · **Week 1**

PyQGIS is a huge toolbox: thousands of classes and tens of thousands of methods. Nobody memorises it, not even QGIS developers. The real skill is **finding out what an object can do** quickly and reliably, and **checking whether a method the AI used actually exists**. This module teaches that skill, and it works offline.

## You will

- understand **objects**, **classes** and **methods** well enough to read any PyQGIS code
- explore any object with `type()`, `dir()` and `help()`, right in the console
- read a page of the PyQGIS API documentation
- recognise the most important PyQGIS classes by name
- avoid the "it came back empty" trap (`None`, `[]`, invalid layers)

## Key words

| Word | Meaning |
|---|---|
| **Object** | A value bundled with the actions it can do. A layer object knows its name, its CRS and its features, and can do things like `reload()`. |
| **Class** | The blueprint for a kind of object, like a blank form. `QgsVectorLayer` is a class. |
| **Instance** | One object made from a class, like a filled-in form. `layer = QgsVectorLayer(...)` creates an instance. |
| **Constructor** | Calling the class name to make an instance: `QgsVectorLayer(uri, "countries", "ogr")`. |
| **Method** | A function that belongs to an object, called with a dot and brackets: `layer.featureCount()`. |
| **Attribute** (Python) | A value stored on an object, used without brackets: `path.name`. (Not the same as a GIS *attribute* in an attribute table!) |
| **API** | "Application Programming Interface": the list of all the classes and methods a program offers to code. The PyQGIS API is that list for QGIS. |
| **Enum** | A named set of options, e.g. `Qgis.GeometryType.Polygon` / `.Line` / `.Point`. Better than magic numbers. |
| **Singleton** | A class with exactly one instance. `QgsProject.instance()` is *the* currently open project. |

---

## 1. Objects: data plus actions

You've used objects already:

```python
name = "dead sea"
name.upper()             # a str object doing its .upper() action

from pathlib import Path
p = Path(r"D:\PythonCourse\data\natural_earth.gpkg")
p.exists()               # a Path object answering a question
p.name                   # an attribute (no brackets): stored data
```

A QGIS layer is the same idea, only bigger:

```python
from qgis.core import QgsVectorLayer

layer = QgsVectorLayer(r"D:\PythonCourse\data\natural_earth.gpkg|layername=countries",
                       "countries", "ogr")

layer.name()             # 'countries'
layer.featureCount()     # 242
layer.crs()              # another object! a QgsCoordinateReferenceSystem
layer.crs().authid()     # 'EPSG:4326'   (a method of THAT object)
```

That last line is **chaining**: `layer.crs()` returns a CRS object, and `.authid()` is called on it. Read chains left to right: "the layer's CRS's authority ID".

### Class vs instance

```text
QgsVectorLayer                 ← the class (blueprint)
    │
    ├── countries = QgsVectorLayer(...countries...)   ← one instance
    └── rivers    = QgsVectorLayer(...rivers...)      ← another instance
```

Both instances have the same *methods* (`featureCount()`, `crs()`…) but different *data*.

### Brackets matter

```python
layer.name()   # 'countries'                      ← calls the method
layer.name     # <built-in method name of ...>    ← the method itself, not called
```

If you ever see `<built-in method ...>` or `<bound method ...>` printed, you forgot the `()`.

## 2. Exploring an object without the internet

Three console tools work everywhere, offline:

```python
type(layer)            # <class 'qgis._core.QgsVectorLayer'>  - what IS this?

dir(layer)             # every method and attribute name (hundreds!)
[m for m in dir(layer) if "count" in m.lower()]   # filter: names containing "count"
# ['featureCount', ...]

help(layer.featureCount)   # the documentation for one method
```

The console also **autocompletes**: type `layer.feat` and wait, and a list of matching methods pops up.

### Reading a method's signature

`help(layer.setSubsetString)` shows something like:

```text
setSubsetString(self, subset: str) -> bool
```

| Piece | Means |
|---|---|
| `setSubsetString` | method name |
| `self` | the object itself. Ignore it: Python fills it in for you |
| `subset: str` | one parameter, called `subset`, must be **text** |
| `-> bool` | it **returns** `True`/`False` (did it work?) |

That's all the information you need to use it: `ok = layer.setSubsetString("continent = 'Africa'")`.

## 3. The PyQGIS API documentation

The online version is at **qgis.org/pyqgis/3.40/** (pick your version). Each class has a page. For example, the `QgsVectorLayer` page lists:

- **the constructor**: how to create one
- **methods**: grouped, each with its parameters and return type
- **enums**: the named options it uses

**How to look something up (the routine):**

1. Know the **class** of your object: `type(obj)`.
2. Open that class's page (or use `help(obj)` offline).
3. Search the page (`Ctrl+F`) for a word related to what you want: *subset*, *extent*, *style*…
4. Read the **signature**: what goes in, what comes out.
5. Try it in the console on real data.

> **Why this matters with AI:** AI sometimes invents a method that sounds right but doesn't exist (`layer.getArea()`, `layer.setColor()`). One `dir()` check, or one docs lookup, catches this in 10 seconds. In Week 4 this becomes a habit.

## 4. The classes you'll meet most

| Class / object | What it is | Module |
|---|---|---|
| `QgsProject.instance()` | the project that's open now (layers, CRS, layouts) | 04 |
| `iface` | the QGIS **window**: map canvas, active layer, messages. Only exists inside the QGIS app | 04 |
| `QgsVectorLayer`, `QgsRasterLayer` | layers | 04 |
| `QgsCoordinateReferenceSystem` | a CRS | 04 |
| `QgsFeature` | one feature (one row with a geometry) | 05 |
| `QgsGeometry` | the shape of a feature | 05 |
| `QgsField`, `QgsFields` | column definitions | 05 |
| `QgsFeatureRequest`, `QgsExpression` | filtering and expressions | 05 |
| `processing` | runs any Processing Toolbox tool | 06 |
| `QgsSymbol`, renderers, `QgsPalLayerSettings` | styling and labels | 07 |
| `QgsPrintLayout`, `QgsLayoutItem…`, `QgsLayoutExporter` | print layouts | 08 |

Nearly everything starts with `Qgs`. The two exceptions you'll see are `Qgis` (enums and settings for the whole program) and `iface`.

## 5. Imports

The QGIS console imports most of PyQGIS automatically, so `QgsVectorLayer` just works there. Course scripts still **import explicitly**:

```python
from qgis.core import QgsProject, QgsVectorLayer
```

because (1) the script then also works outside the console (Module 09), (2) a reader, or an AI, can see where each name comes from, and (3) a missing import is the first thing to check when something is "not defined".

Use `qgis.PyQt` (not `PyQt5`) for Qt things like colours. That one import works in both QGIS 3 and QGIS 4:

```python
from qgis.PyQt.QtGui import QColor      # ✔ QGIS 3 and 4
from PyQt5.QtGui import QColor          # ✘ breaks in QGIS 4
```

## 6. Enums: named options

Old code (and lots of AI code) uses bare numbers, or short names that QGIS 4 no longer accepts:

```python
layer.geometryType() == 2                            # what is 2? (polygon) - unreadable
layer.geometryType() == QgsWkbTypes.PolygonGeometry  # old style: deprecated
layer.geometryType() == Qgis.GeometryType.Polygon    # ✔ clear, works in QGIS 3.30+ and 4
```

The pattern for QGIS 4 is **`Class.EnumName.Value`**. More in Module 09.

## 7. The "came back empty" trap

Many PyQGIS methods don't crash when something is missing. They hand back something *empty*, and the crash comes later, somewhere confusing.

```python
layers = QgsProject.instance().mapLayersByName("Countries")   # wrong case!
layers                # []  - an EMPTY list, no error yet
layer = layers[0]     # IndexError: list index out of range  ← crash here

iface.activeLayer()   # None if no layer is selected in the Layers panel
iface.activeLayer().name()   # AttributeError: 'NoneType' object has no attribute 'name'

bad = QgsVectorLayer(r"D:\nowhere.gpkg|layername=x", "x", "ogr")
bad.isValid()         # False - QGIS made the object, but it holds no data
bad.featureCount()    # -2, a meaningless number, and no error at all! The silent kind.
```

**Defence:** check right after you get something.

```python
layer = QgsVectorLayer(uri, "countries", "ogr")
if not layer.isValid():
    raise RuntimeError(f"Could not load layer from {uri}")
```

`raise` stops the script with **your** message, which is clearer than a confusing error ten lines later.

## 8. The course header, explained

Now you can read the lines at the top of every exercise:

```python
from pathlib import Path
from qgis.core import QgsExpressionContextUtils

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA = COURSE / "data"
```

- `QgsExpressionContextUtils.globalScope()` returns an object holding all QGIS **global variables**
- `.variable("course_root")` reads the one Module 00 saved: the folder path, as text
- `Path(...)` turns that text into a `Path` object, so `/ "data"` can join folders
- names in CAPITALS (`COURSE`, `DATA`) are a convention for "set once at the top, never changed"

---

## Exercises

| File | Practises |
|---|---|
| `ex03_1_explore_layer.py` | asking a layer about itself, chaining, `dir()` |
| `ex03_2_docs_hunt.py` | finding methods you've never seen with `dir()`/`help()`/docs |
| `ex03_3_empty_trap.py` | writing a safe `get_layer()` helper that fails clearly |

## Checkpoint

1. `layer.crs` prints `<built-in method crs ...>`. What's wrong?
2. What does `-> bool` at the end of a signature tell you?
3. An AI script calls `layer.getFeatureCount()`. How do you check in 10 seconds whether that exists?
4. What do you get from `QgsProject.instance().mapLayersByName("roads")` when there is no layer called *roads*?
5. Why `from qgis.PyQt.QtGui import QColor` and not `from PyQt5.QtGui import QColor`?

<details><summary>Answers</summary>

1. Missing brackets: it should be `layer.crs()`.
2. The method returns `True` or `False`.
3. `[m for m in dir(layer) if "count" in m.lower()]`. It shows `featureCount`, not `getFeatureCount`: the AI invented the name.
4. An empty list `[]`. No error until you try `[0]`.
5. `qgis.PyQt` works in both QGIS 3 (Qt5) and QGIS 4 (Qt6). `PyQt5` breaks in QGIS 4.

</details>

## 🤖 With Claude

Ask: *"I'm using QGIS 3.40. List 5 methods of QgsVectorLayer you think I'll use most, with their exact signatures."* Then **check each one** with `help(layer.<method>)` in your console. Did Claude get them all right? This is the start of the verification habit.

**Next:** [Module 04: Layers, projects and CRS](../04-layers-and-crs/README.md)
