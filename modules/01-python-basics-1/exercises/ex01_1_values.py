"""
MODULE 01 - Exercise 1: values, variables, f-strings, paths

Fill in every TODO, save, and click Run Script.
If you see "All checks passed" you're done. A red AssertionError
tells you which answer to look at again.
"""
from pathlib import Path

# --- Part A: variables --------------------------------------------------------
# The Dead Sea shore is about 430 metres BELOW sea level.
# TODO: store the number -430 in a variable called shore_elevation
shore_elevation = None

# Mount Hermon summit is 2814 m.
hermon = 2814

# TODO: compute the difference in height between Hermon and the shore
#       (hint: hermon minus shore_elevation) and store it in height_range
height_range = None

# --- Part B: numbers and f-strings ---------------------------------------------
population = 9_751_717
city = "Lima"

# TODO: make this sentence exactly:  "Lima: 9.8 million people"
#       using an f-string with city and population (hint: divide by 1_000_000
#       and use :.1f)
sentence = None
print(sentence)

# --- Part C: paths -------------------------------------------------------------
# TODO: build a Path for D:\PythonCourse\output\map_01.pdf by starting from
#       Path(r"D:\PythonCourse") and joining "output" and "map_01.pdf" with /
pdf_path = None
print(pdf_path)

# TODO: use a property of pdf_path to get just "map_01.pdf"  (hint: .name)
file_name = None

# --- Checks (don't edit below this line) ------------------------------------
assert shore_elevation == -430, "Part A: shore_elevation should be -430 (a negative int)"
assert height_range == 3244, "Part A: height_range should be 2814 - (-430) = 3244"
assert sentence == "Lima: 9.8 million people", f"Part B: got {sentence!r}"
assert pdf_path == Path(r"D:\PythonCourse") / "output" / "map_01.pdf", "Part C: check the path"
assert file_name == "map_01.pdf", "Part C: use pdf_path.name"
print("All checks passed ✔")
