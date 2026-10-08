"""MODULE 01 - Solution 2: lists"""
rivers = ["Nile", "Amazonas", "Yangtze", "Mississippi", "Danube"]
lengths_km = [6650, 6400, 6300, 3730, 2850]

first = rivers[0]
last = rivers[-1]
middle = rivers[1:4]          # up to, but not including, index 4
count = len(rivers)

rivers.append("Jordan")
lengths_km.append(251)

longest = max(lengths_km)
alphabetical = sorted(rivers)
has_danube = "Danube" in rivers

print(first, last, middle, count, longest)
print(alphabetical)

assert first == "Nile", "first: remember counting starts at 0"
assert last == "Danube" or last == "Jordan", "last: use rivers[-1]"
assert middle == ["Amazonas", "Yangtze", "Mississippi"], "middle: rivers[1:4]"
assert count == 5, "count: len(rivers) BEFORE adding Jordan"
assert rivers[-1] == "Jordan" and lengths_km[-1] == 251, "append Jordan and 251"
assert longest == 6650, "longest: max(lengths_km)"
assert alphabetical[0] == "Amazonas" and alphabetical[-1] == "Yangtze", "sorted(rivers)"
assert has_danube is True, "has_danube: 'Danube' in rivers"
print("All checks passed ✔")
