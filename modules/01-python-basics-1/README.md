# Module 01: Values, lists and dictionaries

**Time:** about 3 hours · **Week 1** · Use the QGIS **console** to try every example.

## You will

- know the five kinds of value you'll see in every script
- store values in **variables** and build sentences with **f-strings**
- write file paths that work on Windows
- keep many values in a **list**, and labelled values in a **dictionary**, which is exactly how QGIS hands you a feature's attributes

## Key words

| Word | Meaning |
|---|---|
| **Value** | A piece of data: `42`, `"Paris"`, `3.5`, `True`. |
| **Type** | The kind of value: text, whole number, decimal number, yes/no… Python treats each type differently. |
| **Variable** | A name that points to a value, like a label on a box. `city = "Paris"` puts `"Paris"` in a box labelled `city`. |
| **String** (`str`) | Text, written inside quotes: `"Lima"` or `'Lima'`. |
| **Integer** (`int`) | A whole number: `7`, `-427`. |
| **Float** (`float`) | A decimal number: `31.77`, `0.5`. |
| **Boolean** (`bool`) | `True` or `False`. Capital letter, no quotes. |
| **None** | "Nothing here." Python's empty value. QGIS uses it for empty (NULL) fields. |
| **List** | An ordered collection: `["Lima", "Quito", "Bogotá"]`. |
| **Dictionary** (`dict`) | A collection of *labelled* values: `{"name": "Lima", "pop": 9_000_000}`. The labels are **keys**. |
| **Index** | A position in a list. **Counting starts at 0.** |
| **Method** | An action a value can do, written with a dot: `"lima".upper()`. |

---

## 1. Values and their types

Type each line in the console:

```python
"Jerusalem"          # str: text
1294                 # int: whole number
31.77                # float: decimal number
True                 # bool: yes/no
None                 # nothing

type(31.77)          # asks: what type is this?  →  <class 'float'>
```

