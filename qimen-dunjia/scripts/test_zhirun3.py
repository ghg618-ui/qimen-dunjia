from datetime import datetime, timedelta
import qimen_paipan

def get_effective_jieqi_zhirun(dt):
    days = (dt.date() - datetime(1900, 1, 1).date()).days
    order = (10 + days) % 60
    futou_offset_days = order % 5
    futou_dt = datetime.combine(dt.date() - timedelta(days=futou_offset_days), datetime.min.time())
    
    futou_order = (order - futou_offset_days) % 60
    yuan = (futou_order % 15) // 5
    
    # 查找距离这个符头最近的节气名称
    # 穷举测试前后30天内的所有节气事件
    candidates = []
    for d in range(-30, 31):
        test_dt = futou_dt + timedelta(days=d)
        jq_idx, jq_name, jq_start = qimen_paipan.get_current_jieqi(test_dt)
        if not candidates or candidates[-1][1] != jq_name:
            candidates.append((jq_idx, jq_name, jq_start))
            
    # 找最近的
    best_jq_idx = 0
    best_jq_name = ""
    best_diff = 99999
    best_start = None
    for jq_idx, jq_name, jq_start in candidates:
        diff = abs((futou_dt - jq_start).total_seconds())
        if diff < best_diff:
            best_diff = diff
            best_jq_name = jq_name
            best_jq_idx = jq_idx
            best_start = jq_start
            
    return best_jq_idx, best_jq_name, yuan, best_start

for offset in range(-10, 5):
    t = datetime(2026, 12, 21, 12) + timedelta(days=offset)
    idx, eff_jq, yuan, jq_start = get_effective_jieqi_zhirun(t)
    print(t.strftime("%m-%d"), eff_jq, yuan, jq_start.strftime("%m-%d"))

