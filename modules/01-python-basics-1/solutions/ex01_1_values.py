"""MODULE 01 - Solution 1: values, variables, f-strings, paths"""
from pathlib import Path

# Part A
shore_elevation = -430
hermon = 2814
height_range = hermon - shore_elevation      # 2814 - (-430) = 3244

# Part B
population = 9_751_717
city = "Lima"
sentence = f"{city}: {population / 1_000_000:.1f} million people"
print(sentence)

# Part C
pdf_path = Path(r"D:\PythonCourse") / "output" / "map_01.pdf"
print(pdf_path)
file_name = pdf_path.name

# Checks
assert shore_elevation == -430, "Part A: shore_elevation should be -430 (a negative int)"
assert height_range == 3244, "Part A: height_range should be 2814 - (-430) = 3244"
assert sentence == "Lima: 9.8 million people", f"Part B: got {sentence!r}"
assert pdf_path == Path(r"D:\PythonCourse") / "output" / "map_01.pdf", "Part C: check the path"
assert file_name == "map_01.pdf", "Part C: use pdf_path.name"
print("All checks passed ✔")
