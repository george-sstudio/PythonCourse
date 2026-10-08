# Module 05: Features, fields and expressions

**Time:** about 4 hours · **Week 2** · Book: Ch. 2 (querying populations), Ch. 3 (iterators, discovering attributes), Ch. 8 (missing data, in QGIS terms)

## You will

- loop through features and read their attributes and geometries
- filter with **QGIS expressions** from Python, and quote them correctly (`Côte d'Ivoire` breaks naive code)
- handle **NULL** values in a way that works in both QGIS 3 and QGIS 4
- measure areas and lengths correctly, and run simple spatial questions ("which country contains this point?")
- select, filter, edit and add fields **safely, on a copy**
- export results to a GeoPackage

## Key words

| Word | Meaning |
|---|---|
| **Feature** | One item in a vector layer: one row of the attribute table plus its geometry. Class: `QgsFeature`. |
| **Field** | A column of the attribute table, with a name and a type. Class: `QgsField`. |
| **Feature ID** (`fid`) | The feature's unique number in the layer. |
| **Iterator** | Something you can loop over, one item at a time. `layer.getFeatures()` returns one. It doesn't load all features at once. |
| **Expression** | A formula in QGIS's own expression language, the same one used in the Field Calculator, filters and labels: `"pop_est" > 1000000`. |
| **NULL** | "No value" in a field. Not 0, and not an empty text. |
| **Selection** | Features highlighted (yellow) in a layer. Many tools can act on "selected features only". |
| **Subset string / filter** | A layer-level filter (the *Filter…* in the layer menu). Features that don't match are hidden from everything. |
| **Edit session** | QGIS's "editing mode". Changes are collected, then **committed** (saved) or **rolled back** (thrown away). |
| **Memory layer** | A temporary layer that lives only in RAM, so it's safe for experiments. Gone when QGIS closes. |

---

## 1. Reading features

```python
countries = QgsVectorLayer(f"{GPKG}|layername=countries", "countries", "ogr")

for f in countries.getFeatures():
    print(f.id(), f["name"], f["pop_est"])
```

- `f["name"]` reads one attribute, like a dictionary.
- `f.attributes()` gives all values as a list, and `countries.fields().names()` gives the matching names.
- `f.geometry()` gives the shape (section 4).

> `getFeatures()` is an **iterator**: it hands out one feature at a time, and it's used up after one loop. To loop twice, call `getFeatures()` again.

### The counting pattern (a dictionary of totals)

```python
per_continent = {}
for f in countries.getFeatures():
    c = f["continent"]
    per_continent[c] = per_continent.get(c, 0) + 1     # .get(..., 0) starts the count
print(per_continent)   # {'Africa': 54, 'Asia': 53, ...}
```

### Faster requests

When you only need some features or some fields, say so. On big layers it's much faster:

```python
from qgis.core import QgsFeatureRequest

request = (QgsFeatureRequest()
           .setFilterExpression("continent = 'Africa'")
           .setSubsetOfAttributes(["name", "pop_est"], countries.fields())
           .setFlags(QgsFeatureRequest.Flag.NoGeometry))       # skip geometries
total = sum(f["pop_est"] for f in countries.getFeatures(request))
```

Short form when you just need a filter: `countries.getFeatures("continent = 'Africa'")`.

## 2. Expressions from Python

The QGIS expression language has its own quoting rules. They're the opposite of what many people expect:

| In an expression | Means |
|---|---|
| `"pop_est"` (double quotes) | a **field** |
| `'Africa'` (single quotes) | a piece of **text** |
| `=`, `<>`, `>`, `AND`, `OR`, `IN (...)`, `LIKE 'A%'`, `IS NULL` | operators |

Inside Python you write the expression as a Python string, so you need both kinds of quote:

```python
expr = "\"continent\" = 'Africa' AND \"pop_est\" > 50000000"
# or, easier to read: Python's single quotes outside, double quotes inside
expr = '"continent" = \'Africa\' AND "pop_est" > 50000000'
```

### The apostrophe trap

```python
name = "Côte d'Ivoire"
expr = f"\"name\" = '{name}'"        # → "name" = 'Côte d'Ivoire'   ← broken expression!
```

The `'` inside the name ends the text early. The safe way is to let QGIS do the quoting:

```python
from qgis.core import QgsExpression
expr = f"{QgsExpression.quotedColumnRef('name')} = {QgsExpression.quotedValue(name)}"
# → "name" = 'Côte d''Ivoire'   ✔ (QGIS doubles the apostrophe)
```

