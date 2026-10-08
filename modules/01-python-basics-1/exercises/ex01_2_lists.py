"""
MODULE 01 - Exercise 2: lists

Fill in every TODO, save, and Run Script.
"""
rivers = ["Nile", "Amazonas", "Yangtze", "Mississippi", "Danube"]
lengths_km = [6650, 6400, 6300, 3730, 2850]   # same order as rivers

# TODO: the first river in the list
first = None

# TODO: the last river, using a negative index
last = None

# TODO: a slice with the 2nd, 3rd and 4th rivers  (indexes 1, 2, 3)
middle = None

# TODO: how many rivers are in the list? (use len)
count = None

# TODO: add "Jordan" to the end of rivers, and 251 to the end of lengths_km
#       (use .append on each list - two lines)


# TODO: the longest length in lengths_km (use max)
longest = None

# TODO: the rivers in alphabetical order (use sorted - it makes a new list)
alphabetical = None

# TODO: True/False - is "Danube" in the list?  (use the word  in)
has_danube = None

print(first, last, middle, count, longest)
print(alphabetical)

# --- Checks (don't edit below this line) ------------------------------------
assert first == "Nile", "first: remember counting starts at 0"
assert last == "Danube" or last == "Jordan", "last: use rivers[-1]"
assert middle == ["Amazonas", "Yangtze", "Mississippi"], "middle: rivers[1:4]"
assert count == 5, "count: len(rivers) BEFORE adding Jordan"
assert rivers[-1] == "Jordan" and lengths_km[-1] == 251, "append Jordan and 251"
assert longest == 6650, "longest: max(lengths_km)"
assert alphabetical[0] == "Amazonas" and alphabetical[-1] == "Yangtze", "sorted(rivers)"
assert has_danube is True, "has_danube: 'Danube' in rivers"
print("All checks passed ✔")
