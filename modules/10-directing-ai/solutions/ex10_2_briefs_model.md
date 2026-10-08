# Exercise 10.2: Model briefs

These are *examples*, not the only right answers. The parts to compare are the **decisions** made explicit and the **checks**, especially the trap cases.

---

## Brief A: cities near rivers

```text
## Goal
A layer of populated places that lie within 10 km of a river.

## Context
<context card> - QGIS 3.40, must also run in 4.x. Both layers are EPSG:4326 (degrees).

## Inputs
- natural_earth.gpkg | layername=places   (1,251 points; name, adm0name, pop_max)
- natural_earth.gpkg | layername=rivers   (478 lines; featurecla 'River' or 'Lake Centerline')
  Use only "featurecla" = 'River'.

## Output
- D:\PythonCourse\output\cities_near_rivers.gpkg, layer "cities_near_rivers",
  EPSG:4326, all fields of places, plus "river" (the name of the nearest river)
  and "dist_km" (distance to it, 1 decimal).

## Rules
- Distances in METRES: do the buffer/distance in a projected CRS suited to each
  area, or with an ellipsoidal method. Never buffer in degrees.
- Don't modify natural_earth.gpkg.
- Use Processing tools where possible.

## Checks
- Every output place has dist_km <= 10.
- Trap (high latitude): Yakutsk and Zhigansk are within 10 km of the Lena
  (a degree-based buffer misses them).
- Trap (equator): Iquitos, Leticia, Santarém are within 10 km of the Amazonas.
- The output CRS is EPSG:4326 and its feature count is printed.

## How I want the answer
Plan first (numbered, with assumptions). Then functions with docstrings,
asserts for the checks at the end.
```

**What the trap cases catch:** the classic "buffer by 0.1°" solution passes the Amazon check and fails the Lena check.

---

## Brief B: countries by wealth

```text
## Goal
A choropleth of the countries layer by GDP per person, saved as a reusable QML.

## Context
<context card>. gdp_md is GDP in MILLIONS of US$; -99 and 0 mean "unknown".

## Inputs
- natural_earth.gpkg | layername=countries (242 polygons; gdp_md, pop_est)

## Output
- Graduated renderer on the expression
  gdp_md * 1,000,000 / pop_est  (US$ per person), 5 classes, Jenks,
  colour ramp YlGnBu, white 0.1 mm outlines; legend labels with thousands
  separators and no decimals.
- Countries with unknown GDP drawn in light grey (#e4e4e4) and labelled
  "No data" in the legend.
- Saved to D:\PythonCourse\output\styles\gdp_per_person.qml

## Rules
- Unknown values (gdp_md <= 0 or pop_est <= 0) must NOT take part in the
  classification.
- QGIS 3.40/4.x compatible (scoped enums, qgis.PyQt).

## Checks
- The lowest class starts above 0 (a negative start means -99 slipped in).
- Vatican, and the other gdp_md <= 0 territories, are in "No data".
- Exactly 5 classes, plus the no-data symbol.
- The QML file exists, and loading it onto a fresh countries layer gives the same classes.

## How I want the answer
Plan first; then code; print the class breaks at the end.
```

**What the trap cases catch:** a naive `"gdp_md" * 1e6 / "pop_est"` puts Vatican at −120,000 US$ and wrecks the lowest class.

---

## Brief C: terrain from the DEM

```text
## Goal
Terrain layers from dem_sample.tif - hillshade, hypsometric tints and
100 m contours - styled and saved as a QGIS project.

## Context
<context card>. The DEM is EPSG:4326 (degrees horizontally, metres vertically),
1200x1200 px, Float32, values about -430 to +1300 m (Dead Sea to hills).

## Inputs
- D:\PythonCourse\data\dem_sample.tif

## Output (all in D:\PythonCourse\output\terrain\)
- dem_utm.tif: reprojected to EPSG:32636 (UTM 36N), 90 m, bilinear, no-data -9999
- hillshade.tif (azimuth 315, altitude 45), slope.tif (degrees)
- contours_100m.gpkg, field "elev"
- terrain.qgz with: tints (my colour stops: -430 #8fb3c9, 0 #a9c59a,
  300 #d8d8a8, 700 #c9a77c, 1300 #f2eee6), hillshade multiply 55%,
  contours 0.12 mm, index contours every 500 m 0.35 mm with labels

## Rules
- Slope and hillshade must be computed on the METRIC DEM, not the degree DEM.
- Set no-data on the reprojected DEM, so its empty corners aren't zeros.
- Nothing written outside output\terrain.

## Checks
- dem_utm.tif is EPSG:32636 with 90 m pixels.
- Trap: mean slope between 5° and 9° and max below 70° (on the degree DEM the
  max is 90°, everywhere steep).
- Contour elev values run from -400 to 1200.
- terrain.qgz opens with 4 layers in the right order.

## How I want the answer
Plan first; then one function per product; asserts at the end.
```

**What the trap cases catch:** slope or hillshade run directly on the EPSG:4326 DEM, and a reprojection without no-data (fake cliffs at the edges).
