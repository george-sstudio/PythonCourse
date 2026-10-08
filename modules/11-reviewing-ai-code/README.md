# Module 11: Reviewing and debugging AI code

**Time:** about 4 hours · **Week 4**

AI-written code fails in two ways. The **loud** way is a traceback, which is annoying but honest. The **silent** way is code that runs, prints "Done!" and is wrong. Silent failures are the dangerous ones, and they're the main subject of this module. You'll review six realistic AI answers, each written to look plausible, and each containing the mistakes this course has been warning you about.

## You will

- review code **before** running it, with a 10-point checklist
- recognise silent failures: wrong units, unsaved edits, swallowed errors, ignored return codes
- catch invented methods and tool ids in seconds
- debug calmly: reproduce → read → inspect → shrink → hypothesise → fix → recheck
- protect your work: copies, Git snapshots, saving before you run

## Key words

| Word | Meaning |
|---|---|
| **Code review** | Reading code critically *before* trusting it, looking for problems rather than confirming it works. |
| **Silent failure** | Code that finishes without an error but produces a wrong or missing result. |
| **Hallucinated API** | A method, parameter or tool id the AI invented because it *sounds* right. |
| **Side effect** | Something code changes besides its output, e.g. leaving a filter on a layer, or overwriting a file. |
| **Minimal reproduction** | The smallest piece of code (and data) that still shows the problem. |
| **Regression** | A fix that breaks something that used to work. Rerun **all** checks after a fix. |
| **Commit / snapshot** | A saved version of your files in Git, so you can always go back. |

---

## 1. The review checklist

