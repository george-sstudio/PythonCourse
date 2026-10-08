"""
MODULE 05 - Exercise 4: copy -> add fields -> fill -> export -> verify

Make a GeoPackage output/module05.gpkg with a layer 'countries_stats' that
has these NEW fields:
    area_km2        Double   ellipsoidal area, 1 decimal
    density         Double   people per km2, 1 decimal - NULL if pop_est <= 0
    gdp_per_person  Double   US$ per person, whole number - NULL if gdp_md <= 0
                              (gdp_md is in MILLIONS of US$; -99 means unknown)
    size_class      Text     "large" (> 1,000,000 km2), "medium" (> 100,000), else "small"
"""
from pathlib import Path

from qgis.core import (QgsDistanceArea, QgsExpressionContextUtils, QgsFeatureRequest,
                       QgsField, QgsProject, QgsVariantUtils, QgsVectorFileWriter,
                       QgsVectorLayer, edit)
from qgis.PyQt.QtCore import QMetaType

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
OUTPUT = COURSE / "output"
OUTPUT.mkdir(exist_ok=True)
project = QgsProject.instance()

source = QgsVectorLayer(f"{GPKG}|layername=countries", "countries", "ogr")

# --- 1. work on a COPY -------------------------------------------------------------
# TODO: work = an in-memory copy of source (source.materialize(QgsFeatureRequest()))
work = None
if work is None:
    raise RuntimeError("Step 1: make the in-memory copy first (work = ...)")

# --- 2. add the four fields in one edit session ------------------------------------
# TODO: with edit(work): work.addAttribute(QgsField("area_km2", QMetaType.Type.Double)) ...
#       (QString for text)


# --- 3. fill them ------------------------------------------------------------------
da = QgsDistanceArea()
da.setSourceCrs(work.crs(), project.transformContext())
da.setEllipsoid("EPSG:7030")

idx = {name: work.fields().indexOf(name)
       for name in ["area_km2", "density", "gdp_per_person", "size_class"]}

# TODO: in an edit session, loop over work.getFeatures() and for each feature:
#         km2 = da.measureArea(f.geometry()) / 1_000_000
#         compute density (None if pop_est <= 0), gdp_per_person (None if
#         gdp_md <= 0), size_class, and write each with
#         work.changeAttributeValue(f.id(), idx["..."], value)


# --- 4. export ----------------------------------------------------------------------
out_path = OUTPUT / "module05.gpkg"
options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "GPKG"
options.layerName = "countries_stats"
options.actionOnExistingFile = QgsVectorFileWriter.ActionOnExistingFile.CreateOrOverwriteFile
# TODO: call QgsVectorFileWriter.writeAsVectorFormatV3(work, str(out_path),
#       project.transformContext(), options), unpack the 4 results, and raise
#       RuntimeError(message) if error != QgsVectorFileWriter.WriterError.NoError


# --- 5. verify: reopen the file -----------------------------------------------------
check = QgsVectorLayer(f"{out_path}|layername=countries_stats", "check", "ogr")
null_gdp = [f["name"] for f in check.getFeatures('"gdp_per_person" IS NULL')]
peru = next(check.getFeatures("\"adm0_a3\" = 'PER'"))
print("features:", check.featureCount(), "| unknown GDP:", null_gdp)
print("Peru:", peru["area_km2"], peru["density"], peru["gdp_per_person"], peru["size_class"])

# --- Checks (don't edit below this line) ------------------------------------
assert check.isValid() and check.featureCount() == 242
assert source.fields().indexOf("area_km2") == -1, "the SOURCE must stay untouched"
assert len(null_gdp) == 5 and "Vatican" in null_gdp, f"gdp NULLs: {null_gdp}"
assert len(list(check.getFeatures('"density" IS NULL'))) == 2
assert 1_290_000 < peru["area_km2"] < 1_300_000
assert peru["size_class"] == "large"
assert round(peru["gdp_per_person"]) == 6978
assert not QgsVariantUtils.isNull(peru["density"])
print("All checks passed ✔")
