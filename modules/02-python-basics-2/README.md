# Module 02: Decisions, loops, functions and errors

**Time:** about 4 hours · **Week 1**

## You will

- make a script choose between actions (`if`)
- repeat an action for every item (`for`). This is the heart of automation: "for every layer…", "for every country…"
- package steps into **functions** you can reuse
- read a CSV file with Python
- **read error messages** calmly and fix them. You'll do this every day, with or without AI

## Key words

| Word | Meaning |
|---|---|
| **Condition** | A question whose answer is `True` or `False`, e.g. `pop > 1_000_000`. |
| **Block** | The indented lines under an `if`, `for`, `def` or `with`. **Indentation (4 spaces) is how Python knows which lines belong together.** |
| **Loop** | Repeating a block once for each item in a collection. |
| **Function** | A named, reusable block. You *define* it once with `def`, then *call* it as often as you like. |
| **Parameter / argument** | The input a function expects (parameter) and the value you actually pass in (argument). |
| **Return value** | What a function hands back. Different from `print`, which only shows something on screen. |
| **Module / import** | A file of ready-made Python code. `import csv` lets you use Python's CSV tools. |
| **Tuple** | Like a list, but in round brackets and unchangeable: `(31.77, 35.21)`. |
| **Exception** | Python's name for an error that stops the script. |
| **Traceback** | The error report Python prints. **Read it from the bottom up.** |

---

## 1. Decisions: `if`, `elif`, `else`

```python
elevation = 820

if elevation < 0:
    print("below sea level")
elif elevation < 500:
    print("lowland")
elif elevation < 1000:
    print("hills")
else:
    print("mountains")
```

- Python checks the conditions **top to bottom** and runs the **first** block that's `True`, then skips the rest.
- The colon `:` and the indentation are both required.

Comparisons: `==` (equal; **two** `=` signs), `!=` (not equal), `<`, `<=`, `>`, `>=`.
Combine them with `and`, `or`, `not`:

```python
pop = 2_000_000
is_capital = True
if is_capital and pop > 1_000_000:
    print("big capital")
```

> `=` stores, `==` compares. Mixing them up is one of the most common beginner errors.

## 2. Loops: `for`

```python
capitals = ["Lima", "Quito", "Bogotá"]
for name in capitals:
    print("Making map for", name)
print("done")          # not indented, so this runs once, after the loop
```

Read it as: "for each item in `capitals`, call it `name`, then run the indented block."

### Patterns you'll see again and again

```python
populations = [9_751_717, 2_011_388, 7_772_000]

# 1. Accumulate a total
total = 0
for p in populations:
    total += p

# 2. Count things that match
big = 0
for p in populations:
    if p > 5_000_000:
        big += 1

# 3. Build a new list
in_millions = []
for p in populations:
    in_millions.append(round(p / 1e6, 1))

# 4. Keep track of the best so far
largest = None
for p in populations:
    if largest is None or p > largest:
        largest = p
```

More loop tools:

```python
for i in range(3):              # 0, 1, 2
    print(i)

for i, name in enumerate(capitals):   # gives position AND item
    print(i, name)                     # 0 Lima, 1 Quito, …

place = {"name": "Lima", "pop": 9_751_717}
for key, value in place.items():       # loop through a dictionary
    print(key, "=", value)
```

### Reading a "list comprehension"

AI loves this compact one-line loop. You don't have to write them, but you should be able to read one:

```python
in_millions = [round(p / 1e6, 1) for p in populations if p > 1_000_000]
```

Read it as "make a list of `round(p/1e6, 1)` for each `p` in `populations`, keeping only those where `p > 1_000_000`." It does the same as pattern 3 above, with a filter.

## 3. Functions

```python
def pop_label(pop):
    """Turn 9751717 into '9.8 M'."""
    millions = pop / 1_000_000
    return f"{millions:.1f} M"

print(pop_label(9_751_717))     # 9.8 M
print(pop_label(2_011_388))     # 2.0 M
```

- `def` defines a function. `pop` is its **parameter**.
- The text in triple quotes is a **docstring**: a note saying what the function does.
- `return` hands a value back to whoever called the function. Without `return`, a function gives back `None`.

Parameters can have **default values**:

```python
def ground_km(cm_on_paper, scale=85_000):
    return cm_on_paper * scale / 100_000

ground_km(4)                 # uses scale 85,000 → 3.4
ground_km(4, scale=50_000)   # → 2.0
```

**Why functions?** You give a name to a step, test it once, and reuse it everywhere. When you ask AI for code, asking for *small, named functions* makes the result much easier to check (Module 10).

### `print` vs `return`

```python
def bad(x):
    print(x * 2)     # shows 10 on screen, but gives back None

def good(x):
    return x * 2     # gives back 10

y = bad(5)    # prints 10, but y is None
z = good(5)   # z is 10
```

