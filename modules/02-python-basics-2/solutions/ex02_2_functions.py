"""MODULE 02 - Solution 2: functions"""


def elevation_class(metres):
    """Return a class name for an elevation in metres."""
    if metres < 0:
        return "below sea level"
    elif metres < 500:
        return "lowland"
    elif metres < 1000:
        return "hills"
    else:
        return "mountains"


def ground_km(cm_on_paper, scale=85_000):
    """How many km on the ground is a distance measured on the map?"""
    return cm_on_paper * scale / 100_000


def pop_label(pop):
    """Short label for a population."""
    if pop >= 1_000_000:
        return f"{pop / 1_000_000:.1f} M"
    elif pop >= 1_000:
        return f"{pop / 1_000:.0f} k"
    else:
        return str(pop)


print(elevation_class(-427), elevation_class(820), elevation_class(1294))
print(ground_km(4.2), ground_km(4, scale=50_000))
print(pop_label(9_751_717), pop_label(835_000), pop_label(825))

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
