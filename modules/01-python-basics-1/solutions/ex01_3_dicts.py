"""MODULE 01 - Solution 3: dictionaries"""
country = {
    "name": "Peru",
    "adm0_a3": "PER",
    "continent": "South America",
    "pop_est": 32_510_453,
    "gdp_md": 226_848,
}

continent = country["continent"]
gdp_per_person = round(country["gdp_md"] * 1_000_000 / country["pop_est"])
country["capital"] = "Lima"
area = country.get("area_km2", 0)

table = [
    {"name": "Peru",     "pop_est": 32_510_453},
    {"name": "Ecuador",  "pop_est": 17_373_662},
    {"name": "Colombia", "pop_est": 50_339_443},
]
last_name = table[-1]["name"]
ecuador_pop = table[1]["pop_est"]

print(continent, gdp_per_person, area, last_name, ecuador_pop)

assert continent == "South America", "continent: country['continent']"
assert gdp_per_person == 6978, f"gdp_per_person: got {gdp_per_person} - check units"
assert country.get("capital") == "Lima", "add the key: country['capital'] = 'Lima'"
assert area == 0, "area: country.get('area_km2', 0)"
assert last_name == "Colombia", "last_name: table[-1]['name']"
assert ecuador_pop == 17_373_662, "ecuador_pop: table[1]['pop_est']"
print("All checks passed ✔")
