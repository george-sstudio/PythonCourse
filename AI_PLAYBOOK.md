# AI Playbook for PyQGIS

Everything from Weeks 3–4 on one page: how to **brief** an AI, the **house rules** to give it once, how to **review** what it writes, and how to **debug** with it.

---

## 1. The loop

```text
 BRIEF ──► PLAN (in words) ──► CODE (small steps) ──► RUN on a copy ──► VERIFY ──► keep / fix
   ▲                                                                          │
   └──────────── after 2 failed fixes: new chat, better brief ◄───────────────┘
```

1. **Brief**: goal, context card, inputs, outputs, rules, checks (template below).
2. **Plan first**: "Before writing code, describe your plan in numbered steps and list any assumptions." Fix the plan, which is cheaper than fixing code.
3. **Code in small steps**: ask for one function or one step at a time, each ending with a check.
4. **Run on a copy**: copied data, a new output folder, the project saved first.
5. **Verify**: run the checks, open the output, *look* at the map.
6. **If it's wrong twice**, start a fresh chat with a better brief that includes what you learned. A long chat full of failed attempts makes things worse, not better.

---

## 2. The brief template

Copy this, fill it in, and paste it as one message.

```text
## Goal
<one or two sentences: what should exist when this works>

## Context
<paste the context card from tools/describe_project.py>
- I run code in the QGIS Python editor (Windows, paths like D:\...).

## Inputs
- <layer / file names exactly as in the context card>

## Output
- <file type, path, layer name, CRS, fields>
- <for maps: page size, scale, what goes on the page>

## Rules
- <e.g. never modify files in D:\PythonCourse\data; write only to D:\PythonCourse\output>
- <e.g. distances in metres; keep all source fields>

## Checks (how we'll know it worked)
- <e.g. 13 PDFs are created; every buffer polygon is in EPSG:4326; Lena → Lensk, Yakutsk, Zhigansk>

## How I want the answer
- First a plan in numbered steps, with assumptions. Wait for my OK.
- Then code in small functions, each with a docstring.
- End the script with assert checks for the Checks above.
```

**Good checks are specific and come from you:** counts you know, a feature you can name, a value you can look up, a case that would expose a bug (high latitude, an apostrophe, a NULL, an empty result).

---

## 3. House rules (give these once)

Save this as the instructions of a Claude **Project** (e.g. "PyQGIS work"), or keep it in a file and paste it at the top of a chat.

```text
PyQGIS house rules
- QGIS 3.40 LTR (Python 3.12) on Windows; code must also run in QGIS 4.x:
  import Qt from qgis.PyQt (never PyQt5); scoped enums (Qgis.GeometryType.Polygon,
  Qt.AlignmentFlag.AlignLeft, Qgis.LayoutUnit.Millimeters); field types with
  QMetaType.Type.*; NULL checks with QgsVariantUtils.isNull().
- Scripts run in the QGIS Python editor. Explicit imports at the top.
- Paths with pathlib.Path or r"..." strings.
- Check every layer with isValid() right after loading; raise a clear error if not.
- Never modify source data. Work on copies (materialize() or a new file);
  write outputs only to the output folder I name.
- Edits only inside "with edit(layer):".
- Distances, buffers and areas in metres in a projected CRS (or QgsDistanceArea),
  never in degrees. State which CRS you use and why.
- Build expressions with QgsExpression.quotedValue() for values from data.
- Never use bare "except:" or "except Exception: pass".
- Check return values (export results, writer errors) and raise if they fail.
- Prefer Processing tools (processing.run) over hand-written geometry loops.
- Use only methods that exist in QGIS 3.40; if unsure, say so.
- End scripts with assert checks and print a short summary of what was made.
- Keep it simple: no features I didn't ask for.
```

---

## 4. Review checklist (before you run AI code)

Go top to bottom. Most problems are caught by the first five.

