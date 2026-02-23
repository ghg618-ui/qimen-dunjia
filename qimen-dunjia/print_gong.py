from datetime import datetime
from scripts.qimen_paipan import paipan

res = paipan(datetime(1987, 5, 8, 16, 14))
jg = res['jiugong']
print(f"Jieqi: {res['jieqi']} {res['jieqi_date']}")
print(f"Ju: {res['dun_type']}{res['ju_shu']}")
print(f"Zhifu: {res['zhifu']}, Zhishi: {res['zhishi']}")
for g in [4, 9, 2, 3, 5, 7, 8, 1, 6]:
    if g == 5: continue
    print(f"[{g}] Shen:{jg[g]['shen']} Xing:{jg[g]['xing']} Men:{jg[g]['men']} TP:{jg[g]['tianpan']} DP:{jg[g]['dipan']} YG:{jg[g]['yingan']}")
