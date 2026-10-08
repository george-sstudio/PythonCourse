"""
MODULE 11 - Review 4: one layer per continent

THE REQUEST
    "Export the countries of each continent as a separate layer (named after
     the continent) into ONE GeoPackage: output\\new_continents.gpkg. QGIS 3.40."

THE AI'S ANSWER is below. It prints "Done! Exported 8 continents."

YOUR JOB: review (# PROBLEM: ...), run, then fix until the checks pass.
Hint: four problems - one of them is in the very first line of the AI's code.
On Windows the AI's file isn't even created, yet the script says "Done!".
"""
from pathlib import Path

from qgis.core import (QgsExpressionContextUtils, QgsProject, QgsVectorFileWriter,
                       QgsVectorLayer)

COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
GPKG = COURSE / "data" / "natural_earth.gpkg"
OUTPUT = COURSE / "output"

# ======================= the AI's code starts here ==============================
out_file = str(OUTPUT) + "\new_continents.gpkg"

countries = QgsVectorLayer(f"{GPKG}|layername=countries", "countries", "ogr")
continents = sorted(countries.uniqueValues(countries.fields().indexOf("continent")))

for continent in continents:
    countries.setSubsetString(f"\"continent\" = '{continent}'")
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = continent
    options.actionOnExistingFile = QgsVectorFileWriter.ActionOnExistingFile.CreateOrOverwriteFile
    QgsVectorFileWriter.writeAsVectorFormatV3(
        countries, out_file, QgsProject.instance().transformContext(), options)

print(f"Done! Exported {len(continents)} continents.")
# ======================= the AI's code ends here ================================

# --- Checks (don't edit below this line) ------------------------------------
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
