# Module 04: Layers, projects and CRS

**Time:** about 4 hours · **Week 2** · Book: Ch. 1 (map projections, vector vs raster) and Ch. 2 (loading data, the Python console)

## You will

- load vector layers (GeoPackage, CSV) and rasters by code, and check they loaded
- list the layers inside a GeoPackage
- organise the Layers panel: groups, order, visibility
- talk to the QGIS window through `iface`
- understand CRS well enough to catch the most common AI mistake: **measuring in degrees**
- set the project CRS, transform coordinates, and save a project

## Key words

| Word | Meaning |
|---|---|
| **Data source / URI** | The "address" QGIS uses to find data: a path, plus extras like `|layername=rivers`. |
| **Provider** | The QGIS component that reads a format: `"ogr"` for most vector files, `"gdal"` for rasters, `"delimitedtext"` for CSV, `"memory"` for temporary layers. |
| **Vector / raster** | Vector = points, lines, polygons with attributes. Raster = a grid of pixels with values (elevation, colour). |
| **Layer tree** | The structure of the Layers panel: groups and layers in order. |
| **`iface`** | The QGIS **window** as an object: map canvas, message bar, active layer. Only exists inside QGIS. |
| **CRS** | Coordinate Reference System: the rule that turns coordinates into places on Earth. |
| **Geographic CRS** | Coordinates are latitude/longitude, in **degrees**. Example: EPSG:4326 (WGS 84). |
| **Projected CRS** | The globe is flattened onto a plane, and coordinates are in **metres** (usually). Examples: EPSG:3035 (Europe), EPSG:2039 (Israel), UTM zones. |
| **EPSG code** | A catalogue number for a CRS, e.g. `EPSG:4326`. |
| **On-the-fly reprojection** | QGIS draws every layer in the *project* CRS, whatever the layer's own CRS. Handy, but it means the layers' data can be in different CRSs without you noticing. |
| **Transform** | Converting coordinates from one CRS to another. |

---

## 1. Loading layers

### A layer from a GeoPackage

```python
from pathlib import Path
from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer

gpkg = DATA / "natural_earth.gpkg"
rivers = QgsVectorLayer(f"{gpkg}|layername=rivers", "Rivers", "ogr")
#                        └── data source (URI) ──┘  └ name ┘  └provider┘
if not rivers.isValid():
    raise RuntimeError("rivers did not load")
QgsProject.instance().addMapLayer(rivers)
```

The second argument is the **display name** in the Layers panel, and you can choose it freely. The *data* is identified by the URI.

### What's inside a GeoPackage?

```python
from qgis.core import QgsProviderRegistry
for sub in QgsProviderRegistry.instance().querySublayers(str(gpkg)):
    print(sub.name())
# countries, countries_110m, places, rivers, lakes, ...
```

### A shapefile

Use just the path: `QgsVectorLayer(r"D:\data\roads.shp", "Roads", "ogr")`.

### Points from a CSV

```python
csv_path = DATA / "capitals.csv"
uri = f"{csv_path.as_uri()}?delimiter=,&xField=longitude&yField=latitude&crs=EPSG:4326"
capitals = QgsVectorLayer(uri, "Capitals", "delimitedtext")
```

