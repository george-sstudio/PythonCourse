"""MODULE 02 - Solution 4: the five bugs, fixed and explained"""
cities = [
    {"name": "Lima", "pop": "9751717"},
    {"name": "Quito", "pop": "2011388"},
    {"name": "Bogotá", "pop": "7772000"},
]

# BUG 1 - SyntaxError: '(' was never closed -> one ) missing at the end.
#         (This is the exact typo from the book's Chapter 2.)
print("Width: {}px".format(len(cities)))

# BUG 2 - TypeError: unsupported operand type(s) for +: 'int' and 'str'
#         pop is text in this table -> convert with int()
total = 0
for city in cities:
    total = total + int(city["pop"])

# BUG 3 - KeyError: 'Name' -> keys are case-sensitive; the key is "name"
first_name = cities[0]["name"]

# BUG 4 - IndexError: list index out of range -> 3 items = indexes 0,1,2.
#         The last one is cities[2], or better cities[-1]
last_city = cities[-1]

# BUG 5 - NameError: name 'Average' is not defined -> the variable is
#         'average' (lower case)
def per_city(total, n):
    return total / n

average = per_city(total, len(cities))
print(f"Average: {average:,.0f}")

assert total == 19_535_105
assert first_name == "Lima"
assert last_city["name"] == "Bogotá"
assert round(average) == 6_511_702
print("All checks passed ✔")