> **AI red flag:** expressions built with f-strings around names that come from data. They work in testing, then fail on *Côte d'Ivoire*, *N'Djamena* or *Coeur d'Alene*. Ask for `QgsExpression.quotedValue`.

### Checking an expression before using it

```python
e = QgsExpression("\"pop_est\" >> 5")
e.hasParserError()      # True
e.parserErrorString()   # explains what's wrong
```

## 3. NULL: the QGIS 3 vs QGIS 4 difference

Some fields have no value. In the `places` layer, 87 features have no `adm1name`. How Python *sees* that empty value **changed between versions**:

| | QGIS 3.40 | QGIS 4.x |
|---|---|---|
| `f["adm1name"]` | `NULL` (a special Qt object, `QVariant`) | `None` |
| `value is None` | **False** ← surprise! | True |

So code written for one version can quietly misbehave on the other. Use one of these, which work in both:

```python
from qgis.core import QgsVariantUtils

if QgsVariantUtils.isNull(f["adm1name"]):      # ✔ QGIS 3.28+ and 4
    ...

countries.getFeatures('"gdp_md" IS NULL')      # ✔ let the expression engine test it
```

**NULL is not the only kind of "missing".** Natural Earth marks unknown GDP as `-99` (and sometimes `0`). That's a *real number* to Python, so averages that include it come out wrong. Always look at the smallest and largest values of a field before you compute with it:

```python
idx = countries.fields().indexOf("gdp_md")
countries.minimumValue(idx), countries.maximumValue(idx)    # (-99, 21433226)  ← aha
```

This is the QGIS version of the book's Chapter 8 (data cleaning): check for missing values, check types, look at summary statistics. It just doesn't need pandas.

## 4. Geometry

```python
g = f.geometry()
g.type() == Qgis.GeometryType.Polygon
g.centroid().asPoint()          # QgsPointXY
g.boundingBox()                 # QgsRectangle
g.isMultipart()                 # True for MultiPolygon (e.g. France + overseas)
g.asWkt()[:80]                  # the shape as text: 'MultiPolygon (((...'
```

### Measuring correctly

```python
from qgis.core import QgsDistanceArea, Qgis

da = QgsDistanceArea()
da.setSourceCrs(countries.crs(), QgsProject.instance().transformContext())
da.setEllipsoid("EPSG:7030")

austria = next(countries.getFeatures("adm0_a3 = 'AUT'"))
area_m2 = da.measureArea(austria.geometry())          # ≈ 84,149,000,000 m²
area_km2 = area_m2 / 1_000_000                         # ≈ 84,149 km²

austria.geometry().area()      # 10.06  ← square DEGREES. Meaningless.
```

`geometry.area()` and `geometry.length()` use the layer's own units. In EPSG:4326 those are degrees, so use `QgsDistanceArea`, or reproject first (Module 06). The expression functions `$area` and `$length` use the **project's** ellipsoid and unit settings.

### Spatial questions

```python
from qgis.core import QgsGeometry, QgsPointXY

vienna = QgsGeometry.fromPointXY(QgsPointXY(16.3738, 48.2082))
for f in countries.getFeatures():
    if f.geometry().contains(vienna):
        print("Vienna is in", f["name"])

# neighbours of Austria: first a quick bounding-box filter, then the exact test
request = QgsFeatureRequest().setFilterRect(austria.geometry().boundingBox())
for f in countries.getFeatures(request):
    if f.id() != austria.id() and f.geometry().intersects(austria.geometry()):
        print(f["name"])
```

Other tests: `intersects`, `touches`, `within`, `disjoint`, `distance`. For whole-layer spatial joins, use Processing tools (Module 06). They're faster and shorter.

## 5. Selecting and filtering

```python
countries.selectByExpression('"income_grp" = \'5. Low income\'')
countries.selectedFeatureCount()
for f in countries.selectedFeatures():
    ...
countries.removeSelection()

countries.setSubsetString('"continent" = \'Europe\'')   # filter: like Layer → Filter…
countries.featureCount()                                 # now only European countries
countries.setSubsetString("")                            # remove the filter
```

A **selection** is temporary highlighting. A **subset string** changes what the layer *contains* until you clear it, and it's saved in the project.

## 6. Editing, safely

**Rule: never test edits on your source data.** Make a copy first:

```python
work = countries.materialize(QgsFeatureRequest())   # an in-memory copy of all features
work.setName("countries (copy)")
```