- `as_uri()` turns the path into `file:///D:/PythonCourse/data/capitals.csv`, the form this provider needs.
- `xField` is the **longitude** (east–west) and `yField` the **latitude**. Swapping them is a classic mistake: the points land in a strange, rotated pattern, or some of them disappear (latitudes can't go beyond ±90°).

### A raster

```python
dem = QgsRasterLayer(str(DATA / "dem_sample.tif"), "DEM")   # provider "gdal" is the default
print(dem.width(), dem.height(), dem.bandCount())
```

### The book's way: `iface.addVectorLayer`

The book uses `iface.addVectorLayer(uri, "places", "ogr")`, which creates **and** adds the layer in one go. That's fine in the console, but it only works inside the QGIS window. The `QgsVectorLayer` + `addMapLayer` way works everywhere (scripts, tools, headless runs), so the course uses it.

## 2. The project and the Layers panel

```python
project = QgsProject.instance()

project.mapLayers()                  # dict: {layer_id: layer, ...}
project.mapLayersByName("Rivers")    # list (maybe empty!)
project.removeMapLayer(rivers.id())  # remove by id
project.count()                      # number of layers
```

### Groups and order

```python
root = project.layerTreeRoot()               # the top of the Layers panel

base = root.addGroup("Base map")             # a new group at the bottom
project.addMapLayer(countries, False)        # False = add to the project, but NOT to the panel yet
base.addLayer(countries)                     # put it inside the group

root.insertGroup(0, "Reference")             # insert a group at position 0 = TOP
```

**The order in the panel is the drawing order:** the top layer is drawn last, so it ends up on top. Points go above lines, lines above polygons, and the background goes at the bottom.

```python
node = root.findLayer(graticule.id())        # the panel entry for one layer
node.setItemVisibilityChecked(False)         # untick it
```

## 3. Talking to the QGIS window: `iface`

```python
iface.setActiveLayer(rivers)                 # select it in the Layers panel
iface.mapCanvas().setExtent(rivers.extent()) # zoom to it
iface.mapCanvas().refresh()
iface.messageBar().pushMessage("Done", "Layers loaded", level=Qgis.MessageLevel.Success)
```

> `iface` exists only in the running QGIS window. Code that will become a Processing tool (Module 09) or run headless should not depend on it. Keep `iface` lines to the end of a script, for "show me the result".

## 4. CRS: the part that matters most

### Degrees are not distances

All the course data is in **EPSG:4326**, so coordinates are longitude/latitude in **degrees**. A degree of longitude is about 111 km at the equator, about 74 km at Vienna, and **0 km** at the poles. A degree is not a fixed distance, so you can't measure lengths or areas in it.

```python
from qgis.core import QgsCoordinateReferenceSystem, QgsUnitTypes

wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")
wgs84.isGeographic()                          # True
QgsUnitTypes.toString(wgs84.mapUnits())       # 'degrees'

laea = QgsCoordinateReferenceSystem("EPSG:3035")   # Europe, equal-area
QgsUnitTypes.toString(laea.mapUnits())        # 'meters'
```

The book's Chapter 3 buffers the Amazon by `0.1` **degrees** ("cities within 10 km"). In degrees, that buffer is about 11 km wide at the equator, and the same code run for a river in Norway would make a buffer that's narrower east–west than north–south. In Module 06 you'll redo that exercise properly, in metres.

> **AI red flag #1:** a distance, buffer or area computed on a layer in EPSG:4326. Always ask: *what are the units of this layer's CRS?*

### Choosing a CRS (rules of thumb)

| Purpose | Choose | Examples |
|---|---|---|
| World map (looks) | a world projection | Equal Earth `EPSG:8857`, Robinson `ESRI:54030` |
| Comparing **areas** | an **equal-area** CRS | `EPSG:8857` (world), `EPSG:3035` (Europe) |
| Local measuring, buffers | a local projected CRS in metres | UTM zone, national grid (`EPSG:2039` Israel TM Grid) |
| Web maps | Web Mercator `EPSG:3857` | (looks only; distorts area badly) |

### Project CRS vs layer CRS

```python
project.setCrs(QgsCoordinateReferenceSystem("EPSG:8857"))   # draw everything in Equal Earth
rivers.crs().authid()                                        # still 'EPSG:4326'!
```

Setting the project CRS changes how things are **drawn**. It doesn't change the layers' **data**. That's on-the-fly reprojection. To change the data itself you **reproject** the layer into a new file (Module 06).

### Transforming coordinates

```python
from qgis.core import QgsCoordinateTransform, QgsPointXY

to_laea = QgsCoordinateTransform(wgs84, laea, project)
vienna = to_laea.transform(QgsPointXY(16.3738, 48.2082))     # x = longitude first!
bratislava = to_laea.transform(QgsPointXY(17.1170, 48.1500))
vienna.distance(bratislava)                                  # ≈ 55,600 (metres)

QgsPointXY(16.3738, 48.2082).distance(QgsPointXY(17.1170, 48.1500))   # 0.745 "degrees" ← meaningless
```

`QgsPointXY(x, y)` takes **x first = longitude**, then y = latitude. People say "lat, lon", but code wants "lon, lat". Another classic swap.

### Measuring on the ellipsoid (no reprojection needed)

`QgsDistanceArea` measures on the curved Earth, straight from degrees:

```python
from qgis.core import QgsDistanceArea
da = QgsDistanceArea()
da.setSourceCrs(wgs84, project.transformContext())
da.setEllipsoid("EPSG:7030")        # WGS 84 ellipsoid
da.measureLine(QgsPointXY(16.3738, 48.2082), QgsPointXY(17.1170, 48.1500))   # ≈ 55,647 m
```

The two answers (55,624 m in EPSG:3035, 55,647 m on the ellipsoid) differ by 0.04%, which is the small distortion of the projection. Both are fine. The degree "distance" is the one that's wrong.

## 5. Saving the project

```python
project.setTitle("Module 04 practice")
ok = project.write(str(OUTPUT / "module04.qgz"))    # True if saved
```

`project.read(path)` opens one. Saved projects store layer paths (relative by default), styles, layouts and the project CRS.

---

## Exercises

| File | Practises |
|---|---|
| `ex04_1_load_layers.py` | list a GeoPackage, load 6 layers into groups in the right drawing order |
| `ex04_2_csv_points.py` | load `capitals.csv` as points; spot the x/y swap |
| `ex04_3_crs.py` | units, project CRS, transforming points, saving a `.qgz` |

## Checkpoint

1. What are the three arguments of `QgsVectorLayer(...)`?
2. Your CSV points appear in a strange, rotated pattern, and some are missing. Likely cause?
3. You set the project CRS to EPSG:3035. What's the CRS of the `rivers` layer now?
4. Why is `buffer(0.1)` on EPSG:4326 data a bad "10 km buffer"?
5. In the Layers panel, which layer is drawn on top: the first or the last?

<details><summary>Answers</summary>

1. The data source (URI), the display name, the provider (`"ogr"`, `"delimitedtext"`…).
2. `xField` and `yField` are swapped (latitude used as x).
3. Still EPSG:4326. The project CRS only changes the display.
4. Degrees aren't a fixed distance. 0.1° is about 11 km north–south everywhere, but east–west it shrinks towards the poles, so the buffer is distorted and the wrong size.
5. The first (top) one. It's drawn last, so it covers the others.

</details>

## 🤖 With Claude

Paste this prompt and **check the answer against this module**: *"In QGIS 3.40 I have a layer in EPSG:4326 and I want a 5 km buffer around rivers in Norway. Write the PyQGIS."* Does Claude reproject first, or use a geodesic method? Or does it buffer in degrees? Keep its answer. You'll grade it again in Module 11.

**Next:** [Module 05: Features, fields and expressions](../05-features-and-fields/README.md)
