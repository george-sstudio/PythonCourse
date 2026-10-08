# How this course uses the book

**Book:** Bonny P. McClain, *Python for Geospatial Data Analysis: Theory, Tools, and Practice for Location Intelligence* (O'Reilly, 2022).

The book is a broad tour: QGIS, Google Earth Engine, OSMnx, the ArcGIS API, GeoPandas, GDAL and climate data. This course has a narrower goal (**automate QGIS** and **direct AI well**), so it keeps the QGIS core, updates it for QGIS 3.40 and 4.x, and drops or shrinks the rest. The table shows what happened to each chapter and why.

| Ch. | Book chapter | In this course | Why |
|---|---|---|---|
| 1 | Introduction to Geospatial Analytics (projections, vector, raster, choosing data) | **Kept**: Module 04 (CRS and units), `data/README.md` (choosing and checking data) | CRS and units are the #1 source of wrong AI code. Taught hands-on, with the "degrees aren't distances" demos. |
| 2 | Essential Facilities: QGIS, Python Console, loading layers, raster layers | **Kept and updated**: Modules 00, 03, 04, 07 | `iface.addVectorLayer` → `QgsVectorLayer` + `isValid()`; star markers via `Qgis.MarkerShape.Star`; the book's `print(...format(...)` typo becomes a debugging exercise (02). US data (NYC complaints, redlining) replaced by world data that works offline. |
| 3 | PyQGIS and native algorithms: iterators, attributes, styling, `processing.run`, extract/buffer/extract-by-location | **Kept, expanded and corrected**: Modules 05, 06, 07 | The Amazonas chain is kept, and its **0.1-degree buffer** becomes the core lesson of Module 06 (correct on the equator by luck, wrong on the Lena). Adds History → "Copy as Python Command", `algorithmHelp`, batch loops, raster tools. |
| 4 | Google Earth Engine, geemap, Leafmap | **Dropped** | Needs an online account and cloud processing, and is outside "automate QGIS". Good later reading if you need satellite time series. |
| 5 | OpenStreetMap with OSMnx; QuickOSM | **Mentioned** (Module 06 note) | OSMnx is a separate library; inside QGIS, the QuickOSM plugin (also runnable via `processing.run`) does the job. Needs internet. |
| 6 | The ArcGIS Python API | **Dropped** | Proprietary platform. You use QGIS. |
| 7 | GeoPandas and spatial statistics; Census API | **Shrunk**: the *ideas* (reading fields, filtering, joins, measuring) are taught in PyQGIS in Module 05; GeoPandas is listed as a next step (Module 12) | Outside QGIS. AI writes GeoPandas well, and Modules 03 and 11 teach you to read and check it. The US Census API is US-specific. |
| 8 | Data cleaning (missing data, types, summary statistics, missingno) | **Kept in QGIS form**: Module 05 (NULL vs `None`, `-99` codes, min/max checks) and 07 (the −99 choropleth trap) | Same habits, no pandas or Colab needed, plus the QGIS 3 → 4 NULL change the book predates. |
| 9 | GDAL: command line, warp, Spyder; EarthExplorer, Copernicus hub | **Kept via Processing**: Module 06 (`gdal:warpreproject`, hillshade, slope, contours, no-data) | GDAL comes with QGIS, so no separate install or Spyder. The Copernicus Open Access Hub the book links to **closed at the end of October 2023**; Sentinel data now comes from the Copernicus Data Space Ecosystem. |
| 10 | Climate data (xarray), deforestation (WTSS, Forest at Risk) | **Dropped** | Specialised research libraries, mostly online. Not needed for QGIS automation. |
| — | *Not in the book* | **Added**: Modules 08 (print layouts, atlases, templates), 09 (Processing tools, QGIS 4 readiness), 10–12 (directing and reviewing AI) | Print cartography and reliable, reviewable automation are where your time goes. AI changed what's worth learning by hand. |

## What "outdated" meant in practice

These are things in the book's code that no longer work, or no longer work the same way, in 2026:

| Book (2022) | Now | Course module |
|---|---|---|
| `"OUTPUT": "memory:"` | `"TEMPORARY_OUTPUT"` (`memory:` still works) | 06 |
| `QgsSimpleMarkerSymbolLayerBase.Star` | `Qgis.MarkerShape.Star` | 07, 09 |
| `from PyQt5...` (in many online examples) | `from qgis.PyQt...` (required in QGIS 4) | 03, 09 |
| `QVariant.Double` field types | `QMetaType.Type.Double` | 05, 09 |
| Buffer distance `0.1 # degrees` | buffer in metres in a projected CRS | 06, 09 |
| Copernicus Open Access Hub | Copernicus Data Space Ecosystem | (reference) |
| Spyder / Colab for GDAL | Processing in QGIS, or the OSGeo4W Shell | 06 |
| Typing scripts by hand | brief → AI draft → review → verify | 10–12 |
