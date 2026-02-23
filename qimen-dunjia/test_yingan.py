from datetime import datetime
from scripts.qimen_paipan import paipan

dt = datetime.strptime("2025-01-22 19:45", "%Y-%m-%d %H:%M")
res = paipan(dt)
jg = res['jiugong']
for g in [4, 9, 2, 3, 5, 7, 8, 1, 6]:
    yg = jg[g]['yingan'] if g in jg and 'yingan' in jg[g] else ''
    print(f"Palace {g}: {yg}")
