from datetime import datetime, timedelta
import qimen_paipan

def get_effective_jieqi_zhirun(dt):
    """
    真正的置闰法定局逻辑（简化版）：
    1. 计算当日的符头（甲子、己巳、甲戌...等开始的日期）。
    2. 找到该符头（对应某日前后）最近的节气。
    3. 符头最近的节气即为“置闰法”下应当使用的节气。
    但置闰法只有在芒种、大雪后才会置闰。我们先不考虑跨年置闰积累问题，
    只用“距离符头最近的节气”的近似法，看看是否能算出正确的定局。
    """
    days = (dt.date() - datetime(1900, 1, 1).date()).days
    # 1900-1-1 是甲戌(10). 
    # 甲戌是下元符头。
    order = (10 + days) % 60
    futou_offset_days = order % 5  # 本周期已过天数（0-4）
    
    # 获取符头当天的午夜时刻
    futou_dt = datetime.combine(dt.date() - timedelta(days=futou_offset_days), datetime.min.time())
    
    # 这个符头是上元、中元还是下元？
    # 符头的 order:
    futou_order = (order - futou_offset_days) % 60
    # 0(甲子), 15(己卯), 30(甲午), 45(己酉) 是上元 -> futou_order % 15 == 0
    # 5, 20, 35, 50 是中元
    # 10, 25, 40, 55 是下元
    yuan = (futou_order % 15) // 5  # 0:上, 1:中, 2:下
    
    # 找最近的节气
    # 可以用一个循环去查符头前后15天的节气
    closest_jq = None
    min_diff = 999
    
    # 稍微复杂一点：从符头时间起寻找节气
    # 我们知道 qimen_paipan.get_current_jieqi 可以获取节气
    # 直接查符头所在的真正的节气，以及前后的节气，看距离（天数）
    _, jq_name, jq_dt = qimen_paipan.get_current_jieqi(futou_dt)
    
    # 还要看看后一个节气
    _, next_jq_name, next_jq_dt = qimen_paipan.get_current_jieqi(futou_dt + timedelta(days=16))
    
    diff_curr = abs((futou_dt - jq_dt).total_seconds())
    diff_next = abs((futou_dt - next_jq_dt).total_seconds())
    
    if diff_curr <= diff_next:
        eff_jq = jq_name
        eff_jq_dt = jq_dt
    else:
        eff_jq = next_jq_name
        eff_jq_dt = next_jq_dt
        
    return eff_jq, yuan, eff_jq_dt

for offset in range(-10, 5):
    t = datetime(2026, 12, 21, 12) + timedelta(days=offset)
    eff_jq, yuan, jq_dt = get_effective_jieqi_zhirun(t)
    print(t.strftime("%m-%d"), eff_jq, yuan, jq_dt.strftime("%m-%d"))

