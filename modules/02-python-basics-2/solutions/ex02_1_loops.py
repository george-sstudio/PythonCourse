"""MODULE 02 - Solution 1: loops"""
capitals = [
    {"name": "Lima",       "lat": -12.05, "pop": 9_751_717},
    {"name": "Nairobi",    "lat": -1.28,  "pop": 3_010_000},
    {"name": "Oslo",       "lat": 59.91,  "pop": 835_000},
    {"name": "Jakarta",    "lat": -6.17,  "pop": 9_125_000},
    {"name": "Ottawa",     "lat": 45.42,  "pop": 1_145_000},
    {"name": "Canberra",   "lat": -35.28, "pop": 327_700},
    {"name": "Reykjavík",  "lat": 64.15,  "pop": 166_212},
]

total_pop = 0
for c in capitals:
    total_pop += c["pop"]

south_count = 0
for c in capitals:
    if c["lat"] < 0:
        south_count += 1

big_names = []
for c in capitals:
    if c["pop"] > 1_000_000:
        big_names.append(c["name"])

northmost = None
northmost_lat = None
for c in capitals:
    if northmost_lat is None or c["lat"] > northmost_lat:
        northmost_lat = c["lat"]
        northmost = c["name"]

print("total:", total_pop)
print("southern:", south_count)
print("big:", big_names)
print("northmost:", northmost)

assert total_pop == 24_360_629, f"TODO 1: got {total_pop}"
assert south_count == 4, f"TODO 2: got {south_count}"
assert big_names == ["Lima", "Nairobi", "Jakarta", "Ottawa"], f"TODO 3: got {big_names}"
assert northmost == "Reykjavík", f"TODO 4: got {northmost}"
print("All checks passed ✔")
