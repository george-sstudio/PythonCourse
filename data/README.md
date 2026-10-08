# Course data

Everything here is small, open data, so the course works offline. Don't edit these files. Scripts read from `data/` and write to `output/`.

## `natural_earth.gpkg`: one GeoPackage, nine layers

A **GeoPackage** (`.gpkg`) is a single file that can hold many layers. Think of it as a folder of shapefiles in one file. To load one layer, add `|layername=…` to the path (see Module 04).

All layers are in **EPSG:4326** (WGS 84 latitude/longitude, measured in **degrees**). That matters for any measuring. See Module 04.

| Layer | Geometry | Features | Fields (short names, lower case) |
|---|---|---|---|
| `countries` | polygons | 242 | `name`, `name_long`, `adm0_a3` (3-letter code), `iso_a3`, `continent`, `region_un`, `subregion`, `pop_est`, `pop_year`, `gdp_md` (GDP, million US$), `economy`, `income_grp`, `mapcolor7` |
| `countries_110m` | polygons | 177 | simpler, coarser countries: `name`, `adm0_a3`, `iso_a3`, `continent`, `pop_est` |
| `places` | points | 1,251 | populated places: `name`, `nameascii`, `adm0name` (country), `adm0_a3`, `adm1name`, `featurecla` (type, e.g. `Admin-0 capital`), `scalerank`, `pop_max`, `pop_min`, `latitude`, `longitude`, `worldcity`, `megacity` |
| `rivers` | lines | 478 | `name`, `featurecla` (`River` / `Lake Centerline`), `scalerank` |
| `lakes` | polygons | 412 | `name`, `featurecla`, `scalerank` |
| `coastline` | lines | 1,428 | `scalerank` |
| `ocean` | polygons | 1 | `scalerank` |
| `graticule_10` | lines | 53 | 10° latitude/longitude lines: `degrees`, `direction`, `display` |
| `admin1` | polygons | 294 | states/provinces of 9 large countries: `name`, `name_en`, `admin` (country), `adm0_a3`, `type_en`, `iso_3166_2` |

**Known quirks (on purpose: real data is messy, and AI code often trips on these):**

- `iso_a3` is `-99` for France, Norway, Kosovo and a few others. Use **`adm0_a3`** to identify countries.
- `gdp_md` is `-99` or `0` for a few tiny territories (e.g. Vatican), which means "unknown", not a real value.
- `countries` France includes French Guiana and other overseas parts in one multipolygon.

## `capitals.csv`

215 national capitals as plain text with `latitude`/`longitude` columns (made from `places`). It's used to practise loading CSV points (Module 04) and reading files with Python (Module 02).

## `world_shaded_relief.tif`

A grey shaded-relief image of the world (2700 × 1350 pixels, EPSG:4326), good as a quiet background layer.

## `dem_sample.tif`

A **DEM** (digital elevation model: a raster where each pixel holds a height in metres) for 1° × 1° from 31–32°N, 35–36°E: the Judean hills, the Jordan valley and the Dead Sea. That's a big range of elevation, from about −427 m to +1,294 m. 1200 × 1200 pixels at 3 arc-seconds (about 90 m), EPSG:4326, float32. Used for hillshade, contours and slope (Module 06).

## Sources and licences

| File | Source | Licence |
|---|---|---|
| `natural_earth.gpkg`, `capitals.csv`, `world_shaded_relief.tif` | [Natural Earth](https://www.naturalearthdata.com/) v5.1.1 (1:50m and 1:110m), fields trimmed and renamed to lower case; relief from the 1:50m *Gray Earth* raster, resampled | Public domain |
| `dem_sample.tif` | [Copernicus DEM GLO-30](https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model) tile `N31_00_E035_00`, resampled from 30 m to about 90 m (average) | © DLR e.V. 2010–2014 and © Airbus Defence and Space GmbH 2014–2018, provided under COPERNICUS by the European Union and ESA; all rights reserved. Free to use with this attribution. |