| # | Ask | How to check |
|---|---|---|
| 1 | **Do I understand every line?** | If not, ask "explain lines 20–35". Don't run what you can't read. |
| 2 | **Is it for my QGIS version?** | Run `tools/check_code.py`. Watch for QGIS 2 names (`QgsMapLayerRegistry`, `processing.runalg`). |
| 3 | **Do the names exist?** | Compare layer and field names with your context card. Check unfamiliar methods with `dir()`/`help()`. |
| 4 | **CRS and units?** | Any distance, buffer, area or length: in what CRS? In metres? |
| 5 | **Is my data safe?** | Where does it write? Does it overwrite? Does it edit the source? Is the output folder right? |
| 6 | **Silent failures?** | `isValid()` checked? Export results checked? Any `except: pass`? What happens if a filter finds 0 features? |
| 7 | **Missing values?** | NULLs, `-99`/`0` "unknown" codes, empty geometries. |
| 8 | **Edge cases?** | Apostrophes in names, multipart features, features crossing ±180°, very large or tiny countries. |
| 9 | **Is the result checked?** | Asserts on counts/CRS/values; opens the output; you look at the map. |
| 10 | **Anything extra?** | Features you didn't ask for are extra code to trust. Ask for them to be removed. |

---

## 5. Red flags (seen in this course)

| Red flag | Why it's wrong | Fix | Module |
|---|---|---|---|
| Buffer/area/length on EPSG:4326 data | Degrees aren't distances | Reproject, `QgsDistanceArea`, or the safe buffer tool | 04, 06, 09 |
| `"D:\new\file.gpkg"` | `\n` becomes a line break | `r"..."` or `Path(...)` | 01 |
| `x=lat, y=lon` | The swap moves every point | x = longitude, y = latitude | 04 |
| `f"\"name\" = '{name}'"` | Breaks on *Côte d'Ivoire* | `QgsExpression.quotedValue(name)` | 05 |
| `if value is None` on attributes | QGIS 3 NULL isn't `None` | `QgsVariantUtils.isNull(value)` | 05 |
| `-99` used as a number | "Unknown" turned into data | `CASE WHEN "x" > 0 THEN ... END` / filter | 05, 07 |
| `iso_a3` as the country key | `-99` for France, Norway… | `adm0_a3` | data README |
| `startEditing()` without commit | Nothing is saved | `with edit(layer):` | 05 |
| Editing the source file "to test" | No way back | Work on a copy | 05 |
| `except: pass` | Errors disappear | Remove it; let it fail loudly | 02 |
| Result of `exportToPdf` ignored | "Success" with no file | Compare with `ExportResult.Success` | 08 |
| Slope/hillshade on a degree DEM | Metres over degrees = 90° | Reproject the DEM first | 06 |
| `#RRGGBBAA` colours | QGIS reads `#AARRGGBB` | `"R,G,B,A"` or `QColor.setAlpha()` | 07 |
| World polygon in a local CRS | Ocean tears into strips | Map background colour as sea | 08 |
| Template loaded in another project | Map items lose their layers | Reconnect layers and legend | 08 |
| `PyQt5`, `QVariant.Double`, `Qt.AlignLeft` | Breaks in QGIS 4 | See Module 09's table | 09 |
| A method you can't find in `dir()` | Probably invented | Ask for the doc link; check `help()` | 03, 11 |

---

## 6. Debugging with AI

Before asking:

1. **Reproduce it.** Run again from a fresh project. Does it fail every time?
2. **Read the traceback bottom-up**: error type, message, line.
3. **Look at the values** just before the failing line: `print(type(x), x)`, `layer.isValid()`, `layer.featureCount()`, `layer.crs().authid()`.
4. **Shrink it**: can you make it fail in 5 lines, on one feature?

Then send **all of this** in one message:

```text
This code (below) fails. QGIS 3.40.
What I expected: ...
What happened: <the FULL traceback, or the wrong output>
What I checked: <prints and their results>
My guess: ...
Context card: <paste>
Please explain the cause first, then the smallest fix. Don't hide the error
with try/except.
```

After the fix: rerun **all** the checks, not just the one that failed.

---

## 7. Two-chat review (writer / reviewer)

For anything that matters, open a **second, fresh chat** and paste the brief plus the code:

```text
Review this PyQGIS script against the brief. List only problems that would
make the result wrong or unsafe (wrong CRS/units, data loss, silent failures,
missing requirements, non-existent API calls). For each: line, problem, fix.
No style comments.
```

A fresh chat hasn't "fallen in love" with the code, so it reviews more honestly. Treat its list as questions, like `check_code.py`'s findings.

---

## 8. Safety habits

- **Save the project before running new code.** Some PyQGIS mistakes crash QGIS itself (no traceback, it just closes).
- **Snapshot with Git** (GitHub Desktop → *Commit*) before letting AI change your scripts, so you can always go back.
- **Write to a new output folder** per run, e.g. `output/2026-10-08_sheets/`.
- **Never paste private data** you wouldn't email. The context card can hide sample values (`SAMPLES = 0`).
