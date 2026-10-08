"""
MODULE 02 - Exercise 4: fix the five bugs

This script has FIVE bugs. Run it. It stops at the first one.
For each error:
   1. read the LAST line of the traceback (what went wrong)
   2. read the line number (where)
   3. write your diagnosis in the comment next to the BUG marker
   4. fix it and run again
Repeat until you see "All checks passed".
Don't change the checks at the bottom.

Note: the first bug is a SyntaxError. Python checks the grammar of the
WHOLE file before running any of it, so nothing runs at all, and the
QGIS editor may mark the line with a red underline instead of printing a
traceback. All the other bugs show up only when their line runs.
"""
cities = [
    {"name": "Lima", "pop": "9751717"},       # note: pop is TEXT here
    {"name": "Quito", "pop": "2011388"},
    {"name": "Bogotá", "pop": "7772000"},
]

# BUG? diagnosis: ...
print("Width: {}px".format(len(cities))

# BUG? diagnosis: ...
total = 0
for city in cities:
    total = total + city["pop"]

# BUG? diagnosis: ...
first_name = cities[0]["Name"]

# BUG? diagnosis: ...
last_city = cities[3]

# BUG? diagnosis: ...
def per_city(total, n):
    return total / n

average = per_city(total, len(cities))
print(f"Average: {Average:,.0f}")

# --- Checks (don't edit below this line) ------------------------------------
assert total == 19_535_105
assert first_name == "Lima"
assert last_city["name"] == "Bogotá"
assert round(average) == 6_511_702
print("All checks passed ✔")
