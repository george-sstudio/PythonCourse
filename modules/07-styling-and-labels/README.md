# Module 07: Styling, labels and QML

**Time:** about 4 hours · **Week 3** · Book: Ch. 2 (renderer, `setSize`, star markers), Ch. 3 (layer styling)

Styling by hand is fine for one map. Code is for when the **same** style goes onto many layers or maps, for applying a palette exactly (hex codes, mm widths), or for rebuilding a style reliably from a recipe. QML files are the bridge: the GUI and code read and write the same file.

## You will

- understand how QGIS draws a layer: **renderer → symbol → symbol layers**
- make single-symbol, categorized, graduated and rule-based styles by code
- size symbols from data (**data-defined properties**)
- style a DEM with a hypsometric colour ramp and a hillshade in *multiply* mode
- add labels: font, size, buffer, placement, labelling only some features
- save and load **QML** style files, and apply one style to many layers

## Key words

| Word | Meaning |
|---|---|
| **Renderer** | The layer's drawing *rule*: "same symbol for all", "colour by category", "colour by class of a number", or "by rules". |
| **Symbol** | What one feature looks like: a marker, a line or a fill. |
| **Symbol layer** | One piece of a symbol. A fill symbol can stack a simple fill plus a dashed outline plus a shadow. Index `0` is the bottom piece. |
| **Categorized** | One symbol per distinct value (continent → colour). |
| **Graduated** | Numbers split into **classes** (ranges), one colour per class (a choropleth). |
| **Classification method** | How the class breaks are chosen: Jenks (natural breaks), Quantile (equal counts), Equal interval, Pretty. |
| **Rule-based** | Each symbol has an expression (and optionally a scale range) deciding which features get it. |
| **Data-defined property** | A symbol setting (size, colour, rotation…) computed from an expression per feature. |
| **Colour ramp** | A smooth sequence of colours used to colour classes or raster values. |
| **Blend mode** | How a layer's colours mix with those below: *Multiply* darkens like ink on paper, which is ideal for hillshades. |
| **QML** | QGIS's style file (`.qml`, XML text). Holds the renderer, labels, opacity, blending… |
| **mm, points, map units** | Symbol units. Print cartography uses **mm** (QGIS's default) and **points** for fonts. |

---

## 1. How a layer is drawn

```text
layer
 └── renderer               e.g. QgsSingleSymbolRenderer / Categorized / Graduated / RuleBased
      └── symbol(s)          QgsFillSymbol, QgsLineSymbol, QgsMarkerSymbol
           └── symbol layers  [0] simple fill, [1] outline, ...
```

The book changes a marker like this:

```python
vlayer.renderer().symbol().setSize(6)
vlayer.renderer().symbol().symbolLayer(0).setShape(QgsSimpleMarkerSymbolLayerBase.Star)
```

That still works, but the shape enum is now spelled `Qgis.MarkerShape.Star` (QGIS 3.24+, and required in 4.x). After changing a style in the live window, call `layer.triggerRepaint()`, and `iface.layerTreeView().refreshLayerSymbology(layer.id())` to update the legend.

## 2. Single symbol

`createSimple` takes a dictionary of the same settings you see in the Symbol dialog. The keys are QGIS's internal names; the easiest way to discover them is to save a QML and read it (section 8).

```python
from qgis.core import QgsFillSymbol, QgsLineSymbol, QgsMarkerSymbol, QgsSingleSymbolRenderer

land = QgsFillSymbol.createSimple({
    "color": "#ece6d6", "outline_color": "#9a958a", "outline_width": "0.15"})   # mm
countries.setRenderer(QgsSingleSymbolRenderer(land))

water = QgsLineSymbol.createSimple({"color": "#6f94b8", "width": "0.25", "capstyle": "round"})
rivers.setRenderer(QgsSingleSymbolRenderer(water))

dot = QgsMarkerSymbol.createSimple({"name": "circle", "color": "#333333",
                                    "size": "1.6", "outline_style": "no"})
places.setRenderer(QgsSingleSymbolRenderer(dot))
```

Layer-level settings:

```python
from qgis.PyQt.QtGui import QPainter
hillshade.setOpacity(0.6)
hillshade.setBlendMode(QPainter.CompositionMode.CompositionMode_Multiply)
```

## 3. Categorized: your palette, your categories

```python
from qgis.core import QgsCategorizedSymbolRenderer, QgsRendererCategory

palette = {"Africa": "#e3c9a5", "Asia": "#e8d9a9", "Europe": "#c7d3e3",
           "North America": "#cfdcc0", "South America": "#d9c7dd", "Oceania": "#c6e0dc"}

categories = []
for continent, colour in palette.items():
    sym = QgsFillSymbol.createSimple({"color": colour, "outline_color": "#ffffff", "outline_width": "0.1"})
    categories.append(QgsRendererCategory(continent, sym, continent))   # value, symbol, legend label

# a catch-all for every value NOT listed (e.g. 'Antarctica', 'Seven seas (open ocean)')
other = QgsFillSymbol.createSimple({"color": "#e4e4e4", "outline_color": "#ffffff", "outline_width": "0.1"})
categories.append(QgsRendererCategory(None, other, "Other"))

countries.setRenderer(QgsCategorizedSymbolRenderer("continent", categories))
```

`layer.uniqueValues(layer.fields().indexOf("continent"))` lists the values that actually exist. Compare it with your palette, so you know nothing gets lost in "Other" by accident.

## 4. Graduated: classes of numbers

```python
from qgis.core import QgsClassificationJenks, QgsGraduatedSymbolRenderer, QgsStyle

gdp_pp = 'CASE WHEN "gdp_md" > 0 AND "pop_est" > 0 THEN "gdp_md" * 1000000 / "pop_est" END'
r = QgsGraduatedSymbolRenderer(gdp_pp)          # a field name OR an expression
r.setClassificationMethod(QgsClassificationJenks())
r.updateClasses(countries, 5)                    # compute 5 classes from the data
r.updateColorRamp(QgsStyle.defaultStyle().colorRamp("YlGnBu"))
countries.setRenderer(r)

for rng in r.ranges():
    print(rng.lowerValue(), rng.upperValue(), rng.label())
```

**Why the `CASE WHEN`?** Without it, Vatican's `gdp_md = -99` makes a GDP per person of **−120,000 US$**, and your lowest class starts there. The `CASE` turns unknown values into NULL, and NULL features are left out of the classes. (Draw a grey "no data" layer underneath so they don't vanish from the map.)

