#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奇门遁甲排盘工具 v3.0 - 转盘奇门 · 置闰 · 寄坤宫
基于标准转盘奇门遁甲规则
"""

import sys
from datetime import datetime, timedelta, date

# ===== 基础常量 =====
TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 三奇六仪顺序
SANQI_LIUYI = ['戊', '己', '庚', '辛', '壬', '癸', '丁', '丙', '乙']

# 旬空表
XUN_KONG = {
    '甲子': '戌亥', '甲戌': '申酉', '甲申': '午未',
    '甲午': '辰巳', '甲辰': '寅卯', '甲寅': '子丑'
}

# 驿马表 (以时支查)
YIMA_MAP = {
    '申': 8, '子': 8, '辰': 8,
    '寅': 2, '午': 2, '戌': 2,
    '巳': 6, '酉': 6, '丑': 6,
    '亥': 4, '卯': 4, '未': 4
}

# 原始九星（按宫号1-9）
JIUXING_ORIG = {
    1: '天蓬', 2: '天芮', 3: '天冲', 4: '天辅',
    5: '天禽', 6: '天心', 7: '天柱', 8: '天任', 9: '天英'
}

# 原始八门（按宫号1-9，中5无门）
BAMEN_ORIG = {
    1: '休门', 2: '死门', 3: '伤门', 4: '杜门',
    5: '', 6: '开门', 7: '惊门', 8: '生门', 9: '景门'
}

# 八神
BASHEN = ['值符', '螣蛇', '太阴', '六合', '白虎', '玄武', '九地', '九天']

# 九宫名称
JIUGONG = {
    1: '坎一宫', 2: '坤二宫', 3: '震三宫', 4: '巽四宫',
    5: '中五宫', 6: '乾六宫', 7: '兑七宫', 8: '艮八宫', 9: '离九宫'
}

# 转盘八宫顺序（洛书顺序，不含中5）
# 坎1→艮8→震3→巽4→离9→坤2→兑7→乾6
ZHUANPAN_ORDER = [1, 8, 3, 4, 9, 2, 7, 6]

# 24节气
JIEQI = [
    '冬至', '小寒', '大寒', '立春', '雨水', '惊蛰',
    '春分', '清明', '谷雨', '立夏', '小满', '芒种',
    '夏至', '小暑', '大暑', '立秋', '处暑', '白露',
    '秋分', '寒露', '霜降', '立冬', '小雪', '大雪'
]

# 节气三元局数表（《烟波钓叟歌》）
YANGDUN_TABLE = {
    0: (1, 7, 4), 1: (2, 8, 5), 2: (3, 9, 6),   # 冬至/小寒/大寒
    3: (8, 5, 2), 4: (9, 6, 3), 5: (1, 7, 4),    # 立春/雨水/惊蛰
    6: (3, 9, 6), 7: (4, 1, 7), 8: (5, 2, 8),    # 春分/清明/谷雨
    9: (4, 1, 7), 10: (5, 2, 8), 11: (6, 3, 9),  # 立夏/小满/芒种
}
YINDUN_TABLE = {
    12: (9, 3, 6), 13: (8, 2, 5), 14: (7, 1, 4), # 夏至/小暑/大暑
    15: (2, 5, 8), 16: (1, 4, 7), 17: (9, 3, 6), # 立秋/处暑/白露
    18: (7, 1, 4), 19: (6, 9, 3), 20: (5, 8, 2), # 秋分/寒露/霜降
    21: (6, 9, 3), 22: (5, 8, 2), 23: (4, 7, 1), # 立冬/小雪/大雪
}

# 五虎遁年
WUHU = {
    '甲': '丙', '己': '丙', '乙': '戊', '庚': '戊',
    '丙': '庚', '辛': '庚', '丁': '壬', '壬': '壬',
    '戊': '甲', '癸': '甲'
}

# 五鼠遁日
WUSHU = {
    '甲': '甲', '己': '甲', '乙': '丙', '庚': '丙',
    '丙': '戊', '辛': '戊', '丁': '庚', '壬': '庚',
    '戊': '壬', '癸': '壬'
}

# 六甲遁干
LIUJIA_DUN = {
    '甲子': '戊', '甲戌': '己', '甲申': '庚',
    '甲午': '辛', '甲辰': '壬', '甲寅': '癸'
}

# 地支对应宫位
DIZHI_GONG = {
    '子': 1, '丑': 8, '寅': 8, '卯': 3,
    '辰': 4, '巳': 4, '午': 9, '未': 2,
    '申': 2, '酉': 7, '戌': 6, '亥': 6
}


# ===== 精确节气表（2024-2030年常用节气时刻） =====
# 格式: (年, 月, 日, 时, 分)
JIEQI_PRECISE = {
    # 2025-2026节气
    (2025, '冬至'): (2025, 12, 21, 23, 3),
    (2025, '小寒'): (2026, 1, 5, 16, 23),
    (2025, '大寒'): (2026, 1, 20, 9, 45),
    (2025, '立春'): (2026, 2, 4, 0, 2),
    (2025, '雨水'): (2026, 2, 18, 23, 51),
    (2025, '惊蛰'): (2026, 3, 5, 21, 58),
    (2025, '春分'): (2026, 3, 20, 22, 46),
    (2025, '清明'): (2026, 4, 5, 2, 39),
    (2025, '谷雨'): (2026, 4, 20, 9, 39),
    (2025, '立夏'): (2026, 5, 5, 20, 48),
    (2025, '小满'): (2026, 5, 21, 9, 36),
    (2025, '芒种'): (2026, 6, 5, 23, 48),
    (2025, '夏至'): (2026, 6, 21, 14, 11),
    (2025, '小暑'): (2026, 7, 7, 3, 57),
    (2025, '大暑'): (2026, 7, 22, 21, 13),
    (2025, '立秋'): (2026, 8, 7, 15, 43),
    (2025, '处暑'): (2026, 8, 23, 6, 19),
    (2025, '白露'): (2026, 9, 7, 21, 41),
    (2025, '秋分'): (2026, 9, 23, 7, 5),
    (2025, '寒露'): (2026, 10, 8, 9, 29),
    (2025, '霜降'): (2026, 10, 23, 12, 38),
    (2025, '立冬'): (2026, 11, 7, 13, 11),
    (2025, '小雪'): (2026, 11, 22, 10, 37),
    (2025, '大雪'): (2026, 12, 7, 7, 52),
    # 2024-2025
    (2024, '冬至'): (2024, 12, 21, 17, 21),
    (2024, '小寒'): (2025, 1, 5, 10, 33),
    (2024, '大寒'): (2025, 1, 20, 3, 59),
    (2024, '立春'): (2025, 2, 3, 18, 10),
    (2024, '雨水'): (2025, 2, 18, 18, 6),
    (2024, '惊蛰'): (2025, 3, 5, 16, 7),
    (2024, '春分'): (2025, 3, 20, 17, 1),
    (2024, '清明'): (2025, 4, 4, 21, 2),
    (2024, '谷雨'): (2025, 4, 20, 4, 15),
    (2024, '立夏'): (2025, 5, 5, 15, 57),
    (2024, '小满'): (2025, 5, 21, 4, 55),
    (2024, '芒种'): (2025, 6, 5, 19, 16),
    (2024, '夏至'): (2025, 6, 21, 9, 42),
    (2024, '小暑'): (2025, 7, 6, 22, 5),
    (2024, '大暑'): (2025, 7, 22, 15, 29),
    (2024, '立秋'): (2025, 8, 7, 9, 51),
    (2024, '处暑'): (2025, 8, 23, 0, 33),
    (2024, '白露'): (2025, 9, 7, 15, 52),
    (2024, '秋分'): (2025, 9, 23, 1, 19),
    (2024, '寒露'): (2025, 10, 8, 3, 41),
    (2024, '霜降'): (2025, 10, 23, 6, 51),
    (2024, '立冬'): (2025, 11, 7, 7, 4),
    (2024, '小雪'): (2025, 11, 22, 4, 35),
    (2024, '大雪'): (2025, 12, 7, 1, 44),
    # 2023-2024
    (2023, '冬至'): (2023, 12, 22, 11, 27),
    (2023, '小寒'): (2024, 1, 6, 4, 49),
    (2023, '大寒'): (2024, 1, 20, 22, 7),
    (2023, '立春'): (2024, 2, 4, 16, 27),
    (2023, '雨水'): (2024, 2, 19, 12, 13),
    (2023, '惊蛰'): (2024, 3, 5, 10, 23),
    (2023, '春分'): (2024, 3, 20, 11, 6),
    (2023, '清明'): (2024, 4, 4, 15, 2),
    (2023, '谷雨'): (2024, 4, 19, 21, 59),
    (2023, '立夏'): (2024, 5, 5, 8, 10),
    (2023, '小满'): (2024, 5, 20, 20, 59),
    (2023, '芒种'): (2024, 6, 5, 12, 10),
    (2023, '夏至'): (2024, 6, 21, 4, 51),
    (2023, '小暑'): (2024, 7, 6, 22, 20),
    (2023, '大暑'): (2024, 7, 22, 15, 44),
    (2023, '立秋'): (2024, 8, 7, 8, 9),
    (2023, '处暑'): (2024, 8, 22, 22, 55),
    (2023, '白露'): (2024, 9, 7, 11, 11),
    (2023, '秋分'): (2024, 9, 22, 20, 44),
    (2023, '寒露'): (2024, 10, 8, 3, 0),
    (2023, '霜降'): (2024, 10, 23, 6, 15),
    (2023, '立冬'): (2024, 11, 7, 6, 20),
    (2023, '小雪'): (2024, 11, 22, 3, 56),
    (2023, '大雪'): (2024, 12, 6, 23, 17),
    # 2026-2027
    (2026, '冬至'): (2026, 12, 22, 4, 50),
    (2026, '小寒'): (2027, 1, 5, 22, 15),
    (2026, '大寒'): (2027, 1, 20, 15, 25),
    (2026, '立春'): (2027, 2, 4, 9, 59),
    (2026, '雨水'): (2027, 2, 19, 5, 33),
    (2026, '惊蛰'): (2027, 3, 6, 3, 47),
    (2026, '春分'): (2027, 3, 21, 4, 30),
    (2026, '清明'): (2027, 4, 5, 8, 24),
    (2026, '谷雨'): (2027, 4, 20, 15, 13),
    (2026, '立夏'): (2027, 5, 6, 1, 40),
    (2026, '小满'): (2027, 5, 21, 14, 21),
    (2026, '芒种'): (2027, 6, 6, 5, 39),
    (2026, '夏至'): (2027, 6, 21, 22, 4),
    (2026, '小暑'): (2027, 7, 7, 15, 47),
    (2026, '大暑'): (2027, 7, 23, 8, 58),
    (2026, '立秋'): (2027, 8, 8, 1, 29),
    (2026, '处暑'): (2027, 8, 23, 16, 9),
    (2026, '白露'): (2027, 9, 8, 4, 31),
    (2026, '秋分'): (2027, 9, 23, 13, 50),
    (2026, '寒露'): (2027, 10, 8, 20, 25),
    (2026, '霜降'): (2027, 10, 23, 23, 22),
    (2026, '小雪'): (2027, 11, 22, 21, 5),
    (2026, '大雪'): (2027, 12, 7, 16, 34),
}


def get_current_jieqi(dt):
    """获取当前时间所在的节气 (基于 lunar_python 国家天文台精度历法算法)"""
    try:
        from lunar_python import Solar
    except ImportError:
        raise ImportError("检测到缺失 lunar_python 库，请使用配套的 `.command` 启动或执行 `pip install lunar_python`。")
        
    solar = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    lunar = solar.getLunar()
    # 查找距离刚才时间点最近的上一个节气（即当前所处的节气段的起点节气）
    # 传入 True 表示返回精准节气（含时分秒精确交节时间）
    jieqi = lunar.getPrevJieQi(True)
    name = jieqi.getName()
    
    jq_solar = jieqi.getSolar()
    jq_datetime = datetime(
        jq_solar.getYear(), jq_solar.getMonth(), jq_solar.getDay(),
        jq_solar.getHour(), jq_solar.getMinute(), jq_solar.getSecond()
    )
    
    idx = JIEQI.index(name)
    return idx, name, jq_datetime


# ===== 干支计算 =====
def __get_lunar(dt):
    try:
        from lunar_python import Solar
    except ImportError:
        raise ImportError("请确保已安装 lunar_python")
    return Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second).getLunar()

def get_ganzhi_year(dt):
    """干支纪年（以精确立春交节时间为界）"""
    return __get_lunar(dt).getYearInGanZhiExact()

def get_ganzhi_month(dt):
    """干支纪月（以精确交节时间为界）"""
    return __get_lunar(dt).getMonthInGanZhiExact()

def get_ganzhi_day(dt):
    """干支纪日（精确早晚子时划分）"""
    return __get_lunar(dt).getDayInGanZhiExact()

def get_ganzhi_hour(dt):
    """干支纪时"""
    return __get_lunar(dt).getTimeInGanZhi()


# ===== 旬首 =====
def get_xun_shou(gz):
    gi = TIANGAN.index(gz[0])
    zi = DIZHI.index(gz[1])
    xs_zi = (zi - gi) % 12
    return f"甲{DIZHI[xs_zi]}"


def get_dun_gan(xs):
    return LIUJIA_DUN.get(xs, '戊')


# ===== 三元局数 =====
def get_ganzhi_order(gi, zi):
    for n in range(60):
        if n % 10 == gi and n % 12 == zi:
            return n
    return 0


def get_san_yuan(dg):
    gi = TIANGAN.index(dg[0])
    zi = DIZHI.index(dg[1])
    r = get_ganzhi_order(gi, zi) % 15
    if r < 5: return 0
    elif r < 10: return 1
    else: return 2


def get_ju_shu(dt):
    """
    获取遁局，实现真正的置闰法核心（超神接气）：
    绝对规则：一个节气必须从上元开始！
    1. 找到该日的符头。
    2. 确定该符头是上、中、下哪一元。
    3. 找到该循环对应的【上元符头】日期。
    4. 找出距离该【上元符头】日期最近的真实节气交令时间。这就是该 15 天循环所属的“当值节气”。
       （当超神超过一气的半长 > 7.5天时，最近节气会自动变成上一个节气，从而实现完美的数学自动置闰）
    5. 取该当值节气对应当日本元的局数。
    """
    from datetime import datetime, timedelta, date
    
    # 1. 计算当日的干支序号和符头日
    days = (dt.date() - date(1900, 1, 1)).days
    order = (10 + days) % 60
    futou_offset_days = order % 5
    futou_order = order - futou_offset_days
    futou_dt = dt - timedelta(days=futou_offset_days)
    futou_date = datetime.combine(futou_dt.date(), datetime.min.time())
    
    # 2. 获取该符头所属的三元 (0:上元, 1:中元, 2:下元)
    sy = (futou_order % 15) // 5
    
    # 3. 找到对应的【上元符头】
    shangyuan_dt = futou_date - timedelta(days=sy * 5)
    
    # 4. 搜索上元符头前后的节气，寻找距离该【上元】最近的节气
    candidates = {}
    for d in range(-20, 21, 5):
        test_dt = shangyuan_dt + timedelta(days=d)
        ji, jn, jd = get_current_jieqi(test_dt)
        if jn not in candidates:
            candidates[jn] = (ji, jd)
            
    best_diff = float('inf')
    best_ji = 0
    for jn, (ji, jd) in candidates.items():
        diff = abs((shangyuan_dt - jd).total_seconds())
        if diff < best_diff:
            best_diff = diff
            best_ji = ji
            
    # 5. 根据当值节气和当日三元，获取阴阳属性和局数
    if best_ji < 12:
        return '阳遁', YANGDUN_TABLE[best_ji][sy]
    else:
        return '阴遁', YINDUN_TABLE[best_ji][sy]


# ===== 地盘 =====
def build_dipan(ju, dun):
    """地盘：阳遁顺排(1→2→...→9)，阴遁逆排(9→8→...→1)"""
    dp = {}
    order = list(range(1, 10))
    si = order.index(ju)
    for i, g in enumerate(SANQI_LIUYI):
        if dun == '阳遁':
            dp[order[(si + i) % 9]] = g
        else:
            dp[order[(si - i) % 9]] = g
    return dp


# ===== 转盘排布核心 =====
def zhuanpan_pos(gong):
    """宫在转盘顺序中的位置索引"""
    if gong == 5:
        return ZHUANPAN_ORDER.index(2)  # 中宫寄坤
    return ZHUANPAN_ORDER.index(gong)


def zhuanpan_rotate(from_gong, to_gong):
    """计算从from_gong到to_gong的转盘步数（顺时针）"""
    fp = zhuanpan_pos(from_gong)
    tp = zhuanpan_pos(to_gong)
    return (tp - fp) % 8


def paipan(dt):
    """完整排盘"""
    yg = get_ganzhi_year(dt)
    mg = get_ganzhi_month(dt)
    dg = get_ganzhi_day(dt)
    hg = get_ganzhi_hour(dt)
    ji, jn, jd = get_current_jieqi(dt)
    dun, ju = get_ju_shu(dt)
    sy = ['上元', '中元', '下元'][get_san_yuan(dg)]

    xs = get_xun_shou(hg)
    dgan = get_dun_gan(xs)

    # 地盘
    dp = build_dipan(ju, dun)

    # 旬首宫（遁干在地盘的位置）
    xs_gong = [g for g, v in dp.items() if v == dgan][0]
    xs_actual = 2 if xs_gong == 5 else xs_gong

    # 值符（旬首宫原始星），值使（旬首宫原始门）
    zf = JIUXING_ORIG[xs_gong]
    zs = BAMEN_ORIG[xs_gong]
    # 不需要将天禽强制改为天芮（热卜起局值符显示天禽）
    if zs == '':
        zs = '死门'

    # 时干宫（值符飞到的位置）
    hgan = hg[0]
    sg = dgan if hgan == '甲' else hgan
    sg_gong = [g for g, v in dp.items() if v == sg][0]
    sg_actual = 2 if sg_gong == 5 else sg_gong

    # 转盘旋转步数（九星）
    xing_steps = zhuanpan_rotate(xs_actual, sg_actual)

    # 时支宫与旬首支间距
    hz_idx = DIZHI.index(hg[1])
    xs_zi_idx = DIZHI.index(xs[1:])
    steps_count = (hz_idx - xs_zi_idx) % 12

    # 值使门飞动：阳遁123456789，阴遁987654321
    curr_g = xs_gong
    for _ in range(steps_count):
        if dun == '阳遁':
            curr_g = curr_g + 1 if curr_g < 9 else 1
        else:
            curr_g = curr_g - 1 if curr_g > 1 else 9
    zs_target_g = 2 if curr_g == 5 else curr_g
    men_steps = zhuanpan_rotate(xs_actual, zs_target_g)

    # ===== 九星（转盘旋转）=====
    xp = {}
    for gong in range(1, 10):
        if gong == 5:
            xp[5] = '天禽'
            continue
        pos = ZHUANPAN_ORDER.index(gong)
        src_pos = (pos - xing_steps) % 8
        src_g = ZHUANPAN_ORDER[src_pos]
        xp[gong] = JIUXING_ORIG[src_g]
    # 天禽永远寄居天芮宫
    rui_gong = [g for g, x in xp.items() if x == '天芮' or x == '芮禽'][0]
    xp[rui_gong] = '芮禽'

    # ===== 天盘干（星带干）=====
    tianpan = {}
    for gong in range(1, 10):
        if gong == 5:
            tianpan[5] = dp.get(5, '')
            continue
        pos = ZHUANPAN_ORDER.index(gong)
        src_pos = (pos - xing_steps) % 8
        src_gong = ZHUANPAN_ORDER[src_pos]
        tianpan[gong] = dp.get(src_gong, '')
    # 天禽带中5宫的干（癸/己等）
    tianqin_gan = dp.get(5, '')

    # ===== 八门（转盘旋转）=====
    mp = {}
    for gong in range(1, 10):
        if gong == 5:
            mp[5] = ''
            continue
        pos = ZHUANPAN_ORDER.index(gong)
        src_pos = (pos - men_steps) % 8
        src_g = ZHUANPAN_ORDER[src_pos]
        m = BAMEN_ORIG[src_g]
        if m == '': # 来自中宫
            m = BAMEN_ORIG[2] # 寄死门
        mp[gong] = m

    # ===== 八神（从值符落宫起排）=====
    sp = {}
    for i, shen in enumerate(BASHEN):
        if dun == '阳遁':
            pos = (ZHUANPAN_ORDER.index(sg_actual) + i) % 8
        else:
            pos = (ZHUANPAN_ORDER.index(sg_actual) - i) % 8
        sp[ZHUANPAN_ORDER[pos]] = shen
    sp[5] = ''

    # ===== 飞宫辅助函数 (1-9宫顺序) =====
    def get_flying_map(start_g, stem_idx, dun_type):
        """从 start_g 宫起，按 shigan_idx 开始飞布三奇六仪"""
        res = {i: [] for i in range(1, 10)}
        for step in range(9):
            if dun_type == '阳遁':
                # 阳遁顺序：1-2-3-4-5-6-7-8-9
                curr_g = (start_g + step - 1) % 9 + 1
            else:
                # 阴遁顺序：9-8-7-6-5-4-3-2-1
                # 使用减法
                curr_g = start_g - step
                while curr_g <= 0: curr_g += 9
            
            curr_stem = SANQI_LIUYI[(stem_idx + step) % 9]
            res[curr_g].append(curr_stem)
            
        return res

    # 时干索引
    shigan = dgan if hg[0] == '甲' else hg[0]
    sg_idx = SANQI_LIUYI.index(shigan)

    # ===== 隐干/引干 (热卜标准) =====
    # 热卜引干排法：时干加在值使门所在的宫位飞布；
    # 遇特殊情况（时干与值使落宫地盘奇仪相同）时，时干从中五宫起飞。
    zs_dp_stem = dp.get(zs_target_g, '')
    if shigan == zs_dp_stem:
        # 时干碰上同地盘干，转入中五宫起飞
        yingan_map_raw = get_flying_map(5, sg_idx, dun)
    else:
        # 正常情况：时干从值使落宫起飞
        yingan_map_raw = get_flying_map(zs_target_g, sg_idx, dun)
    yingan_map = {g: "".join(stems) for g, stems in yingan_map_raw.items()}

    # ===== 暗干 (暂不独立排布) =====
    angan_map_raw = {i: [] for i in range(1, 10)}
    angan_map = {g: "".join(stems) for g, stems in angan_map_raw.items()}


    # ===== 长生状态计算 =====
    def get_cs(gan, palace):
        if not gan or gan not in GAN_WUXING: return ""
        starts = {'甲':'亥', '乙':'午', '丙':'寅', '丁':'酉', '戊':'寅', '己':'酉', '庚':'巳', '辛':'子', '壬':'申', '癸':'卯'}
        dirs = {'甲':1, '乙':-1, '丙':1, '丁':-1, '戊':1, '己':-1, '庚':1, '辛':-1, '壬':1, '癸':-1}
        is_yin = dirs[gan] == -1
        
        BRANCHES = {
            1: ['子'], 8: ['丑', '寅'], 3: ['卯'], 4: ['辰', '巳'],
            9: ['午'], 2: ['未', '申'], 7: ['酉'], 6: ['戌', '亥'],
            5: ['未', '申'] # parasite Kun 2
        }
        targets = BRANCHES.get(palace, [])
        if not targets: return ""
        if is_yin and len(targets) > 1:
            targets = targets[::-1]
            
        dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        start_idx = dizhi.index(starts[gan])
        
        FULL_STATES = ["长生", "沐浴", "冠带", "临官", "帝旺", "衰", "病", "死", "墓", "绝", "胎", "养"]
        SHORT_STATES = {"长生": "生", "沐浴": "沐", "冠带": "冠", "临官": "临", "帝旺": "旺"}
        for s in FULL_STATES:
            if s not in SHORT_STATES:
                SHORT_STATES[s] = s
                
        res = []
        for tz in targets:
            target_idx = dizhi.index(tz)
            steps = (target_idx - start_idx) % 12 if dirs[gan] == 1 else (start_idx - target_idx) % 12
            state = FULL_STATES[steps]
            res.append(state)
            
        if len(res) == 1:
            return res[0]
        else:
            return SHORT_STATES[res[0]] + SHORT_STATES[res[1]]

    # 组合
    jg = {}
    for g in range(1, 10):
        # 地盘干集合（坤2需包含寄宫的己）
        dps = [dp.get(g, '')]
        if g == 2:
            center_dp = dp.get(5, '')
            if center_dp and center_dp not in dps:
                dps.append(center_dp)

        # 预计算长生状态
        tp_gan = tianpan.get(g, '')
        dp_gan = dp.get(g, '')
        
        jg[g] = {
            'name': JIUGONG[g],
            'dipan': dp_gan,
            'dipans': dps,
            'tianpan': tp_gan,
            'men': mp.get(g, ''),
            'xing': xp.get(g, ''),
            'shen': sp.get(g, ''),
            'yingan': yingan_map.get(g, ''),
            'yingans': yingan_map_raw.get(g, []),
            'angan': angan_map.get(g, ''),
            'angans': angan_map_raw.get(g, []),
            # 长生 (不考虑引干)
            'cs_tianpan': get_cs(tp_gan, g),
            'cs_dipan': get_cs(dp_gan, g),
            'cs_tianqin': get_cs(tianqin_gan, g) if g == rui_gong and tianqin_gan != tp_gan else ""
        }

    # 天禽带的干（来自中5宫地盘干）
    tianqin_gan = dp.get(5, '')

    return {
        'datetime': dt, 'year_gz': yg, 'month_gz': mg,
        'day_gz': dg, 'hour_gz': hg,
        'jieqi': jn, 'jieqi_date': jd,
        'dun_type': dun, 'ju_shu': ju,
        'san_yuan': sy, 'zhifu': zf, 'zhishi': zs,
        'xun_shou': xs, 'dun_gan': dgan, 'jiugong': jg,
        'rui_gong': rui_gong,          # 天芮+天禽合宫的宫号
        'tianqin_gan': tianqin_gan,    # 天禽带的干（中5地盘干）
        'xunkong': XUN_KONG.get(get_xun_shou(hg), ''), # 旬空
        'yima': YIMA_MAP.get(hg[1]),   # 驿马落宫
    }


# ===== ANSI颜色 =====
C_RESET = '\033[0m'
C_GREEN = '\033[32m'     # 符使
C_GRAY = '\033[90m'      # 入墓
C_BLUE = '\033[34m'      # 击刑
C_ORANGE = '\033[33m'    # 门迫
C_MAGENTA = '\033[35m'   # 刑+墓
C_RED = '\033[31m'       # 强调
C_BOLD = '\033[1m'

# 五行属性
WUXING = {
    1: '水', 2: '土', 3: '木', 4: '木',
    5: '土', 6: '金', 7: '金', 8: '土', 9: '火'
}

MEN_WUXING = {
    '休门': '水', '死门': '土', '伤门': '木', '杜门': '木',
    '景门': '火', '开门': '金', '惊门': '金', '生门': '土'
}

GAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}

# 入墓关系：天干→墓库宫
RUMU = {
    '乙': [2, 8],  # 木墓在丑未(艮8坤2)? 实为辰(巽4) — 规则因流派而异
    '丙': [6],     # 火墓在戌(乾6)
    '丁': [6],     # 火墓在戌(乾6)
    '壬': [4],     # 水墓在辰(巽4)
    '癸': [4],     # 水墓在辰(巽4)
}
# 标准三奇入墓：乙到坤2/艮8墓, 丙到乾6墓, 丁到坤2/艮8墓
RUMU_SANQI = {
    '乙': [2, 8],  # 乙奇入墓于丑未
    '丙': [6],     # 丙奇入墓于戌
    '丁': [2, 8],  # 丁奇入墓于丑未
}


def get_ke(wx1, wx2):
    """wx1是否克wx2"""
    ke_map = {'金': '木', '木': '土', '土': '水', '水': '火', '火': '金'}
    return ke_map.get(wx1) == wx2


def analyze_sihai(result):
    """
    四害分析——依据教材定义：
    ┌──────┬──────────────────────────────────────────────┐
    │ 门迫 │ 门的五行克所落之宫的五行（门克宫）             │
    │      │ 口诀：惊开三四休离九，伤杜二八景六七，生死居一 │
    ├──────┼──────────────────────────────────────────────┤
    │ 击刑 │ 六仪天干落指定宫时与宫位地支相刑（固定对应）   │
    │      │ 口诀：己2 戊3 壬癸4 庚8 辛9                   │
    ├──────┼──────────────────────────────────────────────┤
    │ 入墓 │ 天干落入其墓库宫                               │
    │      │ 甲癸→坤2  乙丙戊→乾6  丁己庚→艮8  辛壬→巽4  │
    ├──────┼──────────────────────────────────────────────┤
    │ 符使 │ 值符八神所在宫；值使门所在宫的门               │
    └──────┴──────────────────────────────────────────────┘
    注：击刑入墓同时出现在同一符号时，只论击刑不论入墓。
    """
    jg    = result['jiugong']
    marks = {g: {
        'shen': [], 'xing': [], 'tianpan': [], 'dipan': [], 'men': [],
        'yingan': [], 'angan': [], 'gan_tags': {}
    } for g in range(1, 10)}

    # ── 1. 符使 ──────────────────────────────────────────────────
    for g in range(1, 10):
        if g == 5: continue
        if jg[g]['shen'] == '值符':
            marks[g]['shen'].append('符使')
        if jg[g]['men'] == result['zhishi']:
            marks[g]['men'].append('符使')

    # ── 2. 门迫（门克宫：门的五行克所落之宫的五行）──────────────
    MEN_PO_TABLE = {
        '伤门': {2, 8}, '杜门': {2, 8},
        '开门': {3, 4}, '惊门': {3, 4},
        '休门': {9},
        '景门': {6, 7},
        '生门': {1},
        '死门': {1},
    }
    for g in range(1, 10):
        if g == 5: continue
        men = jg[g]['men']
        if men in MEN_PO_TABLE and g in MEN_PO_TABLE[men]:
            marks[g]['men'].append('门迫')

    # ── 3. 入墓与击刑（逐干独立判定）──────────────
    RUMU_GAN = {
        '甲': [2],  '癸': [2],
        '乙': [6],  '丙': [6], '戊': [6],
        '丁': [8],  '己': [8], '庚': [8],
        '辛': [4],  '壬': [4],
    }
    JIXING_TABLE = {
        '己': {2}, '戊': {3}, '壬': {4}, '癸': {4}, '庚': {8}, '辛': {9}
    }

    for g in range(1, 10):
        # 每个宫包含多个层面的天干：天盘、地盘、引干、暗干
        slots = [
            ('tianpan', jg[g]['tianpan']), 
            ('dipan', jg[g]['dipan']), 
            ('yingan', jg[g]['yingan']),
            ('angan', jg[g]['angan'])
        ]
        if g == result['rui_gong'] and result['tianqin_gan']:
            slots.append(('tianpan', result['tianqin_gan']))
        if len(jg[g]['dipans']) > 1:
            for extra in jg[g]['dipans'][1:]:
                slots.append(('dipan', extra))

        # 每个宫包含多个层面的天干：天盘、地盘、引干、暗干
        # 逐个层级处理，每个层级可能有多个干（如寄宫）
        levels = [
            ('tianpan', [jg[g]['tianpan']]),
            ('dipan', jg[g]['dipans']),
            ('yingan', jg[g]['yingans']),
            ('angan', jg[g]['angans'])
        ]
        if g == result['rui_gong'] and result['tianqin_gan']:
            levels[0][1].append(result['tianqin_gan'])

        for key, gans in levels:
            for gan in gans:
                if not gan: continue
                # 逐干独立判定四害标签
                gan_t = []
                if gan in RUMU_GAN and g in RUMU_GAN[gan]:
                    gan_t.append('入墓')
                if gan in JIXING_TABLE and g in JIXING_TABLE[gan]:
                    gan_t.append('击刑')
                
                # 记录到干属性表
                if gan not in marks[g]['gan_tags']:
                    marks[g]['gan_tags'][gan] = []
                for t in gan_t:
                    if t not in marks[g]['gan_tags'][gan]:
                        marks[g]['gan_tags'][gan].append(t)
                    # 同时记录到层级属性表（用于 UI 渲染该位置的样式）
                    if t not in marks[g][key]:
                        marks[g][key].append(t)

        # 层级 击刑优先逻辑
        for k in ['tianpan', 'dipan']:
            t = marks[g][k]
            if '击刑' in t and '入墓' in t:
                t.remove('入墓')

    return marks



def colorize(text, tags):
    """根据标记添加颜色"""
    if not tags:
        return text
    if '门迫' in tags and '入墓' in tags:
        return f"{C_MAGENTA}{text}{C_RESET}"
    if '符使' in tags:
        return f"{C_GREEN}{text}{C_RESET}"
    if '门迫' in tags:
        return f"{C_ORANGE}{text}{C_RESET}"
    if '入墓' in tags:
        return f"{C_GRAY}{text}{C_RESET}"
    if '击刑' in tags:
        return f"{C_BLUE}{text}{C_RESET}"
    return text


def display_width(text):
    """计算终端显示宽度（去除ANSI转义码后）"""
    import re
    clean = re.sub(r'\033\[[0-9;]*m', '', text)
    return sum(2 if ('\u4e00' <= c <= '\u9fff' or c in '：（）') else 1 for c in clean)


def pad_cell(text, width):
    """居中填充文本到指定宽度"""
    dw = display_width(text)
    pad = width - dw
    lp = max(0, pad // 2)
    rp = max(0, pad - lp)
    return " " * lp + text + " " * rp


def print_result(r):
    """打印排盘结果（含四害颜色标注）"""
    marks = analyze_sihai(r)

    print("\n" + "=" * 62)
    print("奇门遁甲排盘（转盘·置闰·寄坤宫）".center(46))
    print("=" * 62)
    dt = r['datetime']
    print(f"\n排盘时间：{dt.strftime('%Y年%m月%d日 %H:%M')}")
    print(f"干支四柱：{r['year_gz']}年 {r['month_gz']}月 {r['day_gz']}日 {r['hour_gz']}时")
    print(f"节    气：{r['jieqi']}（{r['jieqi_date'].strftime('%m月%d日 %H:%M')}）")
    print(f"遁局信息：{r['dun_type']}{r['ju_shu']}局 ({r['san_yuan']})")
    print(f"旬    首：{r['xun_shou']}（甲遁{r['dun_gan']}）  空亡：{r['xunkong']}")
    print(f"值符值使：{C_GREEN}{r['zhifu']}{C_RESET} / {C_GREEN}{r['zhishi']}{C_RESET}  驿马：{JIUGONG.get(r['yima'], '')}")

    print("\n" + "-" * 62)
    print("九宫格局 (引星天  地暗)".center(56))
    print("-" * 62 + "\n")

    jg = r['jiugong']
    layout = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
    cw = 20

    print("┌" + "─" * cw + "┬" + "─" * cw + "┬" + "─" * cw + "┐")
    for ri, row in enumerate(layout):
        cells = []
        for gn in row:
            g = jg[gn]
            m = marks.get(gn, {})
            # 空亡标记
            kong_mark = "○" if r['xunkong'] and any(z in r['xunkong'] for z in [k for k,v in DIZHI_GONG.items() if v==gn]) else ""
            
            if gn == 5:
                yin_col = colorize(g['yingan'], m.get('yingan', []))
                cells.append([
                    g['name'],
                    f"  {yin_col}{g['dipan']}",
                    ''
                ])
            else:
                # 八神行
                shen_str = g['shen'] if g['shen'] else '(寄坤)'
                if gn == r['yima']: shen_str += "🐎"
                shen_colored = colorize(kong_mark + shen_str, m.get('shen', []))

                # 星+天盘+地盘+引干+暗干
                xing_str = g['xing'] if g['xing'] else '(寄坤)'
                
                # 天盘干处理：芮禽宫需显示两个
                tps = [g['tianpan']]
                if gn == r['rui_gong'] and r.get('tianqin_gan'):
                    tps.append(r['tianqin_gan'])
                tp_str = "".join([colorize(t, m.get('gan_tags', {}).get(t, [])) for t in tps])
                
                # 地盘处理：坤二宫显示多个干
                dp_str = "".join([colorize(d, m.get('gan_tags', {}).get(d, [])) for d in g['dipans']])
                
                yin_colored = colorize(g['yingan'], m.get('yingan', []))
                
                
                # 布局：引星天  地暗
                mid_str = f"{yin_colored}{xing_str}{tp_str}  {dp_str}"

                # 八门行
                men_colored = colorize(g['men'], m.get('men', []))

                cells.append([shen_colored, mid_str, men_colored])

        for li in range(3):
            rs = "│"
            for ci in range(3):
                txt = cells[ci][li] if li < len(cells[ci]) else ''
                rs += pad_cell(txt, cw) + "│"
            print(rs)
        if ri < 2:
            print("├" + "─" * cw + "┼" + "─" * cw + "┼" + "─" * cw + "┤")
    print("└" + "─" * cw + "┴" + "─" * cw + "┴" + "─" * cw + "┘")

    # 颜色说明
    print(f"\n颜色说明：{C_GREEN}符使{C_RESET}、{C_GRAY}入墓{C_RESET}、"
          f"{C_BLUE}击刑{C_RESET}、{C_ORANGE}门迫{C_RESET}、{C_MAGENTA}刑+墓{C_RESET}")
    print("\n" + "=" * 62 + "\n")


def main():
    if len(sys.argv) > 1:
        try:
            dt = datetime.strptime(sys.argv[1], "%Y-%m-%d %H:%M")
        except:
            print("时间格式错误，请使用：YYYY-MM-DD HH:MM")
            sys.exit(1)
    else:
        dt = datetime.now()
    result = paipan(dt)
    print_result(result)


if __name__ == "__main__":
    main()
