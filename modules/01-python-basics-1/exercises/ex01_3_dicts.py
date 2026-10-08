"""
MODULE 01 - Exercise 3: dictionaries (one row of an attribute table)

Fill in every TODO, save, and Run Script.
"""
# One row of the 'countries' layer, as a dictionary
country = {
    "name": "Peru",
    "adm0_a3": "PER",
    "continent": "South America",
    "pop_est": 32_510_453,
    "gdp_md": 226_848,
}

# TODO: read the continent
continent = None

# TODO: GDP per person in US dollars.
#       gdp_md is in MILLIONS of dollars, so multiply by 1_000_000 first,
#       then divide by pop_est. Round to a whole number with round(...).
gdp_per_person = None

# TODO: add a new key "capital" with the value "Lima"


# TODO: safely read a key that does NOT exist: "area_km2".
#       Use .get so that you get 0 instead of a crash.
area = None

# A small table: a list of dictionaries
table = [
    {"name": "Peru",     "pop_est": 32_510_453},
    {"name": "Ecuador",  "pop_est": 17_373_662},
    {"name": "Colombia", "pop_est": 50_339_443},
]

# TODO: the name in the LAST row of the table
last_name = None

# TODO: the population of Ecuador (row 1)
ecuador_pop = None

print(continent, gdp_per_person, area, last_name, ecuador_pop)

# --- Checks (don't edit below this line) ------------------------------------
assert continent == "South America", "continent: country['continent']"
assert gdp_per_person == 6978, f"gdp_per_person: got {gdp_per_person} - check units"
assert country.get("capital") == "Lima", "add the key: country['capital'] = 'Lima'"
assert area == 0, "area: country.get('area_km2', 0)"
assert last_name == "Colombia", "last_name: table[-1]['name']"
assert ecuador_pop == 17_373_662, "ecuador_pop: table[1]['pop_est']"
print("All checks passed ✔")
