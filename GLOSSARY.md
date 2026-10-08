# Glossary

Plain-language meanings of every technical word in the course. The module where a word is introduced is in brackets.

## Python

| Word | Meaning |
|---|---|
| **argument** | The actual value you pass to a function: in `round(2.67, 1)`, `2.67` and `1`. [02] |
| **assert** | A line that stops the script with a message if something isn't true: `assert n == 13, "expected 13"`. [02] |
| **attribute (Python)** | A value stored on an object, used without brackets: `path.name`. Not the same as a GIS attribute. [03] |
| **block** | The indented lines belonging to an `if`, `for`, `def` or `with`. [02] |
| **boolean (`bool`)** | `True` or `False`. [01] |
| **class** | A blueprint for a kind of object (`QgsVectorLayer`). [03] |
| **comment** | Text after `#` that Python ignores, for humans. [00] |
| **condition** | Something that is `True` or `False`, used by `if`. [02] |
| **constructor** | Calling a class to make an object: `QgsVectorLayer(uri, name, "ogr")`. [03] |
| **deprecated** | Still works, but is marked for removal. Change it before it breaks. [09] |
| **dictionary (`dict`)** | Labelled values: `{"name": "Lima", "pop": 9751717}`. [01] |
| **docstring** | The text in triple quotes at the start of a function, explaining what it does. [02] |
| **enum** | A named set of options: `Qgis.GeometryType.Polygon`. [03] |
| **exception** | An error that stops the script, e.g. `KeyError`. [02] |
| **f-string** | Text with values inserted: `f"{city} has {pop:,} people"`. [01] |
| **float** | A decimal number: `31.77`. [01] |
| **function** | A named, reusable block of code, defined with `def`. [02] |
| **import** | Making a module's code available: `from pathlib import Path`. [02] |
| **index** | A position in a list. **Starts at 0.** [01] |
| **instance** | One object made from a class. [03] |
| **integer (`int`)** | A whole number: `-427`. [01] |
| **iterator** | Something you loop over one item at a time, e.g. `layer.getFeatures()`. It's used up after one loop. [05] |
| **list** | Ordered values: `["Lima", "Quito"]`. [01] |
| **list comprehension** | A one-line loop that builds a list: `[f["name"] for f in layer.getFeatures()]`. [02] |
| **loop** | Repeating a block for each item: `for x in items:`. [02] |
| **method** | A function belonging to an object: `layer.featureCount()`. [03] |
| **module** | A `.py` file of code you can import. [02, 09] |
| **None** | Python's "nothing here". [01] |
| **parameter** | The input name a function expects, in its `def` line. [02] |
| **raw string** | `r"D:\data"`, where backslashes are kept as they are. Use it for Windows paths. [01] |
| **refactor** | Rewrite code to be clearer without changing what it does. [09] |
| **return value** | What a function hands back with `return`. Not the same as `print`. [02] |
| **script** | A `.py` file run from top to bottom. [00] |
| **string (`str`)** | Text in quotes. [01] |
| **traceback** | Python's error report. Read it from the bottom up. [02] |
| **tuple** | Like a list, but unchangeable: `(16.37, 48.21)`. [02] |
| **type** | The kind of a value: `str`, `int`, `float`, `bool`… [01] |
| **variable** | A name that holds a value: `city = "Lima"`. [01] |

## QGIS and PyQGIS

