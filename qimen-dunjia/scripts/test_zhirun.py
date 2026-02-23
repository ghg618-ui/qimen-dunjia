from datetime import datetime, timedelta
import qimen_paipan

for offset in range(-30, 10):
    dt = datetime(2026, 12, 21, 12, 0) + timedelta(days=offset)
    dz = qimen_paipan.get_ganzhi_day(dt)
    sy_str = ['上', '中', '下'][qimen_paipan.get_san_yuan(dz)]
    jq, jn, jd = qimen_paipan.get_current_jieqi(dt)
    print(f"{dt.strftime('%m-%d')} | {dz} | {sy_str}元 | {jn}")
