import re

with open("scripts/qimen_paipan.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("yingan_map_raw = get_flying_map(sg_actual, sg_idx, dun)", "yingan_map_raw = get_flying_map(5, sg_idx, dun)  # 时干入中五宫")
content = content.replace("angan_map_raw = get_flying_map(zs_target_g, sg_idx, dun)", "angan_map_raw = {i: [] for i in range(1, 10)}  # 暗干暂不独立排布")
content = content.replace("mid_str = f\"{yin_colored}{xing_str}{tp_str}  {dp_str}{an_colored}\"", "mid_str = f\"{yin_colored}{xing_str}{tp_str}  {dp_str}\"")
content = content.replace("an_colored = colorize(g['angan'], m.get('angan', []))", "")

with open("scripts/qimen_paipan.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched.")
