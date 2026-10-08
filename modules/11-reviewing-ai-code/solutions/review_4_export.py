"""
MODULE 11 - Review 4 (solution): one layer per continent

PROBLEMS FOUND
  1. str(OUTPUT) + "\new_continents.gpkg": "\n" is a NEWLINE character, so the
     path is broken. On Windows the file can't be created at all.
     Use OUTPUT / "new_continents.gpkg".          (checklist 5; Module 01)
  2. CreateOrOverwriteFile inside the loop: every continent REPLACES the whole
     file, so at best only the last continent survives. Create the file for
     the first layer, then CreateOrOverwriteLayer for the rest. (checklist 5)
  3. The writer's return value is ignored, so failures are silent and the script
     still prints "Done!".                          (checklist 6)
  4. The countries layer is left with a filter on it (side effect). Clear
     it at the end - or better, don't filter the shared layer at all: use
     options.filterFeatureIds / a request, or a loop over extracts.
  Also: f"... '{continent}'" is safe here only because no continent name
  contains an apostrophe - QgsExpression.quotedValue() makes it safe always.
"""
from pathlib import Path

from qgis.core import (QgsExpression, QgsExpressionContextUtils, QgsProject,
                       QgsVectorFileWriter, QgsVectorLayer)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
OUTPUT = COURSE / "output"
OUTPUT.mkdir(exist_ok=True)

out_file = OUTPUT / "new_continents.gpkg"                            # fix 1
if out_file.exists():
    out_file.unlink()

countries = QgsVectorLayer(f"{GPKG}|layername=countries", "countries", "ogr")
if not countries.isValid():
    raise RuntimeError("countries did not load")
continents = sorted(countries.uniqueValues(countries.fields().indexOf("continent")))

try:
    for i, continent in enumerate(continents):
        countries.setSubsetString(f"\"continent\" = {QgsExpression.quotedValue(continent)}")
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "GPKG"
        options.layerName = continent
        options.actionOnExistingFile = (                               # fix 2
            QgsVectorFileWriter.ActionOnExistingFile.CreateOrOverwriteFile if i == 0
            else QgsVectorFileWriter.ActionOnExistingFile.CreateOrOverwriteLayer)
        error, message, _, _ = QgsVectorFileWriter.writeAsVectorFormatV3(
            countries, str(out_file), QgsProject.instance().transformContext(), options)
        if error != QgsVectorFileWriter.WriterError.NoError:            # fix 3
            raise RuntimeError(f"{continent}: {message}")
        print(f"{continent}: {countries.featureCount()} countries")
finally:
    countries.setSubsetString("")                                      # fix 4

print(f"Done! Exported {len(continents)} continents to {out_file.name}.")

from qgis.core import QgsProviderRegistry
target = OUTPUT / "new_continents.gpkg"
assert target.exists(), f"{target.name} was not created"
names = [s.name() for s in QgsProviderRegistry.instance().querySublayers(str(target))]
made = {n: QgsVectorLayer(f"{target}|layername={n}", n, "ogr").featureCount() for n in names}
print("layers in the file:", made)
assert len(made) == 8, f"expected 8 layers, found {len(made)}: {sorted(made)}"
assert made.get("Africa") == 54 and sum(made.values()) == 242, made
assert countries.subsetString() == "", "the countries layer was left filtered"
print("All checks passed ✔")
