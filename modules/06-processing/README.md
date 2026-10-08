# Module 06: Processing tools from Python

**Time:** about 4 hours · **Week 2** · Book: Ch. 3 (processing algorithms: extract by expression, buffer, extract by location), Ch. 9 (GDAL: warp, raster tools), Ch. 5 (QuickOSM, mentioned only)

The Processing Toolbox has hundreds of tools: buffer, clip, dissolve, reproject, hillshade, contours, zonal statistics… Every one of them can be run from Python with **one function**: `processing.run()`. This is the most useful thing in PyQGIS. Most automation is just "run these tools, in this order, for each of these inputs".

## You will

- find any tool's **ID** and **parameters**, including the trick of letting QGIS write the code for you
- run tools, use their results, and chain them
- redo the book's "cities along the Amazon" example properly, and see why its bug hid at the equator
- batch-process many inputs in a loop, saving into one GeoPackage
- run raster tools (reproject, hillshade, slope, contours) on a DEM
- know about `qgis_process`, which runs tools from the command line

## Key words

| Word | Meaning |
|---|---|
| **Algorithm** | Processing's word for a tool. Each has an **ID** like `native:buffer` or `gdal:hillshade`. |
| **Provider** | Who supplies the tool: `native` (QGIS's own, fast), `gdal` (GDAL's tools), `qgis`, `grass`… |
| **Parameters** | The tool's inputs and options, given as a **dictionary**: `{"INPUT": ..., "DISTANCE": 10000, "OUTPUT": ...}`. |
| **`TEMPORARY_OUTPUT`** | "Keep the result in memory, don't write a file." |
| **Result dictionary** | What `processing.run()` returns, e.g. `{"OUTPUT": <layer or path>}`. |
| **Chaining** | Feeding one tool's output into the next tool's input. |
| **Batch** | Running the same tool(s) on many inputs. |
| **Predicate** | The spatial test in "select/extract by location": intersects, contains, within… |

---

## 1. The basic call

```python
import processing

result = processing.run("native:buffer", {
    "INPUT": rivers_layer,          # a layer object, a path, or "path|layername=..."
    "DISTANCE": 10000,              # in the layer's CRS units!
    "SEGMENTS": 8,
    "DISSOLVE": True,
    "OUTPUT": "TEMPORARY_OUTPUT",
})
buffered = result["OUTPUT"]
```

Parameters you leave out get their **default** values.

### What comes back?

| `OUTPUT` you give | What `result["OUTPUT"]` is |
|---|---|
| `"TEMPORARY_OUTPUT"` (vector tool) | a `QgsVectorLayer` in memory: use it directly |
| a file path, e.g. `str(OUTPUT / "buffer.gpkg")` | the path as **text**. Make a layer from it if you need one |
| `"TEMPORARY_OUTPUT"` (GDAL/raster tool) | the path of a temporary **file** (text) |

When in doubt, `print(type(result["OUTPUT"]))`. That check would save a lot of AI-written code that does `.featureCount()` on a string.

## 2. Finding the ID and parameters

### Trick 1: let QGIS write the code (best)

1. Run the tool once **in the GUI**, with the settings you want.
2. Open **Processing → History**.
3. Right-click the entry → **Copy as Python Command**.
4. Paste it into the editor. It's correct code for *your* QGIS version, with every parameter spelled out.

You can also open a tool's dialog and use **Advanced → Copy as Python Command** without running it.

> **This is the most reliable source of Processing code, more reliable than any AI**, because it comes from your own QGIS. A good workflow is: run in the GUI → copy from History → ask AI to wrap it in a loop. AI is good at loops and bad at remembering parameter names.

### Trick 2: ask Processing itself (offline)

```python
processing.algorithmHelp("native:buffer")      # description + every parameter + allowed values

from qgis.core import QgsApplication
for alg in QgsApplication.processingRegistry().algorithms():
    if "buffer" in alg.id():
        print(alg.id(), "→", alg.displayName())
```

### Options given as numbers

Some parameters are choices given as numbers. `algorithmHelp` lists them:

```text
END_CAP_STYLE: End cap style
    Parameter type: QgsProcessingParameterEnum
    Available values:
        - 0: Round
        - 1: Flat
        - 2: Square
```

