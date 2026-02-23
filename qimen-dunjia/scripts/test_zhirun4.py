from datetime import datetime, timedelta
import qimen_paipan

def get_ju_shu_zhirun(dt):
    from datetime import datetime, timedelta
    
    # 1. 计算当日的符头日期
    days = (dt.date() - datetime(1900, 1, 1).date()).days
    order = (10 + days) % 60
    futou_offset_days = order % 5
    futou_dt = datetime.combine(dt.date() - timedelta(days=futou_offset_days), datetime.min.time())
    
    # 2. 搜索符头前后16天内的所有节气，寻找距离符头最近的节气
    candidates = {}
    for d in range(-16, 17, 4):
        test_dt = futou_dt + timedelta(days=d)
        ji, jn, jd = qimen_paipan.get_current_jieqi(test_dt)
        if jn not in candidates:
            candidates[jn] = (ji, jd)
            
    best_diff = float('inf')
    best_ji = 0
    best_jn = ""
    for jn, (ji, jd) in candidates.items():
        diff = abs((futou_dt - jd).total_seconds())
        if diff < best_diff:
            best_diff = diff
            best_ji = ji
            best_jn = jn

    # 3. 三元局数
    dg = qimen_paipan.get_ganzhi_day(dt)
    sy = qimen_paipan.get_san_yuan(dg)
    
    if best_ji < 12:
        return '阳遁', qimen_paipan.YANGDUN_TABLE[best_ji][sy], best_jn
    else:
        return '阴遁', qimen_paipan.YINDUN_TABLE[best_ji][sy], best_jn

for offset in range(-5, 5):
    t = datetime(2026, 12, 21, 13, 31) + timedelta(days=offset)
    dun, ju, jn = get_ju_shu_zhirun(t)
    print(f"{t.strftime('%m-%d')}: {jn} {dun} {ju}局")