Full version: [AI_PLAYBOOK.md §4](../../AI_PLAYBOOK.md#4-review-checklist-before-you-run-ai-code). In short:

1. **Do I understand every line?**
2. **Right QGIS version?** Run `tools/check_code.py`.
3. **Do the names exist?** Layers, fields (context card), methods (`dir()`, `help()`).
4. **CRS and units?** Every distance, buffer, area and length.
5. **Is my data safe?** What does it write, overwrite or edit?
6. **Silent failures?** `isValid()`, return codes, `except: pass`, empty filters.
7. **Missing values?** NULL, `-99`, `0`.
8. **Edge cases?** Apostrophes, multipart, high latitudes, ±180°.
9. **Is the result checked?** Asserts, opening the output, looking at it.
10. **Anything extra?** Code you didn't ask for is code you have to trust.

**Read top to bottom once without judging**, just to get the shape: inputs → steps → outputs. Then go through the checklist. Most real problems are caught by points 3–6.

### Comments in AI code are claims, not facts

```python
# 5 km is about 0.045 degrees (1 degree = 111 km)
zone = processing.run("native:buffer", {"INPUT": volga, "DISTANCE": 0.045, ...})
```

The comment makes the code *look* reasoned. It's only true north–south. At the Volga's latitude, 0.045° east–west is about 3 km. Review 1 shows the result: one city missing, and an area that's 37% off.

## 2. Silent failures: the six you'll meet most

| Pattern | What you see | What actually happened |
|---|---|---|
| Units | a plausible number | measured in degrees |
| `startEditing()` without commit | "Density added!" | nothing saved |
| `except: pass` | no errors | errors happened, and were hidden |
| Ignored return code | "Exported!" | no file (or a broken one) |
| Invalid filter expression | an empty loop | a country silently skipped |
| Overwrite in a loop | one file | only the last iteration survived |

**The cure is the same for all of them: check the *output*, not the *messages*.** Open the file again and count. Compare with something you know. Look at the map.

## 3. Hallucinated methods and tool ids

When a name looks unfamiliar, it takes ten seconds to check:

```python
[m for m in dir(layer) if "count" in m.lower()]          # is getFeatureCount real?
help(layer.featureCount)                                  # what does it take?
[a.id() for a in QgsApplication.processingRegistry().algorithms() if "count" in a.id()]
processing.algorithmHelp("native:countpointsinpolygon")   # real parameters
```

Invented names usually fail **loudly** (`AttributeError`, `Algorithm not found`), so they're the *easier* kind of bug. Fix them by checking, not by asking the AI to "try again", because a second guess can be wrong too.

A useful prompt when you suspect invention: *"Which QGIS 3.40 class and method is this exactly? Give me the name so I can check it with help()."*

## 4. Debugging: a calm routine

```text
1. REPRODUCE   fresh project, run again - same failure?
2. READ        traceback bottom-up: type, message, line
3. INSPECT     print what's going into the failing line:
               type(x), layer.isValid(), featureCount(), crs().authid(), field names
4. SHRINK      make it fail in 5 lines on 1 feature
5. HYPOTHESISE "I think X because Y" - then test exactly that
6. FIX         the cause, not the symptom (never wrap it in try/except to hide it)
7. RECHECK     run ALL checks again (regressions!)
```

When you bring in the AI, send everything at once: code, full traceback, what you expected, what you checked, your guess, context card. Template: [AI_PLAYBOOK.md §6](../../AI_PLAYBOOK.md#6-debugging-with-ai).

### When QGIS itself crashes

Rarely, PyQGIS code makes QGIS close with no traceback at all. Usually that's from using an object after QGIS has deleted it. While building this course, a long chain like `layer.labeling().rootRule().children()[0].settings().format()` crashed QGIS 3.40 headless. The fix was to keep each step in its own variable. Protect yourself:

- **save the project before running new code**
- prefer short steps with named variables over long chains on temporary objects
- if it crashes, rerun line by line in the console to find the line

## 5. Safety habits

- **Work on copies:** `materialize()`, a copied GeoPackage, or a new output file.
- **New output folder per run:** `output/2026-10-08_volga/`.
- **Git snapshots:** in GitHub Desktop, *Commit* before asking AI to change a script. If the change is bad, *Discard* or revert. That's your undo button across days, not just across Ctrl+Z.
- **Test where bugs would show:** high latitude, apostrophes, NULLs, empty results (Module 06's lesson).
- **Independent checks:** compare with a number you got another way (buffer area ≈ 2 × d × L; a known count).

## 6. A second opinion: the two-chat review

For code that matters, paste the brief and the code into a **fresh** chat and ask for problems only. The prompt is in [AI_PLAYBOOK.md §7](../../AI_PLAYBOOK.md#7-two-chat-review-writer--reviewer). The reviewer hasn't seen the reasoning that produced the code, so it judges the result on its own terms. Treat its findings like `check_code.py`'s: as questions to verify, not orders.

---

## Exercises: six AI answers to review

Each file has **the request**, **the AI's answer**, and **checks** that define the correct result. Review *before* running, writing each problem as `# PROBLEM: ...`, then run, then fix until the checks pass. The solutions list every problem with its checklist number.

| File | Looks like | Problems to find | Main lessons |
|---|---|---|---|
| `review_1_volga.py` | a clean Processing chain | 2 (+1 note) | degrees as distance; fake km² conversion; comments as claims |
| `review_2_density.py` | a careful edit with try/except | 4 | unsaved edits; `except: pass`; square degrees; QGIS 4 types |
| `review_3_lookup.py` | a neat table | 3 | apostrophe trap; `iso_a3 = -99`; NULL vs `None` (version-dependent!) |
| `review_4_export.py` | a tidy export loop | 4 | `"\n"` in a path; overwrite in a loop; ignored return code; side effect |
| `review_5_layout.py` | a standard layout script | 4 | extent in the wrong CRS; call order; `#RRGGBBAA`; unchecked export |
| `review_6_invented.py` | confident code that crashes | 5 | invented methods, field and tool id; checking with `dir`/`help`/registry |

Suggested order: 6 (loud), then 1–5 (silent). Before each one, run `tools/check_code.py` on it and note **which problems it catches and which it misses**. That tells you how far automated checks go, and where your judgment starts.

> **Review 3 is special:** one of its bugs gives a wrong answer in QGIS 3.40 and the *right* answer in QGIS 4. Code can be "correct" or "wrong" depending on the version, which is another reason to state your version in every brief.

## Checkpoint

1. Which is more dangerous: an `AttributeError` or a script that prints "Done!" with the wrong result? Why?
2. A script uses `layer.startEditing()` and `changeAttributeValue()`, but no `commitChanges()`. What's in the file afterwards?
3. Name two ways to check whether a method the AI used actually exists.
4. After fixing a bug, why rerun *all* the checks?
5. What should you do before running AI code that edits files?

<details><summary>Answers</summary>

1. The silent one. An error stops you, while a wrong result gets used.
2. No changes: the edits were never committed.
3. `dir(obj)` (filtered), `help(obj.method)`, the PyQGIS docs, or (for tools) the processing registry or `processing.algorithmHelp()`.
4. Fixes can break something else (regressions).
5. Make sure it works on copies and writes to a new output folder, save the project, and commit a Git snapshot.

</details>

## 🤖 With Claude

Take your answer from Module 04's "🤖 With Claude" box (the 5 km buffer around rivers in Norway). Review it now with the checklist and `check_code.py`. Then run the two-chat review on it. Did the second chat catch what you caught?

**Next:** [Module 12: Capstone: a map sheet factory](../12-capstone/README.md)
