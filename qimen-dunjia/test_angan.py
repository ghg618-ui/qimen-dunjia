from scripts.qimen_paipan import *
dt = datetime(2026, 2, 22, 9, 46)
yg = get_ganzhi_year(dt)
mg = get_ganzhi_month(dt)
dg = get_ganzhi_day(dt)
hg = get_ganzhi_hour(dt)
dun, ju = get_ju_shu(dt)
xs = get_xun_shou(hg)
dgan = get_dun_gan(xs)

dp = build_dipan(ju, dun)
xs_gong = [g for g, v in dp.items() if v == dgan][0]
xs_actual = 2 if xs_gong == 5 else xs_gong

# Doors
hz_idx = DIZHI.index(hg[1])
xs_zi_idx = DIZHI.index(xs[1:])
steps_count = (hz_idx - xs_zi_idx) % 12
curr_g = xs_gong
for _ in range(steps_count):
    if dun == '阳遁':
        curr_g = curr_g + 1 if curr_g < 9 else 1
    else:
        curr_g = curr_g - 1 if curr_g > 1 else 9
zs_target_g = 2 if curr_g == 5 else curr_g
men_steps = zhuanpan_rotate(xs_actual, zs_target_g)

# Original doors logic (Eight doors follow the Zhuanpan order)
mp = {}
door_home_stems = {}
for gong in range(1, 10):
    if gong == 5:
        continue
    pos = ZHUANPAN_ORDER.index(gong)
    src_pos = (pos - men_steps) % 8
    src_g = ZHUANPAN_ORDER[src_pos]
    m = BAMEN_ORIG[src_g]
    if m == '': m = BAMEN_ORIG[2]
    mp[gong] = m
    # "八门带干" (Yin Gan = the Earth Pan stem of the door's original home palace)
    door_home_stems[gong] = dp.get(src_g, '')

print("2026-02-22 09:46 Yang Dun 9")
print("Doors:")
for g in range(1, 10):
    if g == 5: continue
    print(f"Palace {g}: {mp[g]} -> Yin Gan (Home Di Pan): {door_home_stems[g]}")
