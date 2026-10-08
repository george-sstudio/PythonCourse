"""
MODULE 02 - Exercise 2: functions

Write the body of each function (replace the  pass  line).
Save and Run Script - the checks call your functions.
"""


def elevation_class(metres):
    """Return a class name for an elevation in metres:
         below 0      -> "below sea level"
         0 to 499     -> "lowland"
         500 to 999   -> "hills"
         1000 or more -> "mountains"
    """
    pass  # TODO: replace with if / elif / else and return


def ground_km(cm_on_paper, scale=85_000):
    """How many km on the ground is a distance measured on the map?
    (1 km = 100,000 cm)"""
    pass  # TODO


def pop_label(pop):
    """Short label for a population:
         1,000,000 or more  -> "9.8 M"   (millions, 1 decimal)
         1,000 or more      -> "835 k"   (thousands, no decimals)
         otherwise          -> "825"     (just the number as text)
    """
    pass  # TODO


# Try your functions here:
print(elevation_class(-427), elevation_class(820), elevation_class(1294))
print(ground_km(4.2), ground_km(4, scale=50_000))
print(pop_label(9_751_717), pop_label(835_000), pop_label(825))

# --- Checks (don't edit below this line) ------------------------------------
assert elevation_class(-427) == "below sea level"
assert elevation_class(0) == "lowland"
assert elevation_class(499) == "lowland"
assert elevation_class(500) == "hills"
assert elevation_class(1294) == "mountains"
assert abs(ground_km(4.2) - 3.57) < 1e-9, "ground_km: cm * scale / 100_000"
assert ground_km(4, scale=50_000) == 2.0
assert pop_label(9_751_717) == "9.8 M", f"got {pop_label(9_751_717)!r}"
assert pop_label(835_000) == "835 k", f"got {pop_label(835_000)!r}"
assert pop_label(825) == "825", f"got {pop_label(825)!r}"
print("All checks passed ✔")