Why care about types? Because `"7" + "3"` is `"73"` (text glued together), while `7 + 3` is `10`. Fields in your layers have types too, and many bugs (yours and AI's) come from a number stored as text.

```python
int("7") + int("3")  # convert text to whole numbers → 10
str(1294) + " m"     # convert a number to text → '1294 m'
float("31.77")       # → 31.77
```

## 2. Variables

```python
city = "Lima"
population = 9_000_000      # the _ is only for readability; Python ignores it
lat = -12.05
is_capital = True
```

- `=` means **store**, not "equals". Read `city = "Lima"` as "*city* now holds `"Lima"`".
- Names: lower case, words joined by `_` (`max_elevation`, not `MaxElevation`). They can't start with a digit, and they can't contain spaces.
- Python is **case-sensitive**: `City` and `city` are different names. Typing `City` when you meant `city` gives a `NameError`. You'll see a lot of these.

You can change what a variable holds:

```python
population = population + 250_000   # take the old value, add, store the result
population += 250_000               # shorter way to write the same thing
```

## 3. Numbers

```python
10 / 4      # 2.5   ordinary division always gives a float
10 // 4     # 2     whole-number division (drops the remainder)
10 % 4      # 2     the remainder
2 ** 10     # 1024  power
round(2.6789, 1)   # 2.7
```

GIS example: a scale of 1:85,000 means 1 cm on paper is 85,000 cm on the ground.

```python
scale = 85_000
cm_on_paper = 4.2
km_on_ground = cm_on_paper * scale / 100_000   # 100,000 cm in a km
print(km_on_ground)                            # 3.57
```

## 4. Strings (text)

```python
name = "dead sea"
name.upper()             # 'DEAD SEA'
name.title()             # 'Dead Sea'
name.replace("sea", "Sea")
len(name)                # 8 characters
"sea" in name            # True
```

### f-strings: putting values into text

Put an `f` before the quotes and the variables inside `{ }`:

```python
city = "Lima"
pop = 9_751_717
print(f"{city} has {pop} people")             # Lima has 9751717 people
print(f"{city} has {pop:,} people")           # Lima has 9,751,717 people
print(f"{city}: {pop / 1_000_000:.1f} million")  # Lima: 9.8 million
```

- `:,` adds thousands separators.
- `:.1f` means "decimal number with 1 digit after the point".

You'll use f-strings constantly: for messages, file names (`f"map_{country}.pdf"`) and labels.

### File paths on Windows

A Windows path has backslashes `\`, and in Python strings a backslash is a special character (`\n` means "new line"). Two safe ways to write a path:

```python
folder = r"D:\PythonCourse\data"         # r"..." = raw string: backslashes are just backslashes

from pathlib import Path
folder = Path(r"D:\PythonCourse") / "data"   # Path objects join with /  (best)
gpkg = folder / "natural_earth.gpkg"
gpkg.exists()      # True or False
gpkg.name          # 'natural_earth.gpkg'
gpkg.suffix        # '.gpkg'
```

> **AI watch:** AI often writes `"D:\new_maps\test.gpkg"`. Here `\n` turns into a line break and `\t` into a tab, so the path breaks without any warning. Look for `r"..."` or `Path(...)`.

## 5. Lists: many values in order

```python
capitals = ["Lima", "Quito", "Bogotá", "Caracas"]

capitals[0]        # 'Lima'      the first item is at index 0
capitals[-1]       # 'Caracas'   negative counts from the end
capitals[1:3]      # ['Quito', 'Bogotá']   a "slice": from index 1 up to (not incl.) 3
len(capitals)      # 4

capitals.append("La Paz")       # add to the end
"Quito" in capitals             # True
sorted(capitals)                # a new, alphabetically sorted list

elevations = [154, 2850, 2640, 900]
max(elevations), min(elevations), sum(elevations)
```

> **Index 0 trips everyone up, AI included.** "The first band of a raster" is band `1` in QGIS (they count from 1), but the first item of a Python list is `[0]`. When counting matters, check which convention is in use.

## 6. Dictionaries: labelled values

A dictionary is like one row of an attribute table: each value has a label (the **key**).

```python
place = {
    "name": "Lima",
    "country": "Peru",
    "pop_max": 9_751_717,
    "is_capital": True,
}

place["name"]               # 'Lima'
place["pop_max"] / 1e6      # 9.75  (1e6 is a short way to write 1,000,000)
place["elevation"] = 154    # add a new key
place.get("area")           # None: .get() doesn't crash if the key is missing
place.get("area", 0)        # 0: you can choose the fallback
place["area"]               # KeyError! square brackets do crash on missing keys

place.keys()                # all the labels
place.items()               # all (label, value) pairs
```

### A list of dictionaries = a table

```python
cities = [
    {"name": "Lima",   "pop": 9_751_717},
    {"name": "Quito",  "pop": 2_011_388},
    {"name": "Bogotá", "pop": 7_772_000},
]
cities[1]["name"]     # 'Quito'   (row 1, column "name")
```

Keep this picture in mind: in Module 05, QGIS hands you features whose attributes you read with `feature["name"]`, the same square brackets.

## 7. Reading code (the skill that matters most)

When you meet unfamiliar code, read it in this order:

1. **Names**: what is each variable *for*? Good names tell you.
2. **Right side of `=` first**: work out the value, then see where it's stored.
3. **Predict**: write down what will be printed *before* you run it.
4. **Run and compare**: if you were wrong, find the exact line where your idea went wrong.

Try it: what does this print? Decide first, then run it.

```python
a = [10, 20, 30]
b = a[1] + a[-1]
a.append(b)
print(len(a), a[3])
```

<details><summary>Answer</summary>

`4 50`. `b` is `20 + 30 = 50`, it's appended, so `a` has 4 items and the item at index 3 is `50`.

</details>

---

## Exercises

Open each file in the editor, fill in the `TODO`s, and run it. The bottom of each file has **checks**: lines starting with `assert` that stay silent when your answer is right and show a red `AssertionError` with a hint when it isn't. (Module 02 explains `assert`. For now: silence plus "All checks passed" means success.)

| File | Practises |
|---|---|
| `ex01_1_values.py` | variables, numbers, f-strings, paths |
| `ex01_2_lists.py` | indexing, slicing, `append`, `sorted`, `max` |
| `ex01_3_dicts.py` | dictionaries and a small table |

## Checkpoint

1. What's the difference between `"1294"` and `1294`?
2. `elev = [5, 12, 40]`. What is `elev[2]`? What is `elev[3]`?
3. Write an f-string that prints `Area: 1,234.6 km²` from `area = 1234.5678`.
4. Why is `"D:\new\data.gpkg"` dangerous?
5. `row = {"name": "Nile"}`. What's the difference between `row["length"]` and `row.get("length")`?

<details><summary>Answers</summary>

1. The first is text (`str`), the second a whole number (`int`). You can do maths with the second, not the first.
2. `40`. `elev[3]` is an `IndexError`: there are only indexes 0, 1 and 2.
3. `f"Area: {area:,.1f} km²"`
4. `\n` becomes a line break, so the path silently breaks. Use `r"D:\new\data.gpkg"` or `Path(...)`.
5. `row["length"]` crashes with `KeyError`. `row.get("length")` returns `None`.

</details>

## 🤖 With Claude

Ask: *"Give me 5 'predict the output' puzzles using lists and dictionaries of cities, one at a time. Don't tell me the answer until I reply."*

**Next:** [Module 02: Decisions, loops, functions and errors](../02-python-basics-2/README.md)