## 4. Imports and reading a CSV file

```python
import csv
from pathlib import Path

csv_path = Path(r"D:\PythonCourse\data\capitals.csv")

with open(csv_path, encoding="utf-8") as f:
    reader = csv.DictReader(f)          # each row becomes a dictionary
    for row in reader:
        name = row["name"]
        pop = int(row["pop_max"])       # CSV values are ALWAYS text → convert
        if pop > 10_000_000:
            print(name, pop)
```

- `with ... as f:` opens the file, runs the block, and **closes the file automatically** afterwards, even if there's an error. You'll see `with` again in PyQGIS: `with edit(layer):` opens an edit session and saves it at the end (Module 05).
- `encoding="utf-8"` makes names like *Bogotá* and *Brasília* read correctly.

## 5. Errors: read the traceback

A **traceback** looks scary, but it follows a fixed pattern. Example:

```text
Traceback (most recent call last):
  File "D:\PythonCourse\...\ex02_4_fix_errors.py", line 12, in <module>
    print(capital["population"])
          ~~~~~~~^^^^^^^^^^^^^^
KeyError: 'population'
```

Read it **from the bottom up**:

1. **Last line: what happened.** `KeyError: 'population'`, so there's no key called `population`.
2. **Just above: where.** File, **line 12**, and the line itself, with `^^^^` under the problem.
3. Everything above that: the chain of calls that led there. Useful later, ignore it for now.

### The errors you'll meet most

| Error | Usually means | Typical fix |
|---|---|---|
| `SyntaxError` | Python can't parse the line: a missing `)`, `:` or quote. | Look at the line **and the one before it**. |
| `IndentationError` | Spaces don't line up. | Use 4 spaces per level, and don't mix tabs with spaces. |
| `NameError: name 'x' is not defined` | Typo, wrong case, or the variable was never created. | Check spelling and capital letters. |
| `TypeError` | Wrong kind of value, e.g. `"5" + 3`. | Convert with `int()`, `float()` or `str()`. |
| `KeyError` | That dictionary key (or field name) doesn't exist. | Print the keys, or use `.get()`. |
| `IndexError` | List position doesn't exist. | Remember lists start at 0, and check `len()`. |
| `AttributeError: 'NoneType' object has no attribute …` | Something you expected to exist came back as `None`. In QGIS this is usually *a layer that wasn't found*. | Find where the `None` came from, and check before using it. |
| `FileNotFoundError` | Wrong path. | `print(path)` and `path.exists()`. |

> **Fun fact:** the book's Chapter 2 has `print("Width: {}px".format(rlayer.width())`, which is missing one `)`. That's a `SyntaxError`. Typos in printed books are why "run it and read the error" beats "copy it and hope".

### Handling errors on purpose: `try` / `except`

```python
text = "n/a"
try:
    value = int(text)
except ValueError:
    value = None          # we expected this might happen, and decided what to do
```

> **AI red flag:** `except: pass` or `except Exception: pass`. That means "if anything at all goes wrong, say nothing". The script "succeeds" while doing nothing. Always ask the AI to remove it, or at least to `print` the error.

### `assert`: a check that complains

```python
assert layer_count == 9, f"expected 9 layers, got {layer_count}"
```

If the condition is `True`, nothing happens. If it's `False`, the script stops with your message. Checks like this are how you'll **verify AI code** in Week 4.

---

## Exercises

| File | Practises |
|---|---|
| `ex02_1_loops.py` | loops with the four patterns (total, count, build, best) |
| `ex02_2_functions.py` | writing small functions with `if`/`elif` and `return` |
| `ex02_3_read_csv.py` | reading `capitals.csv`, converting types, finding the nearest capitals |
| `ex02_4_fix_errors.py` | a script with **five bugs**: run, read the traceback, fix, repeat |

## Checkpoint

1. What's wrong with `if pop = 1000:`?
2. What does this print?
   ```python
   n = 0
   for x in [3, 8, 1, 9]:
       if x > 2:
           n += 1
   print(n)
   ```
3. A function ends with `print(result)` instead of `return result`. What do you get if you store its result in a variable?
4. In a traceback, which line do you read first?
5. Why is `except: pass` dangerous?

<details><summary>Answers</summary>

1. `=` stores, `==` compares. It should be `if pop == 1000:` (and it's a `SyntaxError` as written).
2. `3`. Three of the numbers are greater than 2.
3. `None`.
4. The last line: the error type and message. Then the line number just above it.
5. It hides every error, so a failure looks like a success.

</details>

## 🤖 With Claude

When you hit an error in an exercise, **don't paste it straight in.** First write down: (1) the error type, (2) the line, (3) your guess at the cause. Then paste the traceback with your guess and ask: *"Is my reading of this traceback right?"*

**Next:** [Module 03: Objects and the PyQGIS docs](../03-objects-and-docs/README.md)
