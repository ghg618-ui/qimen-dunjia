
from datetime import date
d0 = date(1900, 1, 1)
d1 = date(2026, 2, 21)
delta = (d1 - d0).days
print(f"Days: {delta}")
print(f"Gan index: {delta % 10}")
print(f"Zhi index: (10 + delta) % 12: {(10 + delta) % 12}")