So `"END_CAP_STYLE": 1` means *Flat*. In `extractbylocation`, `"PREDICATE": [0]` means *intersect* (it's a list because you can choose several).

## 3. Chaining: the book's Amazon example, fixed

The book (Chapter 3, adapted from Anita Graser's *PyQGIS 101*) finds cities along the Amazon:

```python
# book version (simplified)
amazonas = processing.run("native:extractbyexpression",
    {"INPUT": rivers, "EXPRESSION": "name = 'Amazonas'", "OUTPUT": "memory:"})["OUTPUT"]
buffer_distance = 0.1 #degrees
buffered = processing.run("native:buffer",
    {"INPUT": amazonas, "DISTANCE": buffer_distance, ..., "OUTPUT": "memory:"})["OUTPUT"]
places_along = processing.run("native:extractbylocation",
    {"INPUT": places, "PREDICATE": [0], "INTERSECT": buffered, "OUTPUT": "memory:"})["OUTPUT"]
```

It finds **Iquitos, Leticia and Santarém**. Do it properly, in metres, and you get… the same three. Was the book right after all?

Only by luck. The Amazon is on the **equator**, where 0.1° is about 11 km in every direction. Run the *same* code on the **Lena** in Siberia (60–72°N):

| Lena | Cities found |
|---|---|
| 0.1° buffer (book method) | Lensk |
| 10 km buffer in a projected CRS | Lensk, **Yakutsk, Zhigansk** |

At 62°N, 0.1° of longitude is only about 5 km, so the degree buffer is squashed east–west and misses Yakutsk, which is about 6 km from the river line.

**The fixed chain:** reproject → buffer in metres → extract.

```python
river = processing.run("native:extractbyexpression",
    {"INPUT": rivers, "EXPRESSION": "\"name\" = 'Lena'", "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
river_m = processing.run("native:reprojectlayer",
    {"INPUT": river, "TARGET_CRS": "ESRI:102027", "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]   # metres
zone = processing.run("native:buffer",
    {"INPUT": river_m, "DISTANCE": 10_000, "DISSOLVE": True, "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
near = processing.run("native:extractbylocation",
    {"INPUT": places, "PREDICATE": [0], "INTERSECT": zone, "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
```

(`places` is still in EPSG:4326 and `zone` in ESRI:102027. `extractbylocation` reprojects on the fly, so that's fine.)

> **Two lessons in one:** (1) the units bug; (2) **test where the bug would show**. Code that's wrong can still give right answers on friendly data. When you check AI code, choose a test case that would expose the mistake: high latitude, a name with an apostrophe, a NULL value, an empty result.

`'memory:'` (the book's output) still works, but `'TEMPORARY_OUTPUT'` is the current spelling and works for every tool type.

## 4. Saving outputs into one GeoPackage

```python
gpkg = OUTPUT / "module06.gpkg"
target = f"ogr:dbname='{gpkg}' table=\"aut_rivers\" (geom)"
processing.run("native:clip", {"INPUT": rivers, "OVERLAY": austria, "OUTPUT": target})
```

That `ogr:dbname=... table=...` string means "a layer called *aut_rivers* inside this GeoPackage". Run it again with another `table` name and you get a second layer in the same file. Giving just `str(OUTPUT / "x.gpkg")` makes a *new* GeoPackage whose single layer is named after the file.

## 5. Batch processing: a loop around tools

```python
codes = ["AUT", "CHE", "NOR", "PER", "KEN"]
for code in codes:
    country = processing.run("native:extractbyattribute", {
        "INPUT": countries, "FIELD": "adm0_a3", "OPERATOR": 0, "VALUE": code,
        "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
    clipped = processing.run("native:clip", {
        "INPUT": rivers, "OVERLAY": country,
        "OUTPUT": f"ogr:dbname='{gpkg}' table=\"{code.lower()}_rivers\" (geom)"})["OUTPUT"]
    print(code, "done")
```

**Habits for batch scripts:**

- print progress (`print(code, "done")`), so you know where it failed
- write each result to a predictable name built from the loop variable
- after the loop, **count** what you made, and compare with what you expected

## 6. Raster tools: a DEM workflow

`dem_sample.tif` is in EPSG:4326: its pixels are 0.00083° wide but their *heights* are in metres. Tools that mix horizontal and vertical distances, like **slope** and **hillshade**, then get nonsense:

```python
processing.run("gdal:slope", {"INPUT": dem, "BAND": 1, "OUTPUT": ...})
# max slope: 90°, everywhere steep ← nonsense, metres of height over "degrees" of width
```

Either tell GDAL how many metres a degree is (`"SCALE": 111120`, an approximation), or, better, **reproject the DEM to a metric CRS first**:

```python
dem_utm = processing.run("gdal:warpreproject", {
    "INPUT": str(DATA / "dem_sample.tif"),
    "TARGET_CRS": "EPSG:32636",          # UTM zone 36N, metres (EPSG:2039 would also do)
    "RESAMPLING": 1,                     # 1 = bilinear (good for elevation)
    "TARGET_RESOLUTION": 90,             # metres
    "NODATA": -9999,                     # mark the empty corners as "no data"
    "OUTPUT": str(OUTPUT / "dem_utm.tif")})["OUTPUT"]

hillshade = processing.run("gdal:hillshade", {"INPUT": dem_utm, "BAND": 1, "Z_FACTOR": 1,
    "AZIMUTH": 315, "ALTITUDE": 45, "OUTPUT": str(OUTPUT / "hillshade.tif")})["OUTPUT"]
slope = processing.run("gdal:slope", {"INPUT": dem_utm, "BAND": 1,
    "OUTPUT": str(OUTPUT / "slope.tif")})["OUTPUT"]
contours = processing.run("gdal:contour", {"INPUT": dem_utm, "BAND": 1, "INTERVAL": 100,
    "FIELD_NAME": "elev", "OUTPUT": str(OUTPUT / "contours.gpkg")})["OUTPUT"]

stats = processing.run("native:rasterlayerstatistics", {"INPUT": slope, "BAND": 1})
print(stats["MEAN"], stats["MAX"])
```

- `NODATA` matters: without it, the empty corners created by reprojection get the value 0, and the edge between 0 and a real height of −400 m or +900 m looks like a cliff.
- This is the book's Chapter 9 (GDAL `warp`), done through Processing, so no separate GDAL install or Spyder is needed.

## 7. Errors from tools

A wrong parameter raises a `QgsProcessingException` with a message, something like this. Read it like any traceback (last line first):

```text
_core.QgsProcessingException: Unable to execute algorithm
Could not load source layer for INPUT: D:\PythonCourse\data\natural_earth.gpkg|layername=river not found
```

The usual causes are a wrong layer name, a wrong parameter name (`"DISTANCES"`), or a value of the wrong type.

## 8. Outside QGIS: `qgis_process`

Every tool can also run from a command prompt, with no QGIS window. On Windows, open the **OSGeo4W Shell** that came with QGIS:

```text
qgis_process-qgis-ltr list                          (all tools)
qgis_process-qgis-ltr help native:buffer
qgis_process-qgis-ltr run native:buffer -- INPUT="D:\data\roads.gpkg" DISTANCE=50 OUTPUT="D:\out\b.gpkg"
```

(The command name depends on how QGIS was installed: `qgis_process-qgis-ltr`, `qgis_process-qgis` or `qgis_process`.) Module 09 shows when this is useful.

> **About OpenStreetMap (book Ch. 5):** the book uses the OSMnx library. Inside QGIS the easy route is the **QuickOSM** plugin (Plugins menu). Its tools also appear in Processing (`quickosm:...`), so you can run them with `processing.run` too. They need the internet, so they aren't part of this offline course.

---

## Exercises

| File | Practises |
|---|---|
| `ex06_1_find_and_run.py` | finding tools, `algorithmHelp`, centroids, dissolve, result types |
| `ex06_2_rivers_fixed.py` | the book's chain in degrees vs metres, on the Amazon **and** the Lena |
| `ex06_3_batch_clip.py` | a batch loop writing 10 layers into one GeoPackage, then verifying |
| `ex06_4_terrain.py` | DEM → reproject → hillshade, slope, contours (and the 90° slope trap) |

**Before the exercises, try Trick 1:** run *Vector geometry → Centroids* in the GUI, then copy it from History as Python. Compare it with what you'd have written.

## Checkpoint

1. Where's the fastest reliable place to get the exact `processing.run(...)` call for a tool?
2. `result["OUTPUT"].featureCount()` fails with `'str' object has no attribute 'featureCount'`. Why?
3. Why did the book's degree buffer give the right cities on the Amazon?
4. A slope raster from a DEM in EPSG:4326 shows 90° almost everywhere. Why, and what are the two fixes?
5. What does `"PREDICATE": [0]` mean in `native:extractbylocation`?

<details><summary>Answers</summary>

1. Processing → History → right-click → Copy as Python Command (or Advanced → Copy as Python Command in the tool dialog).
2. The output was written to a file, so `OUTPUT` is a path (text). Make a layer: `QgsVectorLayer(path, "name", "ogr")`.
3. Near the equator 0.1° is about 11 km both ways, so the error is small there. It shows up at high latitudes.
4. Heights are in metres but pixel sizes are in degrees. Fix: reproject the DEM to a metric CRS (best), or set `SCALE` to about 111120.
5. Intersects (0 in the list of predicates).

</details>

## 🤖 With Claude

Copy a command from your Processing History, paste it to Claude, and ask: *"Turn this into a loop over these 5 country codes, saving each result as a separate layer in one GeoPackage, with a progress print and a count check at the end."* Then check: did Claude keep your parameter names exactly as they were?

**Next:** [Module 07: Styling, labels and QML](../07-styling-and-labels/README.md)