(Or write a copy to a new GeoPackage, section 7.)

### Adding fields and changing values

```python
from qgis.core import QgsField, edit
from qgis.PyQt.QtCore import QMetaType

with edit(work):                                   # starts editing; commits at the end
    work.addAttribute(QgsField("area_km2", QMetaType.Type.Double))
    work.addAttribute(QgsField("size_class", QMetaType.Type.QString))

idx_area = work.fields().indexOf("area_km2")
idx_class = work.fields().indexOf("size_class")

with edit(work):
    for f in work.getFeatures():
        km2 = da.measureArea(f.geometry()) / 1e6
        work.changeAttributeValue(f.id(), idx_area, round(km2, 1))
        work.changeAttributeValue(f.id(), idx_class, "large" if km2 > 1e6 else "other")
```

- `with edit(layer):` is like `with open(...)` from Module 02. It opens an edit session, and when the block ends it **commits**. If an error happens inside, it **rolls back**, so nothing half-done is saved.
- Field types: use `QMetaType.Type.Double`, `.Int`, `.LongLong`, `.QString`, `.Bool`, `.QDate`. These work in QGIS 3.38+ and 4.x. Old code uses `QVariant.Double`, which is deprecated and removed in QGIS 4.

> **AI red flags:** editing without an edit session (`startEditing()` with no `commitChanges()`, so nothing is saved); `QVariant.String` for field types; and editing the original GeoPackage "just to test".

## 7. Exporting to a GeoPackage

```python
from qgis.core import QgsVectorFileWriter

options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "GPKG"
options.layerName = "countries_stats"
options.actionOnExistingFile = QgsVectorFileWriter.ActionOnExistingFile.CreateOrOverwriteFile

error, message, path, layer_name = QgsVectorFileWriter.writeAsVectorFormatV3(
    work, str(OUTPUT / "module05.gpkg"), QgsProject.instance().transformContext(), options)

if error != QgsVectorFileWriter.WriterError.NoError:
    raise RuntimeError(message)
```

- `CreateOrOverwriteFile` replaces the whole file. To add another layer to an existing GeoPackage, use `CreateOrOverwriteLayer`.
- Set `options.ct = QgsCoordinateTransform(...)` to reproject while exporting.
- The function returns **four** things at once (a *tuple*), and Python lets you unpack them into four variables in one line.

**Verify the export.** Open it again and compare counts. It takes two lines and catches a lot:

```python
check = QgsVectorLayer(f"{OUTPUT / 'module05.gpkg'}|layername=countries_stats", "check", "ogr")
assert check.featureCount() == work.featureCount()
```

---

## Exercises

| File | Practises |
|---|---|
| `ex05_1_read_features.py` | loops, counting per category, top 5, totals with a request |
| `ex05_2_expressions.py` | filters, selection, subset strings, the apostrophe trap |
| `ex05_3_geometry.py` | point-in-polygon, neighbours, area in km² vs "square degrees" |
| `ex05_4_edit_and_export.py` | copy → add fields → fill them (with NULL / −99 handling) → export → verify |

## Checkpoint

1. In an expression, what's the difference between `"name"` and `'name'`?
2. Why does `f"\"name\" = '{name}'"` fail for some countries?
3. In QGIS 3.40, `f["adm1name"] is None` is `False` for an empty field. Why, and what should you use?
4. `geometry.area()` returns `10.06` for Austria. What unit is that?
5. What does `with edit(layer):` do if an error happens halfway through?

<details><summary>Answers</summary>

1. `"name"` is the field called *name*. `'name'` is the text *name*.
2. Names with an apostrophe (e.g. *Côte d'Ivoire*) end the text early. Use `QgsExpression.quotedValue(name)`.
3. QGIS 3 returns a `NULL` `QVariant`, not Python's `None`. Use `QgsVariantUtils.isNull(value)` or `IS NULL` in an expression.
4. Square degrees, which is meaningless. Use `QgsDistanceArea` or a projected CRS.
5. It rolls back: none of the changes are saved.

</details>

## 🤖 With Claude

Ask Claude: *"Write PyQGIS (QGIS 3.40) that adds a population density field to my countries layer."* Then review its answer against this module: does it work on a copy? Use an edit session? Measure area in km² correctly (not square degrees)? Handle `pop_est` = 0 and NULL? Use `QMetaType`, not `QVariant`? Write your findings down. Module 11 turns this into a checklist.

**Next:** [Module 06: Processing tools from Python](../06-processing/README.md)