> **Always print the class breaks.** A legend that starts at −120,000 or ends at 10¹² is the cheapest data-quality alarm there is.

Manual breaks (when *you* decide the classes, as cartographers usually do):

```python
from qgis.core import QgsRendererRange
breaks = [(0, 1000), (1000, 4000), (4000, 12000), (12000, 40000), (40000, 250000)]
ramp = QgsStyle.defaultStyle().colorRamp("YlGnBu")
ranges = []
for i, (lo, hi) in enumerate(breaks):
    sym = QgsFillSymbol.createSimple({"outline_color": "#ffffff", "outline_width": "0.1"})
    sym.setColor(ramp.color(i / (len(breaks) - 1)))
    ranges.append(QgsRendererRange(lo, hi, sym, f"{lo:,} – {hi:,}"))
countries.setRenderer(QgsGraduatedSymbolRenderer(gdp_pp, ranges))
```

## 5. Rule-based: different symbols by expression

```python
from qgis.core import QgsRuleBasedRenderer

root = QgsRuleBasedRenderer.Rule(None)              # an invisible top rule
root.appendChild(QgsRuleBasedRenderer.Rule(
    QgsMarkerSymbol.createSimple({"name": "square", "color": "#b03a2e", "size": "2.2"}),
    filterExp="\"featurecla\" LIKE 'Admin-0 capital%'", label="Capital"))
root.appendChild(QgsRuleBasedRenderer.Rule(
    QgsMarkerSymbol.createSimple({"name": "circle", "color": "#333333", "size": "1.2"}),
    elseRule=True, label="Other place"))           # everything not matched above
places.setRenderer(QgsRuleBasedRenderer(root))
```