| Word | Meaning |
|---|---|
| **API** | The list of classes and methods a program offers to code. [03] |
| **atlas** | A layout repeated once per feature of a coverage layer. [08] |
| **blend mode** | How a layer's colours mix with those below. *Multiply* is good for hillshades. [07] |
| **categorized / graduated / rule-based** | Renderers: by category, by number classes, or by expression rules. [07] |
| **child algorithm** | A Processing tool run inside another tool. [09] |
| **console / editor** | QGIS's one-line Python prompt / its script editor. [00] |
| **context (Processing)** | The object carrying settings and temporary layers through a Processing run. [09] |
| **data-defined property** | A symbol setting computed per feature from an expression. [07] |
| **edit session** | QGIS editing mode. Changes are committed or rolled back. `with edit(layer):` [05] |
| **expression** | A formula in QGIS's own language: `"pop_est" > 1000000`. [05] |
| **feature** | One item of a vector layer: attributes + geometry. [05] |
| **feedback** | How a Processing tool reports progress and messages, and checks for Cancel. [09] |
| **field** | A column of the attribute table. [05] |
| **GeoPackage (`.gpkg`)** | A single file holding many layers. [04] |
| **`iface`** | The QGIS window as a Python object. Not available in tools or headless runs. [04] |
| **layer tree** | The structure of the Layers panel. [04] |
| **layout item / item id** | Anything on a print layout page / the name code uses to find it. [08] |
| **memory layer** | A temporary layer in RAM. [05] |
| **NULL** | "No value" in a field. It's `QVariant` NULL in QGIS 3 and `None` in QGIS 4. Check with `QgsVariantUtils.isNull()`. [05] |
| **Processing / algorithm** | QGIS's toolbox system, and one tool in it (`native:buffer`). [06] |
| **provider** | The component that reads a format (`ogr`, `gdal`, `delimitedtext`), or that supplies Processing tools (`native`, `gdal`). [04, 06] |
| **QML** | A QGIS style file. [07] |
| **QPT** | A QGIS layout template file. [08] |
| **renderer** | A layer's drawing rule. [07] |
| **selection / subset string** | Highlighted features / a layer-level filter. [05] |
| **sink** | Where a Processing tool's output features go. [09] |
| **symbol / symbol layer** | What a feature looks like / one piece of that look. [07] |
| **`TEMPORARY_OUTPUT`** | "Keep the result in memory" in `processing.run`. [06] |
| **URI** | A data source address, e.g. `path.gpkg|layername=rivers`. [04] |

## GIS and cartography

| Word | Meaning |
|---|---|
| **antimeridian** | The 180° meridian. Features that cross it (Fiji, Russia) break naive extent and centroid code. [12] |
| **CRS** | Coordinate Reference System: how coordinates map to places on Earth. [04] |
| **DEM** | Digital Elevation Model: a raster of heights. [06] |
| **ellipsoid** | The mathematical shape of the Earth used for accurate measuring (e.g. WGS 84, EPSG:7030). [04] |
| **EPSG code** | A catalogue number for a CRS (`EPSG:4326`). [04] |
| **equal-area projection** | A projection that keeps areas correct (Equal Earth, LAEA). [04] |
| **geographic CRS** | Coordinates in degrees of latitude/longitude. [04] |
| **hillshade** | Shading that simulates light on terrain. [06] |
| **hypsometric tints** | Colours by elevation. [07] |
| **no-data** | A raster value meaning "no value here". [06] |
| **on-the-fly reprojection** | QGIS drawing every layer in the project CRS, whatever the layer's own CRS. [04] |
| **projected CRS** | A flat map CRS, usually in metres. [04] |
| **scale (1:N)** | 1 unit on paper = N units on the ground. [01, 08] |
| **UTM** | Universal Transverse Mercator: 60 zones, 6° wide, in metres. [08] |

## Working with AI

| Word | Meaning |
|---|---|
| **acceptance check** | A concrete test of "correct", written before the code. [10] |
| **brief** | A full written request: goal, context, inputs, outputs, rules, checks. [10] |
| **context card** | A generated summary of your project for the AI (`tools/describe_project.py`). [10] |
| **context window** | How much conversation an AI can hold in mind. Long, messy chats make it worse. [10] |
| **hallucination** | Invented output that sounds right, e.g. a method that doesn't exist. [10, 11] |
| **house rules** | Standing instructions given once (Claude Project instructions). [10] |
| **minimal reproduction** | The smallest code and data that still shows a bug. [11] |
| **regression** | A fix that breaks something that used to work. [11] |
| **silent failure** | Code that finishes with no error but a wrong or missing result. [11] |
| **two-chat review** | Asking a fresh chat to review code against the brief. [11] |
