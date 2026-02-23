
from qimen_paipan import get_xun_shou, get_ganzhi_hour, get_ganzhi_day, datetime, TIANGAN, DIZHI

dt = datetime(2026, 2, 21, 16, 49)
dg = get_ganzhi_day(dt)
hg = get_ganzhi_hour(dt)
xs = get_xun_shou(hg)
print(f"Day: {dg}")
print(f"Hour: {hg}")
print(f"Xun Shou: {xs}")
