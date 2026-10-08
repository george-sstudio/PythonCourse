# PyQGIS cheat sheet

The snippets used most in this course, in forms that work in **QGIS 3.40 and QGIS 4.x**. This whole page is tested: run top to bottom, it executes without errors on both versions.

## 1. Course header / paths

Every course script starts like this. For your own projects, use `Path(r"D:\Maps\...")`.

```python
from pathlib import Path
from qgis.core import QgsExpressionContextUtils
COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA, OUTPUT = COURSE / "data", COURSE / "output"
GPKG = DATA / "natural_earth.gpkg"
```

## 2. Load layers (and check them)

Always check `isValid()`. `mapLayersByName` returns a **list**, which may be empty.

```python
from qgis.core import QgsProject, QgsRasterLayer, QgsVectorLayer, QgsProviderRegistry
project = QgsProject.instance()
countries = QgsVectorLayer(f"{GPKG}|layername=countries", "Countries", "ogr")
if not countries.isValid():
    raise RuntimeError("countries did not load")
project.addMapLayer(countries)
dem = QgsRasterLayer(str(DATA / "dem_sample.tif"), "DEM")
csv_uri = f"{(DATA / 'capitals.csv').as_uri()}?delimiter=,&xField=longitude&yField=latitude&crs=EPSG:4326"
capitals = QgsVectorLayer(csv_uri, "Capitals", "delimitedtext")
names_in_gpkg = [s.name() for s in QgsProviderRegistry.instance().querySublayers(str(GPKG))]
layer = project.mapLayersByName("Countries")[0]       # [] if no such layer!
```

## 3. Ask a layer about itself

```python
from qgis.core import Qgis, QgsUnitTypes, QgsWkbTypes
layer.name(), layer.featureCount(), layer.crs().authid()
QgsUnitTypes.toString(layer.crs().mapUnits())        # 'degrees' or 'meters'
layer.geometryType() == Qgis.GeometryType.Polygon
layer.fields().names()
QgsWkbTypes.displayString(layer.wkbType())           # 'MultiPolygon'
```

## 4. Features, filters, NULL

Field names in `"double quotes"`, text in `'single quotes'`. Let QGIS quote values that come from data.

```python
from qgis.core import QgsExpression, QgsFeatureRequest, QgsVariantUtils
for f in layer.getFeatures("\"continent\" = 'Africa'"):
    name, pop = f["name"], f["pop_est"]
name = "Côte d'Ivoire"
expr = f"\"name\" = {QgsExpression.quotedValue(name)}"       # safe quoting
civ = next(layer.getFeatures(expr))
request = QgsFeatureRequest().setFilterExpression("\"pop_est\" > 1e8").setFlags(QgsFeatureRequest.Flag.NoGeometry)
big = [f["name"] for f in layer.getFeatures(request)]
QgsVariantUtils.isNull(civ["gdp_md"])                # NULL test for QGIS 3 AND 4
layer.selectByExpression("\"continent\" = 'Europe'"); layer.removeSelection()
layer.setSubsetString("\"continent\" = 'Europe'"); layer.setSubsetString("")
```

## 5. Measure correctly

On EPSG:4326 data, never use `geometry.area()`/`.length()`: those are in degrees.

```python
from qgis.core import QgsDistanceArea, QgsPointXY
da = QgsDistanceArea()
da.setSourceCrs(layer.crs(), project.transformContext())
da.setEllipsoid("EPSG:7030")
area_km2 = da.measureArea(civ.geometry()) / 1e6
dist_m = da.measureLine(QgsPointXY(16.37, 48.21), QgsPointXY(17.12, 48.15))   # x = lon first
```

## 6. CRS and transforms

Project CRS changes the display only. Transform extents into a map item's CRS before using them.

```python
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform
utm = QgsCoordinateReferenceSystem("EPSG:32633")
to_utm = QgsCoordinateTransform(layer.crs(), utm, project)
p = to_utm.transform(QgsPointXY(16.37, 48.21))
box = to_utm.transformBoundingBox(civ.geometry().boundingBox())
project.setCrs(QgsCoordinateReferenceSystem("EPSG:8857"))   # display only
```

## 7. Edit a copy safely

Never edit source files to test. `with edit()` commits at the end, or rolls back on an error.

```python
from qgis.core import QgsField, edit
from qgis.PyQt.QtCore import QMetaType
work = layer.materialize(QgsFeatureRequest())
with edit(work):
    work.addAttribute(QgsField("area_km2", QMetaType.Type.Double))
idx = work.fields().indexOf("area_km2")
with edit(work):
    for f in work.getFeatures():
        work.changeAttributeValue(f.id(), idx, round(da.measureArea(f.geometry()) / 1e6, 1))
```

## 8. Export to GeoPackage (and check)

```python
from qgis.core import QgsVectorFileWriter
opts = QgsVectorFileWriter.SaveVectorOptions()
opts.driverName, opts.layerName = "GPKG", "countries_area"
opts.actionOnExistingFile = QgsVectorFileWriter.ActionOnExistingFile.CreateOrOverwriteFile   # ...OverwriteLayer to add
err, msg, _, _ = QgsVectorFileWriter.writeAsVectorFormatV3(work, str(OUTPUT / "cheat.gpkg"), project.transformContext(), opts)
if err != QgsVectorFileWriter.WriterError.NoError:
    raise RuntimeError(msg)
```

## 9. Processing

Fastest source of exact parameters: run the tool in the GUI → Processing → History → *Copy as Python Command*.

