"""
describe_project.py - make a "context card" of the open QGIS project for an AI.

AI can't see your project. This script writes down the facts it needs: QGIS
version, project CRS, every layer's source, CRS and units, geometry type,
feature count, fields with their types, a few sample values, NULL counts,
and the print layouts with their item ids. The result is Markdown text you
paste at the top of a request to Claude.

How to use it in QGIS:
  1. Open the project you're working on.
  2. Open this file in the Python editor and click Run Script.
  3. The card is printed AND saved to <course>/output/context_card.md
     (or next to the project file, if the course variable isn't set).

Privacy: the card includes up to 3 sample values per field. Set SAMPLES = 0
if your attributes are private.
"""
from pathlib import Path

from qgis.core import (Qgis, QgsExpressionContextUtils, QgsLayoutItem, QgsMapLayer,
                       QgsProject, QgsRasterLayer, QgsUnitTypes, QgsVariantUtils,
                       QgsVectorLayer, QgsWkbTypes)

SAMPLES = 3           # sample values per field (0 = none)
MAX_FIELDS = 40       # long tables: list the first N fields only


def short_source(layer):
    """The layer's data source with the folder shortened (paths can be long)."""
    source = layer.source()
    path, _, rest = source.partition("|")
    p = Path(path)
    shown = f"…/{p.parent.name}/{p.name}" if p.parent.name else p.name
    return shown + (f"|{rest}" if rest else "")


def crs_text(crs):
    if not crs.isValid():
        return "NO CRS (unknown!)"
    units = QgsUnitTypes.toString(crs.mapUnits())
    return f"{crs.authid()} - {crs.description()} (units: {units})"


def field_lines(layer):
    """One line per field: name, type, NULL count, sample values."""
    lines = []
    total = layer.featureCount()
    for i, field in enumerate(layer.fields()):
        if i >= MAX_FIELDS:
            lines.append(f"  - … and {len(layer.fields()) - MAX_FIELDS} more fields")
            break
        nulls = 0
        samples = []
        for f in layer.getFeatures():
            value = f[field.name()]
            if QgsVariantUtils.isNull(value):
                nulls += 1
            elif len(samples) < SAMPLES and value not in samples:
                samples.append(value)
        sample_text = ", ".join(repr(v) for v in samples) if SAMPLES else "(hidden)"
        null_text = f", {nulls}/{total} NULL" if nulls else ""
        lines.append(f"  - `{field.name()}` ({field.typeName()}{null_text}): {sample_text}")
    return lines


def describe_vector(layer):
    geometry = QgsWkbTypes.displayString(layer.wkbType())
    lines = [f"- **{layer.name()}** - vector, {geometry}, {layer.featureCount()} features",
             f"  - source: `{short_source(layer)}` (provider `{layer.providerType()}`)",
             f"  - CRS: {crs_text(layer.crs())}"]
    if layer.subsetString():
        lines.append(f"  - FILTER active: `{layer.subsetString()}`")
    if layer.selectedFeatureCount():
        lines.append(f"  - {layer.selectedFeatureCount()} features selected")
    lines.append("  - fields:")
    lines += ["  " + line for line in field_lines(layer)]
    return lines


def describe_raster(layer):
    provider = layer.dataProvider()
    lines = [f"- **{layer.name()}** - raster, {layer.width()} x {layer.height()} px, "
             f"{layer.bandCount()} band(s)",
             f"  - source: `{short_source(layer)}`",
             f"  - CRS: {crs_text(layer.crs())}",
             f"  - pixel size: {layer.rasterUnitsPerPixelX():g} x {layer.rasterUnitsPerPixelY():g} "
             f"(map units)"]
    for band in range(1, layer.bandCount() + 1):
        nodata = provider.sourceNoDataValue(band) if provider.sourceHasNoDataValue(band) else "none"
        data_type = getattr(provider.dataType(band), "name", provider.dataType(band))
        lines.append(f"  - band {band}: {data_type}, no-data = {nodata}")
    return lines


def describe_layouts(project):
    lines = []
    for layout in project.layoutManager().printLayouts():
        ids = [item.id() for item in layout.items()
               if isinstance(item, QgsLayoutItem) and item.id()]
        page = layout.pageCollection().page(0)
        size = f"{page.pageSize().width():g} x {page.pageSize().height():g} mm" if page else "?"
        lines.append(f"- layout **{layout.name()}** ({size}); item ids: "
                     + (", ".join(f"`{i}`" for i in ids) if ids else "(none set)"))
    return lines or ["- (no print layouts)"]


def context_card(project=None):
    """Return the context card as Markdown text."""
    project = project or QgsProject.instance()
    lines = ["## Context: my QGIS project",
             f"- QGIS {Qgis.version()} (PyQGIS). Code must also work in QGIS 4.x.",
             f"- project file: `{Path(project.fileName()).name or '(not saved)'}`",
             f"- project CRS: {crs_text(project.crs())}",
             "",
             "### Layers (top of the Layers panel first)"]
    root = project.layerTreeRoot()
    for node in root.findLayers():
        layer = node.layer()
        if layer is None:
            continue
        if isinstance(layer, QgsVectorLayer):
            lines += describe_vector(layer)
        elif isinstance(layer, QgsRasterLayer):
            lines += describe_raster(layer)
        else:
            lines.append(f"- **{layer.name()}** - {layer.type()}")
        if not node.isVisible():
            lines.append("  - (hidden in the Layers panel)")
    lines += ["", "### Print layouts"] + describe_layouts(project)
    return "\n".join(lines)


def save_card(text):
    course = QgsExpressionContextUtils.globalScope().variable("course_root")
    if course:
        out = Path(course) / "output" / "context_card.md"
    elif QgsProject.instance().fileName():
        out = Path(QgsProject.instance().fileName()).with_name("context_card.md")
    else:
        out = Path.home() / "context_card.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return out


if __name__ in ("__main__", "__console__"):
    card = context_card()
    print(card)
    print("\nSaved to:", save_card(card))