Rules can also have scale limits (`rule.setMinimumScale(...)` / `setMaximumScale(...)`), for symbols that appear only when zoomed in.

## 6. Data-defined size (proportional symbols)

```python
from qgis.core import QgsProperty, QgsSymbolLayer

sym = QgsMarkerSymbol.createSimple({"name": "circle", "color": "51,51,51,153", "outline_color": "#ffffff"})
sym.symbolLayer(0).setDataDefinedProperty(
    QgsSymbolLayer.Property.Size,
    QgsProperty.fromExpression('scale_linear(sqrt("pop_max"), 0, 6000, 1, 7)'))
```

`sqrt` makes the circle's **area** (not its width) proportional to population, which is the cartographically honest choice. `scale_linear(value, in_min, in_max, out_min, out_max)` maps the result to 1–7 mm. `"51,51,51,153"` is red, green, blue, **alpha** (opacity, 0–255, so 153 is 60%).

> **Transparency trap:** on the web (CSS), `#33333399` means "grey, 60% opaque" (alpha *last*). QGIS uses Qt, which reads 8-digit hex as **`#AARRGGBB`** (alpha *first*). So in QGIS `#33333399` is a 20%-opaque **blue**. AI writes the CSS form all the time. Use `"R,G,B,A"` text, or set alpha separately: `c = QColor("#333333"); c.setAlpha(153)`.

## 7. Rasters: hypsometric tints and hillshade

```python
from qgis.core import (QgsColorRampShader, QgsRasterShader,
                       QgsSingleBandPseudoColorRenderer)
from qgis.PyQt.QtGui import QColor

stops = [(-430, "#8fb3c9"), (0, "#a9c59a"), (300, "#d8d8a8"),
         (700, "#c9a77c"), (1000, "#a8876a"), (1300, "#f2eee6")]
shader = QgsColorRampShader()
shader.setColorRampType(QgsColorRampShader.Type.Interpolated)
shader.setColorRampItemList([QgsColorRampShader.ColorRampItem(v, QColor(c), str(v)) for v, c in stops])
raster_shader = QgsRasterShader()
raster_shader.setRasterShaderFunction(shader)
dem.setRenderer(QgsSingleBandPseudoColorRenderer(dem.dataProvider(), 1, raster_shader))

hillshade.setBlendMode(QPainter.CompositionMode.CompositionMode_Multiply)   # put it ABOVE the DEM
hillshade.setOpacity(0.55)
```

Your hand-tuned colour stops become a few lines of code you can reuse on every map of a series.

## 8. Labels

```python
from qgis.core import (Qgis, QgsPalLayerSettings, QgsTextBufferSettings,
                       QgsTextFormat, QgsVectorLayerSimpleLabeling)
from qgis.PyQt.QtGui import QColor, QFont

fmt = QgsTextFormat()
fmt.setFont(QFont("IBM Plex Sans"))       # any installed font family
fmt.setSize(7)                             # points
fmt.setColor(QColor("#222222"))

buffer = QgsTextBufferSettings()           # the halo
buffer.setEnabled(True)
buffer.setSize(0.6)                        # mm
buffer.setColor(QColor("#ffffff"))
fmt.setBuffer(buffer)

settings = QgsPalLayerSettings()
settings.fieldName = "name"                # or an expression:
# settings.fieldName = "upper(\"name\")"; settings.isExpression = True
settings.placement = Qgis.LabelPlacement.AroundPoint      # points
# Qgis.LabelPlacement.Curved for rivers, .Horizontal / .OverPoint, ...
settings.setFormat(fmt)

places.setLabeling(QgsVectorLayerSimpleLabeling(settings))
places.setLabelsEnabled(True)
```