```python
import processing
processing.algorithmHelp("native:buffer")            # parameters + allowed values
out = processing.run("native:reprojectlayer", {"INPUT": layer, "TARGET_CRS": "EPSG:3035", "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]   # a layer
buf = processing.run("native:buffer", {"INPUT": out, "DISTANCE": 10_000, "DISSOLVE": True, "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
path = processing.run("native:centroids", {"INPUT": layer, "OUTPUT": str(OUTPUT / "cent.gpkg")})["OUTPUT"]   # a path (str)
target = f"ogr:dbname='{OUTPUT / 'many.gpkg'}' table=\"africa\" (geom)"   # a named layer inside a GeoPackage
processing.run("native:extractbyattribute", {"INPUT": layer, "FIELD": "continent", "OPERATOR": 0, "VALUE": "Africa", "OUTPUT": target})
```

## 10. Style

QML files store colours as R,G,B,A. 8-digit hex in QGIS is `#AARRGGBB`.

```python
from qgis.core import QgsFillSymbol, QgsSingleSymbolRenderer, QgsCategorizedSymbolRenderer, QgsRendererCategory, QgsGraduatedSymbolRenderer, QgsClassificationJenks, QgsStyle
from qgis.PyQt.QtGui import QColor, QPainter
layer.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple({"color": "#f1ede4", "outline_color": "#b8b2a5", "outline_width": "0.15"})))
cats = [QgsRendererCategory(v, QgsFillSymbol.createSimple({"color": c}), v) for v, c in [("Africa", "#e3c9a5"), ("Europe", "#c7d3e3")]]
cats.append(QgsRendererCategory(None, QgsFillSymbol.createSimple({"color": "#e4e4e4"}), "Other"))
layer.setRenderer(QgsCategorizedSymbolRenderer("continent", cats))
g = QgsGraduatedSymbolRenderer('CASE WHEN "gdp_md" > 0 THEN "gdp_md" * 1e6 / "pop_est" END')
g.setClassificationMethod(QgsClassificationJenks()); g.updateClasses(layer, 5)
g.updateColorRamp(QgsStyle.defaultStyle().colorRamp("YlGnBu")); layer.setRenderer(g)
dem.setBlendMode(QPainter.CompositionMode.CompositionMode_Multiply); dem.setOpacity(0.6)
semi_white = "255,255,255,179"                       # R,G,B,A  (NOT "#ffffffb3")
message, ok = layer.saveNamedStyle(str(OUTPUT / "cheat.qml"))
message, ok = layer.loadNamedStyle(str(OUTPUT / "cheat.qml"))
layer.triggerRepaint()
```

## 11. Labels

Placement options: `AroundPoint`, `OverPoint`, `Horizontal`, `Curved` (lines), `Line`, `Free`.

```python
from qgis.core import QgsPalLayerSettings, QgsTextFormat, QgsTextBufferSettings, QgsVectorLayerSimpleLabeling
fmt = QgsTextFormat(); fmt.setSize(7); fmt.setColor(QColor("#222222"))
halo = QgsTextBufferSettings(); halo.setEnabled(True); halo.setSize(0.6); halo.setColor(QColor("white")); fmt.setBuffer(halo)
s = QgsPalLayerSettings(); s.fieldName = "name"; s.placement = Qgis.LabelPlacement.Horizontal; s.setFormat(fmt)
layer.setLabeling(QgsVectorLayerSimpleLabeling(s)); layer.setLabelsEnabled(True)
```

## 12. Layout and export

Order for a map item: size → CRS → layers → `zoomToExtent` → `setScale`. Check the export result.

```python
from qgis.core import QgsPrintLayout, QgsLayoutItemPage, QgsLayoutItemMap, QgsLayoutPoint, QgsLayoutSize, QgsLayoutExporter, QgsLayoutItemLabel
MM = Qgis.LayoutUnit.Millimeters
lay = QgsPrintLayout(project); lay.initializeDefaults(); lay.setName("Cheat")
lay.pageCollection().page(0).setPageSize("A4", QgsLayoutItemPage.Orientation.Portrait)
m = QgsLayoutItemMap(lay); m.setId("main_map")
m.attemptMove(QgsLayoutPoint(15, 30, MM)); m.attemptResize(QgsLayoutSize(180, 200, MM))
m.setCrs(utm); m.setLayers([layer]); m.zoomToExtent(box); m.setScale(2_500_000)   # extent in MAP crs; scale last
lay.addLayoutItem(m)
t = QgsLayoutItemLabel(lay); t.setText('[% @layout_name %]'); lay.addLayoutItem(t)
result = QgsLayoutExporter(lay).exportToPdf(str(OUTPUT / "cheat.pdf"), QgsLayoutExporter.PdfExportSettings())
if result != QgsLayoutExporter.ExportResult.Success:
    raise RuntimeError(result)
```

## 13. QGIS 3 + 4 in one script

See Module 09 for the full QGIS 3 → 4 table, and run `tools/check_code.py` on any script.

```python
from qgis.core import QgsLayoutItemLegend
legend = QgsLayoutItemLegend(lay)
if hasattr(legend, "setSyncMode"):                   # QGIS 4.0+
    legend.setSyncMode(Qgis.LegendSyncMode.Manual)
else:                                                # QGIS 3.x
    legend.setAutoUpdateModel(False)
newer = Qgis.QGIS_VERSION_INT >= 40000               # running QGIS 4?
```

More: [AI_PLAYBOOK.md](AI_PLAYBOOK.md) (red flags), [GLOSSARY.md](GLOSSARY.md), and the PyQGIS API docs at qgis.org/pyqgis/3.40/.
