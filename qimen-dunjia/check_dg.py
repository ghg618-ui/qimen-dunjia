from datetime import date
d1 = date(1900, 1, 1) # This was 甲戌 (11)
d2 = date(2026, 2, 22)
diff = (d2 - d1).days
print("diff:", diff)
print("ganzhi index:", (10 + diff) % 60)