**Label only some features** with rule-based labelling:

```python
from qgis.core import QgsRuleBasedLabeling
rule = QgsRuleBasedLabeling.Rule(settings)
rule.setFilterExpression("\"featurecla\" LIKE 'Admin-0 capital%'")
root = QgsRuleBasedLabeling.Rule(None)
root.appendChild(rule)
places.setLabeling(QgsRuleBasedLabeling(root))
places.setLabelsEnabled(True)
```

> If a font isn't installed, QGIS silently uses a fallback. Check with `QFontDatabase().families()` (from `qgis.PyQt.QtGui`) when exact typography matters, e.g. before exporting a print map.

## 9. QML files: save, load, reuse

```python
styles = OUTPUT / "styles"
styles.mkdir(parents=True, exist_ok=True)

message, ok = places.saveNamedStyle(str(styles / "places.qml"))
message, ok = other_layer.loadNamedStyle(str(styles / "places.qml"))
other_layer.triggerRepaint()
```

Both return a pair: a message and `True`/`False`. **Check `ok`.** A QML whose renderer uses a field the layer doesn't have still "loads", but then draws nothing, or draws everything as "Other".

**Read a QML.** Open one in a text editor. The settings you passed to `createSimple` are there as `<Option name="outline_width" value="0.15"/>`. Colours are stored as red, green, blue, alpha numbers: `#8fb0c7` appears as `value="143,176,199,255,..."`. This is how you find the right key names, and how you check that a style file (from the GUI, from another tool, or from AI) says what you think it says.

**One style for many layers:**

```python
for layer in project.mapLayers().values():
    if layer.name().endswith("_rivers"):
        layer.loadNamedStyle(str(styles / "rivers.qml"))
```

---

## Exercises

| File | Practises |
|---|---|
| `ex07_1_base_style.py` | a quiet base map: ocean, land, lakes, rivers; save four QMLs |
| `ex07_2_choropleth.py` | categorized by continent, then graduated GDP per person, with the −99 trap |
| `ex07_3_places.py` | rule-based places, proportional circles, capital labels with a halo |
| `ex07_4_terrain_style.py` | hypsometric DEM + multiply hillshade + labelled contours (uses Module 06 outputs) |

Each exercise loads its layers into the project, so look at the map after each run. If you're working headless or something looks off, open the saved QML in a text editor.

## Checkpoint

1. A fill symbol has a simple fill and a dashed outline. Which is `symbolLayer(0)`?
2. Your graduated legend starts at −120,000. What happened, and what's the fix?
3. Why `sqrt("pop_max")` for proportional circles?
4. `loadNamedStyle` returned `('', True)`, but the layer draws nothing. What's a likely cause?
5. Where do you find the key names for `createSimple({...})`?

<details><summary>Answers</summary>

1. The simple fill: index 0 is the bottom of the stack.
2. A "no data" code (−99) was treated as a real number. Turn it into NULL first (`CASE WHEN "gdp_md" > 0 ... END`) or filter it out.
3. So the circle's *area* scales with the value. Width-proportional circles exaggerate big values.
4. The style refers to a field (or category values) that this layer doesn't have.
5. Save a QML of a layer styled in the GUI, and read its `<Option name=... value=...>` lines.

</details>

## 🤖 With Claude

Style a layer by hand in the GUI, save it as QML, and give Claude the QML with: *"Write PyQGIS (QGIS 3.40, must also work in 4.x) that recreates this style from scratch, without loading the QML."* Run it on a fresh layer and compare the two maps side by side. What did it miss?

**Next:** [Module 08: Print layouts and export](../08-print-layouts/README.md)
