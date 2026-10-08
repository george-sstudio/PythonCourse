"""
MODULE 02 - Exercise 1: loops

A small table of capitals (a list of dictionaries, as in Module 01).
Use a  for  loop for each TODO. Save and Run Script.
"""
capitals = [
    {"name": "Lima",       "lat": -12.05, "pop": 9_751_717},
    {"name": "Nairobi",    "lat": -1.28,  "pop": 3_010_000},
    {"name": "Oslo",       "lat": 59.91,  "pop": 835_000},
    {"name": "Jakarta",    "lat": -6.17,  "pop": 9_125_000},
    {"name": "Ottawa",     "lat": 45.42,  "pop": 1_145_000},
    {"name": "Canberra",   "lat": -35.28, "pop": 327_700},
    {"name": "Reykjavík",  "lat": 64.15,  "pop": 166_212},
]

# TODO 1 (accumulate): total population of all capitals
total_pop = 0


# TODO 2 (count): how many capitals are in the southern hemisphere (lat < 0)?
south_count = 0


# TODO 3 (build a list): names of capitals with more than 1 million people
big_names = []


# TODO 4 (best so far): the name of the capital furthest NORTH (highest lat)
northmost = None
northmost_lat = None


print("total:", total_pop)
print("southern:", south_count)
print("big:", big_names)
print("northmost:", northmost)

# --- Checks (don't edit below this line) ------------------------------------
assert total_pop == 24_360_629, f"TODO 1: got {total_pop}"
assert south_count == 4, f"TODO 2: got {south_count}"
assert big_names == ["Lima", "Nairobi", "Jakarta", "Ottawa"], f"TODO 3: got {big_names}"
assert northmost == "Reykjavík", f"TODO 4: got {northmost}"
print("All checks passed ✔")
