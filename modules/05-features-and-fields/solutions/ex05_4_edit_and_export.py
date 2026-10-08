"""MODULE 05 - Solution 4: copy -> add fields -> fill -> export -> verify"""
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

# 1. a copy in memory - the source file is never opened for editing
work = source.materialize(QgsFeatureRequest())

# 2. new fields
with edit(work):
    work.addAttribute(QgsField("area_km2", QMetaType.Type.Double))
    work.addAttribute(QgsField("density", QMetaType.Type.Double))
    work.addAttribute(QgsField("gdp_per_person", QMetaType.Type.Double))
    work.addAttribute(QgsField("size_class", QMetaType.Type.QString))

# 3. fill
da = QgsDistanceArea()
da.setSourceCrs(work.crs(), project.transformContext())
da.setEllipsoid("EPSG:7030")

idx = {name: work.fields().indexOf(name)
       for name in ["area_km2", "density", "gdp_per_person", "size_class"]}


def size_class(km2):
    if km2 > 1_000_000:
        return "large"
    elif km2 > 100_000:
        return "medium"
    return "small"


with edit(work):
    for f in work.getFeatures():
        km2 = da.measureArea(f.geometry()) / 1_000_000
        pop = f["pop_est"]
        gdp = f["gdp_md"]

        density = round(pop / km2, 1) if pop > 0 else None          # None -> NULL
        gdp_pp = round(gdp * 1_000_000 / pop) if gdp > 0 and pop > 0 else None

        work.changeAttributeValue(f.id(), idx["area_km2"], round(km2, 1))
        work.changeAttributeValue(f.id(), idx["density"], density)
        work.changeAttributeValue(f.id(), idx["gdp_per_person"], gdp_pp)
        work.changeAttributeValue(f.id(), idx["size_class"], size_class(km2))

# 4. export
out_path = OUTPUT / "module05.gpkg"
options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "GPKG"
options.layerName = "countries_stats"
options.actionOnExistingFile = QgsVectorFileWriter.ActionOnExistingFile.CreateOrOverwriteFile
error, message, path, layer_name = QgsVectorFileWriter.writeAsVectorFormatV3(
    work, str(out_path), project.transformContext(), options)
if error != QgsVectorFileWriter.WriterError.NoError:
    raise RuntimeError(message)

# 5. verify
check = QgsVectorLayer(f"{out_path}|layername=countries_stats", "check", "ogr")
null_gdp = [f["name"] for f in check.getFeatures('"gdp_per_person" IS NULL')]
peru = next(check.getFeatures("\"adm0_a3\" = 'PER'"))
print("features:", check.featureCount(), "| unknown GDP:", null_gdp)
print("Peru:", peru["area_km2"], peru["density"], peru["gdp_per_person"], peru["size_class"])

assert check.isValid() and check.featureCount() == 242
assert source.fields().indexOf("area_km2") == -1, "the SOURCE must stay untouched"
assert len(null_gdp) == 5 and "Vatican" in null_gdp, f"gdp NULLs: {null_gdp}"
assert len(list(check.getFeatures('"density" IS NULL'))) == 2
assert 1_290_000 < peru["area_km2"] < 1_300_000
assert peru["size_class"] == "large"
assert round(peru["gdp_per_person"]) == 6978
assert not QgsVariantUtils.isNull(peru["density"])
print("All checks passed ✔")
