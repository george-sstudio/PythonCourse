# Module 00: Setup, and how to learn with AI

**Time:** about 45 minutes · **Week 1**

## You will

- get the course onto your computer and connect it to QGIS (once)
- learn the two places you'll type Python in QGIS: the **console** and the **editor**
- run your first script
- set Claude up as a *tutor*: something that helps you understand, not something that does the work for you

## Key words

| Word | Meaning |
|---|---|
| **Python** | A programming language: a precise way of writing instructions for the computer. |
| **PyQGIS** | The part of QGIS you control with Python. Almost everything you can click in QGIS can also be done with PyQGIS. |
| **Script** | A text file of Python instructions, ending in `.py`. It runs from top to bottom. |
| **Console** | A box where you type **one** line of Python, press Enter and see the result at once. Good for trying things out. |
| **Editor** | A notepad inside QGIS for writing and running **whole scripts**. Good for anything you want to keep. |
| **Run** | Tell Python to carry out the instructions. |
| **Global variable** (QGIS) | A named value QGIS remembers across all projects. We store the course folder in one, called `course_root`. |

---

## 1. Put the course on your computer

Pick **one** of these:

- **GitHub Desktop (recommended).** *File → Clone repository → PythonCourse → Local path `D:\`*. You get `D:\PythonCourse`. In Module 11 you'll use GitHub Desktop to take "snapshots" before letting AI change your files.
- **ZIP.** On the GitHub page: *Code → Download ZIP*. Unzip it to `D:\PythonCourse`.

After that, no internet is needed.

## 2. Meet the console and the editor

1. Open QGIS 3.40.
2. Open the console: **Plugins → Python Console** (or `Ctrl+Alt+P`). A panel appears with a `>>>` prompt.
3. Type each line below and press **Enter**. Watch what comes back.

```python
print("Hello from QGIS")
2 + 3
Qgis.version()
```

- `print(...)` shows whatever you put in the brackets.
- `2 + 3` shows `5`. In the console, a bare value is shown automatically.
- `Qgis.version()` asks QGIS for its version number. You just used PyQGIS for the first time.

4. Now click **Show Editor** (the notepad icon at the top of the console). A second panel opens on the right. This is where scripts live.

| Console (left) | Editor (right) |
|---|---|
| one line at a time | many lines, saved as a `.py` file |
| result appears immediately | click **Run Script** (green triangle) to run the whole file |
| forgotten when QGIS closes | kept on disk, so you can rerun and share it |

> **Habit:** experiment in the console, keep things in the editor.

## 3. Connect the course to QGIS (once)

1. In the editor click **Open Script…** and choose `D:\PythonCourse\modules\00-setup\setup_course.py`.
2. Click **Run Script**.
3. The console should print your course folder, `natural_earth.gpkg`, the output folder and your QGIS version, then `All set.`

If it says it can't find the data, follow the instruction it prints: type your folder path on the `COURSE_FOLDER = r""` line, save, and run again.

What just happened? The script saved your course folder in a QGIS **global variable** named `course_root`. You can see it in *Settings → Options → Variables*. Every exercise starts with these lines, which read it back:

```python
COURSE = Path(QgsExpressionContextUtils.globalScope().variable("course_root"))
DATA = COURSE / "data"
```

You don't need to understand them yet. By Module 03 you will.

## 4. Your first script

Open `exercises/ex00_first_script.py` in the editor, read it, run it, and do the TODO.

**Before you click Run, say out loud what you expect to happen.** This "predict, then run" habit is the fastest way to learn to read code, and reading code is the main skill this course builds.

> **Saving matters.** Press `Ctrl+S` before Run Script. If a script has unsaved changes, QGIS runs a temporary copy of it, and `__file__` (the script's own path) then points to that copy. Only `setup_course.py` cares about this, but saving first is a good habit anyway.

---

## 5. How to learn with AI (read this before Module 01)

AI makes learning to code much faster, as long as you use it as a **tutor** and not as a **ghostwriter**. If it writes all your exercises, you'll finish the course unable to judge its code, and judging its code is the whole point (Week 4).

### Tutor rules

| Do | Don't |
|---|---|
| "Explain this line to me as if I'm new to Python." | "Write the solution to this exercise." |
| "Give me a hint, not the answer." | Paste code you don't understand into your project. |
| "Here's what I think this does: … Am I right?" | Accept "it runs" as proof that it's right. |
| "Quiz me with 3 questions on this module." | Skip the error message and just say "it doesn't work". |
| Tell it your QGIS version (3.40) every time | Let it guess the version. Old QGIS 2 code is all over the internet. |

### A tutor prompt you can reuse

Save this as the instructions of a Claude **Project** called "Python course", or paste it at the start of a chat:

```text
You are my tutor for a Python-for-QGIS course. I know a little Python.
Explain in plain language and define technical words. I use QGIS 3.40 LTR
(PyQGIS, Python 3.12) and will later move to QGIS 4.x, so prefer code that
works in both (scoped enums like Qgis.GeometryType.Polygon, imports from
qgis.PyQt). When I'm doing an exercise, give hints and ask me questions
before giving answers. When I paste code, explain it line by line. When I
paste an error, help me read the error message myself first.
```

### Three ways to ask

1. **Explain**: paste a few lines and ask "what does each line do?"
2. **Check**: write your own explanation or answer, then ask "is this right? what did I miss?"
3. **Stretch**: after an exercise, ask "give me a harder variation of this exercise."

Each module ends with a **🤖 With Claude** box that suggests one of these.

---

## Checkpoint

1. You want to try out `layer.featureCount()` quickly. Console or editor?
2. You've written 20 lines that export a map. Where should they live, and why?
3. What does `course_root` store, and where can you see it in QGIS?
4. Why tell an AI "QGIS 3.40" every time?

<details><summary>Answers</summary>

1. The console. It's a one-line experiment.
2. In the editor, saved as a `.py` file, so you can rerun it, fix it and keep it.
3. The path of the course folder. *Settings → Options → Variables*.
4. PyQGIS has changed across versions (2.x, 3.x, 4.x). Without the version, AI often mixes old and new code, and old code fails or behaves differently.

</details>

## 🤖 With Claude

Set up the tutor prompt above. Then paste `ex00_first_script.py` and ask: *"Explain this script line by line. Then ask me two questions to check I understood."*

**Next:** [Module 01: Values, lists and dictionaries](../01-python-basics-1/README.md)
