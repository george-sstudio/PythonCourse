# Python for QGIS in the Age of AI

A self-paced, offline course for George, built around two goals:

1. **Automate QGIS** with Python (PyQGIS): load and style layers, run Processing tools, build print layouts and export PDFs, and turn scripts into reusable tools.
2. **Direct AI well**: describe a GIS task so an AI assistant (like Claude) writes the right code, then read, check and fix what it gives you.

You don't need to memorise Python. AI can type code faster than any of us. What it can't do is see your data, know your CRS, or judge whether a map is right. This course teaches you enough Python to **read** code, **steer** it and **catch its mistakes**, plus the PyQGIS you need to make QGIS do repetitive work for you.

> **Reference book:** Bonny P. McClain, *Python for Geospatial Data Analysis* (O'Reilly, 2022). We keep its QGIS and PyQGIS chapters (updated for QGIS 3.40 and 4.x) and drop or shrink the rest. See [BOOK_MAP.md](BOOK_MAP.md) for what changed and why.

---

## What you need

| Thing | Notes |
|---|---|
| **QGIS 3.40 LTR** or newer | Everything is tested on **QGIS 3.40** and **QGIS 4.2**. Python comes with QGIS, so there's nothing else to install. |
| **This folder** on your computer | Best place: `D:\PythonCourse`. Get it with GitHub Desktop (*File → Clone repository*) or *Code → Download ZIP* on GitHub. |
| **No internet** | All the data is in [`data/`](data/). Once the folder is on your computer, everything works offline. |
| **Claude (optional, recommended)** | Used as a tutor in every module and as the main tool in Week 4. |

## Reading the course offline

- **`course.html`**: the whole course on one page. Double-click it to open it in any browser, no internet needed. Links to exercise files work as long as it stays in this folder.
- Or open the `README.md` files in any Markdown viewer (VS Code: `Ctrl+Shift+V`). On GitHub they render automatically.

## How to start

1. Open [modules/00-setup](modules/00-setup/README.md) and follow it (about 45 minutes).
2. Work through the modules in order. Each one has:
   - `README.md`: the lesson. Read it with QGIS open beside it.
   - `exercises/`: scripts with `TODO` gaps for you to fill in. Open them in the QGIS Python editor.
   - `solutions/`: finished versions. Try first, then compare.
   - **Checkpoint** questions at the end, with hidden answers.
3. Your results go into `output/`, which Git ignores, so you can't break the course files.

## Schedule (intensive: about 4 weeks, 10–12 hours a week)

| Week | Module | You will be able to… | Time |
|---|---|---|---|
| **1. Python you'll read every day** | [00 Setup and how to learn with AI](modules/00-setup/README.md) | run scripts in QGIS and use Claude as a tutor, not a crutch | 1 h |
| | [01 Values, lists and dictionaries](modules/01-python-basics-1/README.md) | read and write the building blocks of every script | 3 h |
| | [02 Decisions, loops, functions and errors](modules/02-python-basics-2/README.md) | follow what a script does step by step, and read error messages | 4 h |
| | [03 Objects and the PyQGIS docs](modules/03-objects-and-docs/README.md) | find out what any QGIS object can do, without guessing | 3 h |
| **2. PyQGIS core** | [04 Layers, projects and CRS](modules/04-layers-and-crs/README.md) | load, organise and save data and projects, with the right CRS | 4 h |
| | [05 Features, fields and expressions](modules/05-features-and-fields/README.md) | query, measure, edit and export attribute data safely | 4 h |
| | [06 Processing tools from Python](modules/06-processing/README.md) | run and chain any Processing tool, in batches | 4 h |
| **3. Cartography by code** | [07 Styling, labels and QML](modules/07-styling-and-labels/README.md) | style and label layers by code, and save/load QML styles | 4 h |
| | [08 Print layouts and export](modules/08-print-layouts/README.md) | build A4 layouts and export PDF/PNG automatically, incl. atlases | 4 h |
| | [09 Reusable tools and QGIS 4](modules/09-reusable-tools/README.md) | turn scripts into Processing tools that work in QGIS 3 and 4 | 3 h |
| **4. Directing AI** | [10 Briefing the AI](modules/10-directing-ai/README.md) | write task briefs and give the AI exact context from your project | 3 h |
| | [11 Reviewing and debugging AI code](modules/11-reviewing-ai-code/README.md) | catch the common mistakes in AI-written PyQGIS before they cost you | 4 h |
| | [12 Capstone: a map sheet factory](modules/12-capstone/README.md) | brief, review and run a complete automated map production script | 5 h |

Going slower is fine. The order matters more than the speed.

## Reference pages (keep these open)

- [GLOSSARY.md](GLOSSARY.md): every technical word in the course, in plain language.
- [CHEATSHEET.md](CHEATSHEET.md): the PyQGIS snippets you'll use most, in versions that work on QGIS 3.40 **and** 4.x.
- [AI_PLAYBOOK.md](AI_PLAYBOOK.md): brief templates, the code-review checklist and the red-flag list from Weeks 3–4.
- [data/README.md](data/README.md): what's in each dataset, and where it comes from.

## Why this course looks the way it does (the "AI era" adjustments)

| Less of this | More of this |
|---|---|
| Memorising syntax and typing long scripts | **Reading** code line by line and predicting what it will do |
| Writing everything from scratch | Starting from the QGIS **History panel**, docs and AI drafts, then adapting them |
| Clever programming tricks | Plain, checkable code, with prints and checks that prove it worked |
| Trusting that code that runs is correct | **Verifying**: counts, CRS, units, a visual check, a test on a copy |
| One-off console commands | Saved scripts, Processing tools and QML/QPT files you can rerun and version |

The skills that matter more now are judgment about data and CRS, describing a task precisely, and checking results. Those run through every module.

## Tools you'll keep using after the course

| Tool | What it does |
|---|---|
| [`tools/describe_project.py`](tools/describe_project.py) | Makes a "context card" of your open project (layers, CRS, fields, layouts) to paste into an AI chat. Module 10. |
| [`tools/check_code.py`](tools/check_code.py) | Scans a script for QGIS 4 problems and AI red flags. Modules 09 and 11. |
| [`modules/09-reusable-tools/solutions/safe_buffer_tool.py`](modules/09-reusable-tools/solutions/safe_buffer_tool.py) | A Processing tool that buffers in metres, whatever the layer's CRS. |
| [`modules/12-capstone/solutions/map_factory.py`](modules/12-capstone/solutions/map_factory.py) | The reference map sheet factory: a starting point for your own series. |

## Maintaining the course

Every solution, the capstone's acceptance checks and every cheat-sheet snippet are tested automatically, outside the QGIS window, on **QGIS 3.40.3 and QGIS 4.2.3** (`tools/run_all_tests.sh`, which uses `tools/qgis_runner.py`). `tools/build_html.py` rebuilds `course.html` (needs pandoc). You don't need any of this to take the course.
