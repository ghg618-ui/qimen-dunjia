#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奇门遁甲排盘 - HTML网页输出 v12
新增：长生状态切换、上一局、下一局跳转提示
"""
import sys, os, webbrowser, json, sqlite3
from datetime import datetime, timedelta
from urllib.parse import urlparse, unquote
import socketserver, http.server, base64
from qimen_paipan import paipan, analyze_sihai

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'cases.db')
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        question TEXT,
        notes TEXT,
        bazi TEXT,
        ju_shu TEXT,
        chart_time TEXT,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()
init_db()

XUN_KONG = {
    '甲子':'戌亥','甲戌':'申酉','甲申':'午未',
    '甲午':'辰巳','甲辰':'寅卯','甲寅':'子丑'
}

NAJI_WUXIANG = {
    "甲": "龙、麒麟、高贵物品", "乙": "中药材、葫芦、艺术品、花草、弯曲的东西、木质的门窗、桌椅、领带、蔬菜、水果、茶叶、绳子、木雕、管道、面条、楼梯",
    "丙": "太阳、圆形的、饼形的、红色的、血液、炉火、眼镜、发光的东西、发热的东西、火焰、小太阳、镜子、炉灶、官印、印章、饼干、火箭、大炮、变压器",
    "丁": "尖锐的、带刺的、蜡烛、发光体、灯、刀、针、剑、注射器、钉子、牙签、香火、焰火、打火机、子弹、耳钉、烟、针灸",
    "戊": "陶土制品、陶瓷制品、水泥制品、钱、黄金", "己": "弯曲之物、土制品、泥制品、卷曲状物品、绳索、线团、垃圾、肮脏污秽之物",
    "庚": "骨头、刀、武器、石头、石制品、器械、金属制品、汽车", "辛": "钱币、小颗粒物、小型金属物品、饰品、戒指、项链、手镯、小摆件、钥匙、螺丝、手表、佛珠、金银珠宝、小刀",
    "壬": "自来水、水管、消防用品、热水器", "癸": "加工过的水、酒、醋、茶、饮品、油漆、液体、污水、厕所、水坑",
    "值符": "高档的、名贵的、贵重的、钱币、珠宝首饰、名贵古董、钻石、名人字画、印章、符", "腾蛇": "虚假的、虚幻的、耀眼的、绳子、锁链、灯、霓虹灯、香火",
    "太阴": "观音像、隐蔽的、暗处的、阴暗角落、羽毛、化妆品、冰", "六合": "具备合作属性的，例如：合同、合约、伞、窗、结婚证书、羽毛",
    "白虎": "金属、刀剑、枪支、石头制品、铁制品", "玄武": "假货",
    "九地": "旧物、五谷、砂石、缸、瓦盆、土制品、首饰盒", "九天": "会飞的、高大的、飞机模型",
    "天蓬": "伞、雨具、渔具", "天任": "老牛、桌子、椅子、鞋子", "天冲": "具有速度属性的、枪炮、汽车、发令枪、弹药",
    "天辅": "文书、木制品、优雅之物", "天英": "亮丽的东西、爆炸易燃物品、烟花爆竹、霓虹灯、灯具、与火一样的食物",
    "天芮": "菩萨、神佛像", "天柱": "乐器、音响、喇叭等发声的物品", "天心": "芯片、贵重物品、神像、佛像",
    "休门": "水、休闲物品", "生门": "植物、生活用品、财库、装钱的东西、生长之物",
    "伤门": "刀、剑、剪子、针、枪、炮、锐器、破裂不完整的物体", "杜门": "门窗、瓶塞、瓶盖",
    "景门": "文书、风景照、照片、图画、图书、艺术品、文件、合同、证书、颜料、油漆、美容美发用品、书籍、烟花爆竹、霓虹灯、电视机、投影仪",
    "死门": "死人照片、墓碑、死物、木偶、玩偶", "惊门": "风铃、钟、音响、电视、电话、乐器等发出声响的物体", "开门": "有开口的东西",
}

NAJI_XINGWEI = {
    "甲": "高级穿着打扮", "乙": "摆弄花木、手写日记、双手合十祈福",
    "丙": "点香祈福、清理个人形象、戴眼镜", "丁": "点香诵经、喝吸管饮料",
    "戊": "吃肉、烤肉串、整理财务钱包", "己": "吃小零食、静坐",
    "庚": "抄经、读经典", "辛": "忏悔许愿、改变布局、吃辛辣",
    "壬": "走路、喝水饮料", "癸": "走动、喝茶、洗净面部",
    "值符": "穿戴高贵大方", "腾蛇": "佩戴带花纹饰物",
    "太阴": "衣着素净典雅、暗中行事", "六合": "与人沟通交流、聚会",
    "白虎": "态度干练、保持威严", "玄武": "保持低调",
    "九地": "保守低姿态、静卧休息", "九天": "积极行动、登高望远",
    "休门": "放松休息、沐浴更衣", "生门": "浇水土培、投资理财规划",
    "开门": "外出活动、开始工作", "景门": "打理妆容、开灯、点香薰蜡烛"
}

NAJI_COLORS = {
    "甲": "绿", "乙": "浅绿",
    "丙": "红", "丁": "浅红",
    "戊": "棕黄", "己": "浅黄",
    "庚": "白", "辛": "金",
    "壬": "蓝黑", "癸": "浅蓝"
}

NAJI_CATEGORIES = {
    '休门': '休息、感情、贵人',
    '生门': '财运、生意',
    '开门': '工作事业、店面',
    '景门': '考试文昌'
}

GONG_DIRECTIONS = {
    1: '正北', 2: '西南', 3: '正东', 4: '东南',
    6: '西北', 7: '正西', 8: '东北', 9: '正南'
}

def get_smart_naji_action(tp, dp, shen, xing, men):
    base_acts = {
        '甲': ['穿衣打扮', '打理盆栽', '整理贵重物品'],
        '乙': ['摆弄花木', '手写日记/文章', '喝茶清修'],
        '丙': ['看电子屏幕', '吃烧烤', '戴眼镜首饰', '点亮灯光'],
        '丁': ['点香薰蜡烛', '使用小电子产品', '喝吸管饮料', '吃小甜点'],
        '戊': ['整理财务钱包', '吃肉食', '规划理财'],
        '己': ['整理坐垫杂物', '吃小零食', '静坐放松'],
        '庚': ['擦拭金属物件', '读经典著作', '做决断'],
        '辛': ['佩戴小首饰', '吃辛辣食物', '整理精细小物件'],
        '壬': ['喝矿泉水饮品', '走动跑动', '清洗物品'],
        '癸': ['喝茶水', '洗脸护肤', '洗手/清理污渍']
    }
    
    iconic_combos = {
        '戊丙': ['吃烤肉串(戊+丙)', '整理红色的财务钱包(戊+丙)', '规划大额理财(戊+丙)'],
        '丙戊': ['吃烤肉串(丙+戊)', '整理红色的财务钱包(丙+戊)', '阳光下吃肉食(丙+戊)'],
        '丁壬': ['喝温热茶水饮料(丁+壬)', '清洁电子产品(丁+壬)', '在暗光下点香(丁+壬)'],
        '壬丁': ['喝温热茶水饮料(壬+丁)', '清洁电子产品(壬+丁)'],
        '乙丙': ['给花草盆栽晒太阳(乙+丙)', '阅读漂亮的文章(乙+丙)', '看明亮的花朵(乙+丙)'],
        '丙乙': ['给花草盆栽晒太阳(丙+乙)', '阅读漂亮的文章(丙+乙)'],
        '戊辛': ['吃带辣味的肉食(戊+辛)', '整理零钱或首饰(戊+辛)'],
        '辛戊': ['吃带辣味的肉食(辛+戊)', '整理零钱或首饰(辛+戊)'],
        '乙戊': ['吃素食搭配肉食(乙+戊)', '在绿植旁整理钱包(乙+戊)'],
        '戊乙': ['吃素食搭配肉食(戊+乙)', '在绿植旁整理钱包(戊+乙)'],
        '庚丁': ['修理电子产品(庚+丁)', '擦拭发光或发热的物件(庚+丁)'],
        '丁庚': ['修理电子产品(丁+庚)', '擦拭发光或发热的物件(丁+庚)']
    }
    
    combo = f"{tp}{dp}"
    
    # 优先采用深度叠合的经典取象
    if combo in iconic_combos:
        acts = iconic_combos[combo][:3]
    else:
        # 无经典叠合时，各自取基础行为，自然并列，避免强行组合造成语病
        acts = []
        for a in base_acts.get(tp, [])[:2]:
            acts.append(a)
        for a in base_acts.get(dp, [])[:2]:
            if a not in acts:
                acts.append(a)
                
    # 尝试叠加极少量的辅助信息，仅限于极度自然的门星
    # 比如生门(生机/财运)，太阴(私密)
    aux_hint = ""
    if men == '休门': aux_hint = "（宜：休闲放松）"
    elif men == '生门': aux_hint = "（宜：求财/种植）"
    elif shen == '太阴': aux_hint = "（宜：保持私密/低调）"
    elif shen == '六合': aux_hint = "（宜：沟通/合作）"
    elif xing == '天心星' or xing == '天心': aux_hint = "（宜：处于核心位置）"
    
    return "、".join(acts) + aux_hint

def generate_html(result, target_dt=None, matter="", notes="", case_id=None):
    if not target_dt:
        target_dt = result['datetime']
    
    prev_dt = target_dt - timedelta(hours=2)
    next_dt = target_dt + timedelta(hours=2)
    prev_str = prev_dt.strftime("%Y-%m-%d %H:%M")
    next_str = next_dt.strftime("%Y-%m-%d %H:%M")
    dt_str_iso = target_dt.strftime("%Y-%m-%dT%H:%M")

    marks  = analyze_sihai(result)
    jg     = result['jiugong']
    dt     = result['datetime']
    xs     = result['xun_shou']
    rg     = result.get('rui_gong', 2)
    tq_gan = result.get('tianqin_gan', '')
    # 伏吟/反吟判断
    is_gan_fuyin = all(jg[g].get('tianpan') == jg[g].get('dipan') for g in [1,2,3,4,6,7,8,9])
    
    original_doors = {'休门': 1, '死门': 2, '伤门': 3, '杜门': 4, '开门': 6, '惊门': 7, '生门': 8, '景门': 9}
    opposite_doors = {'休门': 9, '死门': 8, '伤门': 7, '杜门': 6, '开门': 4, '惊门': 3, '生门': 2, '景门': 1}
    home_stars = { '天蓬': 1, '天芮': 2, '芮禽': 2, '天冲': 3, '天辅': 4, '天禽': 5, '天心': 6, '天柱': 7, '天任': 8, '天英': 9,
                   '天蓬星': 1, '天芮星': 2, '芮禽星': 2, '天冲星': 3, '天辅星': 4, '天禽星': 5, '天心星': 6, '天柱星': 7, '天任星': 8, '天英星': 9 }
    opposite_stars = { '天蓬': 9, '天芮': 8, '芮禽': 8, '天冲': 7, '天辅': 6, '天禽': 8, '天心': 4, '天柱': 3, '天任': 2, '天英': 1,
                       '天蓬星': 9, '天芮星': 8, '芮禽星': 8, '天冲星': 7, '天辅星': 6, '天禽星': 8, '天心星': 4, '天柱星': 3, '天任星': 2, '天英星': 1 }
    
    is_men_fuyin  = all(original_doors.get(jg[g].get('men','')) == g for g in [1,3,4,6,7,9])
    is_xing_fuyin = all(home_stars.get(jg[g].get('xing','')) == g for g in [1,3,4,6,7,9])
    is_men_fanyin = all(opposite_doors.get(jg[g].get('men','')) == g for g in [1,3,4,6,7,9])
    is_xing_fanyin = all(opposite_stars.get(jg[g].get('xing','')) == g for g in [1,3,4,6,7,9])
    
    is_bad_chart = is_gan_fuyin or is_men_fuyin or is_xing_fuyin or is_men_fanyin or is_xing_fanyin
    is_fuyin = is_gan_fuyin # 为兼容其他位置的显示

    # 五不遇时判断
    is_wubuyushi = (
        (result['day_gz'][0] == '甲' and result['hour_gz'][0] == '庚') or
        (result['day_gz'][0] == '乙' and result['hour_gz'][0] == '辛') or
        (result['day_gz'][0] == '丙' and result['hour_gz'][0] == '壬') or
        (result['day_gz'][0] == '丁' and result['hour_gz'][0] == '癸') or
        (result['day_gz'][0] == '戊' and result['hour_gz'][0] == '甲') or
        (result['day_gz'][0] == '己' and result['hour_gz'][0] == '乙') or
        (result['day_gz'][0] == '庚' and result['hour_gz'][0] == '丙') or
        (result['day_gz'][0] == '辛' and result['hour_gz'][0] == '丁') or
        (result['day_gz'][0] == '壬' and result['hour_gz'][0] == '戊') or
        (result['day_gz'][0] == '癸' and result['hour_gz'][0] == '己')
    )

    # 纳吉门位匹配 (已综合排除门迫、门制、本宫星门伏吟反吟)
    NAJI_VALID_DOORS = {
        1: ['开门'], 
        2: ['开门', '景门'], 
        3: ['休门', '景门'], 
        4: ['休门', '景门'], 
        6: ['休门', '生门'], 
        7: ['休门', '生门', '开门'], 
        8: ['开门', '景门'], 
        9: ['生门']
    }

    # 驿马计算器
    hz = result['hour_gz'][1]
    ma_map = {'申': (8, '寅'), '子': (8, '寅'), '辰': (8, '寅'),
              '寅': (2, '申'), '午': (2, '申'), '戌': (2, '申'),
              '巳': (6, '亥'), '酉': (6, '亥'), '丑': (6, '亥'),
              '亥': (4, '巳'), '卯': (4, '巳'), '未': (4, '巳')}
    ma_idx, ma_zhi = ma_map.get(hz, (None, ''))

    def get_style(tags):
        """基于标签着色"""
        if not tags: return ''
        has_rumu  = '入墓' in tags
        has_jixing = '击刑' in tags
        has_menpo = '门迫' in tags
        # 刑+墓 同时存在
        if has_jixing and has_rumu: return 'color:#0066cc;font-weight:bold'
        if has_menpo and has_rumu:  return 'color:#0066cc;font-weight:bold'
        if has_menpo:  return 'color:#cc0000;font-weight:bold'
        if has_jixing: return 'color:#8b00cc;font-weight:bold'
        if has_rumu:   return 'color:#cc8800;font-weight:bold'
        return ''

    def S(text, tags):
        st = get_style(tags)
        return f'<span style="{st}">{text}</span>' if st else text

    # 空亡标记
    ZHI_GONG = {'子':1,'丑':8,'寅':8,'卯':3,'辰':4,'巳':4,'午':9,'未':2,'申':2,'酉':7,'戌':6,'亥':6}
    kong_zhi = XUN_KONG.get(xs, '')
    kong_gong = {ZHI_GONG[z] for z in list(kong_zhi) if z in ZHI_GONG}

    layout = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
    cells  = ''

    # 宫位详细信息库
    PALACE_INFO_DB = {
        1: {"name": "坎1宫", "xt": "坤", "zhi": "子", "num": "1, 6", "sign": "坎", "nature": "水"},
        2: {"name": "坤2宫", "xt": "巽", "zhi": "未、申", "num": "2, 5, 8, 10", "sign": "坤", "nature": "地"},
        3: {"name": "震3宫", "xt": "离", "zhi": "卯", "num": "3, 8", "sign": "震", "nature": "雷"},
        4: {"name": "巽4宫", "xt": "兑", "zhi": "辰、巳", "num": "4, 5, 3, 8", "sign": "巽", "nature": "风"},
        5: {"name": "中5宫", "xt": "-", "zhi": "-", "num": "5, 10", "sign": "坤", "nature": "地"},
        6: {"name": "乾6宫", "xt": "艮", "zhi": "戌、亥", "num": "6, 1, 4, 9", "sign": "乾", "nature": "天"},
        7: {"name": "兑7宫", "xt": "坎", "zhi": "酉", "num": "7, 2, 4, 9", "sign": "兑", "nature": "泽"},
        8: {"name": "艮8宫", "xt": "震", "zhi": "丑、寅", "num": "8, 5, 7, 10", "sign": "艮", "nature": "山"},
        9: {"name": "离9宫", "xt": "乾", "zhi": "午", "num": "9, 3, 2, 7", "sign": "离", "nature": "火"}
    }
    
    HEXAGRAM_NAMES = {
        (6,6): "乾为天", (6,2): "天地否", (6,3): "天雷无妄", (6,4): "天风姤", (6,1): "天水讼", (6,9): "天火同人", (6,8): "天山遁", (6,7): "天泽履",
        (2,6): "地天泰", (2,2): "坤为地", (2,3): "地雷复", (2,4): "地风升", (2,1): "地水师", (2,9): "地火明夷", (2,8): "地山谦", (2,7): "地泽临",
        (3,6): "雷天大壮", (3,2): "雷地豫", (3,3): "震为雷", (3,4): "雷风恒", (3,1): "雷水解", (3,9): "雷火丰", (3,8): "雷山小过", (3,7): "雷泽归妹",
        (4,6): "风天小畜", (4,2): "风地观", (4,3): "风雷益", (4,4): "巽为风", (4,1): "风水涣", (4,9): "风火家人", (4,8): "风山渐", (4,7): "风泽中孚",
        (1,6): "水天需", (1,2): "水地比", (1,3): "水雷屯", (1,4): "水风井", (1,1): "坎为水", (1,9): "水火既济", (1,8): "水山蹇", (1,7): "水泽节",
        (9,6): "火天大有", (9,2): "火地晋", (9,3): "火雷噬嗑", (9,4): "火风鼎", (9,1): "火水未济", (9,9): "离为火", (9,8): "火山旅", (9,7): "火泽睽",
        (8,6): "山天大畜", (8,2): "山地剥", (8,3): "山雷颐", (8,4): "山风蛊", (8,1): "山水蒙", (8,9): "山火贲", (8,8): "艮为山", (8,7): "山泽损",
        (7,6): "泽天夬", (7,2): "泽地萃", (7,3): "泽雷随", (7,4): "泽风大过", (7,1): "泽水困", (7,9): "泽火革", (7,8): "泽山咸", (7,7): "兑为泽"
    }

    GATE_ORIGIN = {'休门': 1, '死门': 2, '伤门': 3, '杜门': 4, '芮': 2, '芮禽': 2, '天芮': 2, '开门': 6, '惊门': 7, '生门': 8, '景门': 9}

    palace_details_data = {}

    def analyze_geju_local(gn, g, is_fuyin, ma_idx):
        geju_list = []
        tp = g.get('tianpan', '')
        dps = g.get('dipans', [])
        dp = dps[0] if dps else ''
        men = g.get('men', '')
        xing = g.get('xing', '').replace('星', '')
        shen = g.get('shen', '')
        combo = f"{tp}{dp}"
        
        # 1. 冲格 (补充丁癸到天干冲)
        t_chong = ['戊庚', '庚戊', '乙辛', '辛乙', '丙壬', '壬丙', '丁癸', '癸丁']
        d_chong = ['戊辛', '辛戊', '庚癸', '癸庚', '壬己', '己壬']
        
        if combo in t_chong:
            geju_list.append(f"冲格：{tp}+{dp}")
        if combo in d_chong:
            geju_list.append(f"冲格：{tp}+{dp}")
        
        # 2. 动格
        dong_stems = ['乙辛', '丙庚', '戊庚', '庚戊', '庚壬', '庚癸', '癸壬']
        if combo in dong_stems:
            geju_list.append(f"动格：{tp}+{dp}")
        
        # 3. 刑格
        xing_stems = ['庚己', '己庚', '庚庚', '壬壬', '辛辛']
        if combo in xing_stems:
            geju_list.append(f"刑格：{tp}+{dp}")
        
        # 4. 合格
        he_stems = ['乙庚', '庚乙', '丙辛', '辛丙', '丁壬', '壬丁', '戊癸', '癸戊']
        if combo in he_stems:
            geju_list.append(f"合格：{tp}+{dp}")
        
        # 5. 墓格
        mu_stems = ['乙己', '乙壬', '丙己', '丁己', '戊己', '辛己', '戊壬', '癸己']
        if combo in mu_stems:
            geju_list.append(f"墓格：{tp}+{dp}")
            
        return list(dict.fromkeys(geju_list))

    for row in layout:
        for gn in row:
            g = jg[gn]
            mk = marks.get(gn, {k:[] for k in ['shen','xing','tianpan','dipan','men']})
            gan_tags = mk.get('gan_tags', {})
            circ = '<span class="circle">○</span>' if gn in kong_gong else ''
            
            if gn == 5:
                # 中五宫
                yin_v = g["yingan"]
                dp_v = g["dipan"]
                cells += f'''<div class="palace p5">
                  <div class="p-row p-mid"><div class="p-left"><div class="p-yingan-box"><span title="隐干">{yin_v}</span></div></div></div>
                  <div class="p-row p-bot" style="justify-content: flex-end;"><div class="p-right"><div class="p-stem-layer"><span class="p-stem" style="font-size:0.9rem; color:#666;">{dp_v}</span></div></div></div>
                </div>'''
                continue

            def render_stem_layer(items, states):
                stems_html = ""
                for i, (s, t) in enumerate(items):
                    st = states[i] if i < len(states) else ""
                    cs_html = f'<span class="cs-label">{st}</span>' if st else ""
                    stems_html += f'<div class="stem-group"><span class="p-stem" style="{get_style(t)};">{cs_html}{s}</span></div>'
                return f'<div class="p-stem-layer">{stems_html}</div>'

            # 构建天盘干列表及长生状态
            tp_list = [(g['tianpan'], gan_tags.get(g['tianpan'], []))]
            tp_cs_list = [g.get('cs_tianpan', '')]
            if gn == rg and tq_gan and tq_gan != g['tianpan']:
                tp_list.insert(0, (tq_gan, gan_tags.get(tq_gan, [])))
                tp_cs_list.insert(0, g.get('cs_tianqin', ''))
            
            # 构建地盘干列表及长生状态
            dp_list = [(d, gan_tags.get(d, [])) for d in g['dipans'][::-1]]
            dp_cs_list = [g.get('cs_dipan', '')] * len(dp_list)

            # 驿马图标 (宫位右侧顶部)
            ma_html = f'<span class="ma-ext">🐎</span>' if gn == ma_idx else ''
            
            # 引干渲染 (移除引干的四害和长生状态)
            yin_list = [f'<span title="隐干">{ygan}</span>' for ygan in g.get('yingans', [])]
            yin_h = f'<div class="p-yingan-box">{"".join(yin_list)}</div>'

            men_tags = [t for t in mk.get('men', []) if t != '符使']

            naji_badge = ""
            if not is_wubuyushi and not is_bad_chart and gn != 5:
                men = g.get('men', '')
                if men in NAJI_VALID_DOORS.get(gn, []):
                    has_sihai = False
                    if '门迫' in mk.get('men', []): has_sihai = True
                    for tp_gan in [s for s, _ in tp_list]:
                        if '击刑' in gan_tags.get(tp_gan, []) or '入墓' in gan_tags.get(tp_gan, []): has_sihai = True
                    for dp_gan in [s for s, _ in dp_list]:
                        if '击刑' in gan_tags.get(dp_gan, []) or '入墓' in gan_tags.get(dp_gan, []): has_sihai = True
                    if gn in kong_gong: has_sihai = True
                    
                    bg_gan = [s for s, _ in tp_list] + [s for s, _ in dp_list]
                    has_geng = ('庚' in bg_gan)
                    is_baihu = (g.get('shen') == '白虎')
                    is_bad_xing = (g.get('xing') in ['天蓬', '天芮', '天蓬星', '天芮星', '芮禽', '芮禽星'])
                    is_bad_jingmen = (men == '景门' and g.get('shen') in ['玄武', '九地'])
                    
                    if not (has_sihai or has_geng or is_baihu or is_bad_xing or is_bad_jingmen):
                        elements = bg_gan + [g.get('shen'), g.get('xing'), g.get('men')]
                        elements = [str(el).replace('星', '') if str(el).startswith('天') and len(str(el))==3 else el for el in elements if el]
                        
                        nj_data = []
                        color_tp = NAJI_COLORS.get(tp_list[0][0], '缺')
                        color_dp = NAJI_COLORS.get(dp_list[0][0], '缺')
                        
                        smart_act = get_smart_naji_action(tp_list[0][0], dp_list[0][0], g.get('shen'), g.get('xing'), g.get('men'))
                        
                        nj_data.append(f"<div style='margin-bottom:8px;border-bottom:1px dashed #eee;padding-bottom:5px'><b>【综合建议行为】</b><br><span style='color:#cd5c5c; font-weight:bold;'>{smart_act}</span></div>")
                        nj_data.append(f"<div style='margin-bottom:8px;border-bottom:1px dashed #eee;padding-bottom:5px'><b>【天地盘颜色指示】</b><br><span style='color:#666'>{color_tp}色(上) - {color_dp}色(下)</span></div>")

                        for el in set(elements):
                            wx = NAJI_WUXIANG.get(el)
                            xw = NAJI_XINGWEI.get(el)
                            if wx or xw:
                                content = f"<div style='margin-bottom:8px;border-bottom:1px dashed #eee;padding-bottom:5px'><b>【{el}】</b><br>"
                                if wx: content += f"<span style='color:#666'>物象：</span>{wx}<br>"
                                if xw: content += f"<span style='color:#666'>行为：</span>{xw}<br>"
                                content += "</div>"
                                nj_data.append(content)
                                
                        if nj_data:
                            full_html = "<h4 style='margin-top:0'>宫位纳吉方案</h4>" + "".join(nj_data)
                            nj_b64 = base64.b64encode(full_html.encode('utf-8')).decode('utf-8')
                            naji_badge = f"""<div class="naji-badge" style="display:none" onclick="showNaji(event, '{nj_b64}')">纳吉</div>"""

            # 准备宫位格局详情数据
            # 重新获取核心干，确保判定准确
            tp_gan_core = tp_list[0][0] if tp_list else ''
            dp_gan_core = dp_list[0][0] if dp_list else ''
            
            # 手动执行一次精确判定，防止缓存或作用域问题
            local_geju = []
            combo_core = f"{tp_gan_core}{dp_gan_core}"
            t_chong_list = ['戊庚', '庚戊', '乙辛', '辛乙', '丙壬', '壬丙', '丁癸', '癸丁']
            d_chong_list = ['戊辛', '辛戊', '庚癸', '癸庚', '壬己', '己壬']
            dong_stems_list = ['乙辛', '丙庚', '戊庚', '庚戊', '庚壬', '庚癸', '癸壬']
            xing_stems_list = ['庚己', '己庚', '庚庚', '壬壬', '辛辛']
            he_stems_list = ['乙庚', '庚乙', '丙辛', '辛丙', '丁壬', '壬丁', '戊癸', '癸戊']
            mu_stems_list = ['乙己', '乙壬', '丙己', '丁己', '戊己', '辛己', '戊壬', '癸己']
            
            if combo_core in t_chong_list: local_geju.append(f"冲格：{tp_gan_core}+{dp_gan_core}")
            if combo_core in d_chong_list: local_geju.append(f"冲格：{tp_gan_core}+{dp_gan_core}")
            if combo_core in dong_stems_list: local_geju.append(f"动格：{tp_gan_core}+{dp_gan_core}")
            if combo_core in xing_stems_list: local_geju.append(f"刑格：{tp_gan_core}+{dp_gan_core}")
            if combo_core in he_stems_list: local_geju.append(f"合格：{tp_gan_core}+{dp_gan_core}")
            if combo_core in mu_stems_list: local_geju.append(f"墓格：{tp_gan_core}+{dp_gan_core}")
            
            pi = PALACE_INFO_DB.get(gn, {})
            desc = [f"<div style='font-weight:bold; font-size:1.1rem; border-bottom:1px solid #eee; padding-bottom:8px; margin-bottom:12px; color:#b8905b;'>{pi['name']}</div>"]
            
            # 门宫卦
            m_name = g.get('men', '')
            if m_name in GATE_ORIGIN:
                top_gn = GATE_ORIGIN[m_name]
                gua_name = HEXAGRAM_NAMES.get((top_gn, gn), "未知卦")
                desc.append(f"<div style='margin-bottom:10px;'><b>门宫卦</b>：<span style='color:#b8905b'>{gua_name}</span></div>")

            # 最终展示格局
            final_geju = list(dict.fromkeys(local_geju))
            if final_geju:
                desc.append("<div style='margin-top:10px; padding-top:10px; border-top:1px dashed #eee;'>")
                desc.append("<b style='display:block; margin-bottom:5px;'>【格局提示】</b>")
                for gj in final_geju: desc.append(f"<div style='color:#d32f2f; margin: 3px 0;'>· {gj}</div>")
                desc.append("</div>")
            
            palace_details_data[gn] = "".join(desc)

            cells += f'''
<div class="palace-wrapper">
  {naji_badge}
  <div class="palace" onclick="showPalaceGeju({gn})">
    <div class="p-row p-top">
      <div class="p-left"><span class="p-shen">{circ}{g['shen']}</span></div>
      <div class="p-right">{ma_html}</div>
    </div>
    <div class="p-row p-mid">
      <div class="p-left">{yin_h}<span class="p-xing">{g['xing']}</span></div>
      <div class="p-right">{render_stem_layer(tp_list, tp_cs_list)}</div>
    </div>
    <div class="p-row p-bot">
      <div class="p-left"><span class="p-men">{S(g['men'], men_tags)}</span></div>
      <div class="p-right">{render_stem_layer(dp_list, dp_cs_list)}</div>
    </div>
  </div>
</div>'''
    dt_str = target_dt.strftime("%Y年%m月%d日 %H时%M分")
    bazi_gz = [f"{g[0]}{g[1]}" for g in [result['year_gz'], result['month_gz'], result['day_gz'], result['hour_gz']]]
    ju_str = f"{result['dun_type']}{result['ju_shu']}局（{result['san_yuan']}）"
    if is_fuyin: ju_str += ' <span class="badge-fuyin" style="color:red;font-size:0.8rem">伏吟</span>'

    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>奇门遁甲 - {dt_str}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Kaiti+7&display=swap');
        body {{ background:#f5f2ed; font-family:"Microsoft YaHei",sans-serif; display:flex; flex-direction:column; align-items:center; padding:20px; margin:0; }}
        .header {{ text-align:center; margin-bottom:15px; color:#333; }}
        .header h1 {{ margin:0; font-size:1.4rem; letter-spacing:4px; font-weight:normal; }}
        .main-info {{ background:#fff; border:1px solid #dcd3d1; padding:15px; width:600px; margin-bottom:5px; box-sizing:border-box; }}
        .info-r {{ display:flex; justify-content:space-between; margin-bottom:8px; border-bottom:1px solid #f9f6f2; padding-bottom:4px; font-size:0.95rem; align-items:center; }}
        .lbl {{ color:#777; width:65px; display:inline-block; }} .val {{ color:#333; flex-grow:1; text-align:left; }}
        .gv {{ color:#006621; }} .kv {{ color:#c02; }}
        
        .bazi-grid {{ display:flex; gap:10px; margin: 10px 0; border-top:1px solid #ddd; border-bottom:1px solid #ddd; padding:10px 0; text-align:center; }}
        .bazi-col {{ flex:1; display:flex; flex-direction:column; }}
        .bazi-lbl {{ color:#b8905b; font-size:0.85rem; margin-bottom:5px; }}
        .bazi-val {{ font-size:1.6rem; color:#d32f2f; font-weight:bold; }}
        .bazi-val.green {{ color:#2e7d32; }}
        
        .grid {{
            display: grid; grid-template-columns: repeat(3, 195px); grid-template-rows: repeat(3, 140px);
            background: #333; border: 2.5px solid #333; gap: 1.5px;
        }}
        .palace-wrapper {{ position: relative; background: #fff; }}
        .palace {{ height:100%; padding: 8px; display: flex; flex-direction: column; box-sizing: border-box; }}
        .p5 {{ background: #fff; justify-content: center; align-items: center; border:1px solid #eee; }}

        .action-bar button {{ padding: 6px 12px; font-size: 0.95rem; border: none; background: #0088cc; color: white; border-radius: 4px; cursor: pointer; }}
        .action-bar button:hover {{ background: #006699; }}
        .action-bar .btn-secondary {{ background: #28a745; }}
        .action-bar .btn-secondary:hover {{ background: #218838; }}
        
        /* Modal Styles */
        .modal {{ display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); }}
        .modal-content {{ background-color: #fefefe; margin: 10% auto; padding: 20px; border: 1px solid #888; width: 600px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); max-height: 80vh; overflow-y: auto; }}
        .close {{ color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer; }}
        .close:hover, .close:focus {{ color: black; text-decoration: none; }}
        .form-group {{ margin-bottom: 15px; }}
        .form-group label {{ display: block; margin-bottom: 5px; color: #333; }}
        .form-group input, .form-group textarea {{ width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }}
        
        /* Bottom Navigation Bar */
        .bottom-nav {{
            position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%);
            width: 92%; max-width: 500px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(184, 144, 91, 0.2);
            border-radius: 40px;
            display: flex; justify-content: space-around;
            padding: 10px 10px; z-index: 1000;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .nav-item {{
            display: flex; flex-direction: column; align-items: center;
            color: #8b7355; font-size: 0.7rem; cursor: pointer; flex: 1;
            transition: all 0.3s; padding: 5px 0; border-radius: 20px;
        }}
        .nav-icon {{ font-size: 1.4rem; margin-bottom: 2px; }}
        .nav-item:hover {{ background: rgba(0, 191, 165, 0.05); color: #00bfa5; }}
        .nav-item.active {{ color: #00bfa5; }}
        
        /* Matter Header */
        .matter-header {{
            width: 600px; padding: 15px 20px; background: #fff; 
            border: 1px solid #dcd3d1; border-bottom: none; 
            border-radius: 12px 12px 0 0; box-sizing: border-box;
            box-shadow: 0 -5px 15px rgba(0,0,0,0.02);
        }}
        .matter-top {{ display: flex; align-items: center; margin-bottom: 8px; }}
        .matter-label {{ color: #b8905b; margin-right: 12px; font-weight: bold; font-size: 1.1rem; border-left: 4px solid #b8905b; padding-left: 8px; line-height: 1; }}
        .matter-input {{ 
            border: none; flex-grow: 1; outline: none; font-size: 1.2rem; 
            padding: 5px 0; color: #333; font-weight: 500;
            background: transparent; resize: none; font-family: inherit;
            line-height: 1.4; overflow: hidden; height: auto;
        }}
        .matter-input::placeholder {{ color: #ccc; font-weight: normal; font-size: 1rem; }}

        .case-item {{ border: 1px solid #eee; padding: 10px; margin-bottom: 10px; border-radius: 4px; background: #fafafa; cursor: pointer; position: relative; }}
        .case-item:hover {{ background: #f0f0f0; border-color:#ccc; }}
        .case-title {{ font-weight: bold; color: #0066cc; font-size: 1.1em; }}
        .case-meta {{ font-size: 0.85em; color: #666; margin-top: 5px; }}
        .case-del {{ position: absolute; right: 10px; top: 10px; color: #cc0000; font-weight:bold; padding:4px 8px; border-radius: 4px; }}
        .case-del:hover {{ background: #fee; }}
.naji-badge {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(212, 237, 218, 0.95);
    color: #155724;
    border: 2px solid #28a745;
    border-radius: 8px;
    padding: 6px 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    font-weight: bold;
    cursor: pointer;
    z-index: 20;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    animation: pulse 2s infinite;
    backdrop-filter: blur(2px);
}}
@keyframes pulse {{
    0% {{ transform: translate(-50%, -50%) scale(1); box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.6); }}
    70% {{ transform: translate(-50%, -50%) scale(1.1); box-shadow: 0 0 0 10px rgba(40, 167, 69, 0); }}
    100% {{ transform: translate(-50%, -50%) scale(1); box-shadow: 0 0 0 0 rgba(40, 167, 69, 0); }}
}}
.naji-modal-content {{
    background-color: #fcfcfc;
    margin: 10% auto;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    width: 60%;
    max-width: 400px;
    max-height: 70vh;
    overflow-y: auto;
    font-size: 0.95rem;
    line-height: 1.5;
}}
        .ma-ext {{ font-size: 1.1rem; color:#00bfa5; }}

        .p-row {{ display: flex; justify-content: space-between; align-items: center; min-height: 33.33%; }}
        .p-mid {{ }}
        .p-left {{ display: flex; align-items: center; white-space: nowrap; }}
        .p-right {{ display: flex; flex-direction: column; align-items: flex-end; justify-content: center; }}
        
        .naji-item {{
            padding: 10px;
            border-bottom: 1px solid #eee;
            margin-bottom: 10px;
            background: #f9fbf9;
            border-radius: 4px;
        }}
        .naji-item:hover {{ background: #f0f7f0; }}
        .naji-time {{ font-weight: bold; color: #28a745; margin-bottom: 5px; display: block; }}
        .naji-details {{ font-size: 0.9rem; color: #555; }}
        .ical-btn {{
            display: inline-block;
            margin-top: 5px;
            padding: 4px 10px;
            background: #28a745;
            color: white;
            border-radius: 4px;
            font-size: 0.8rem;
            cursor: pointer;
            text-decoration: none;
        }}
        
        .p-stem-layer {{ display: flex; justify-content: flex-end; align-items: baseline; width: 100%; }}
        .p-shen {{ font-size: 1.1rem; color: #333; }}
        .p-yingan-box {{ display: flex; align-items: center; margin-right: 2px; position:relative; }}
        .p-yingan-box span {{ color: #aaa; font-size: 0.9rem; font-family: "Kaiti", serif; }}
        .p-xing {{ font-family: "Kaiti", serif; font-size: 1.15rem; color: #333; }}
        .p-men {{ font-family: "Kaiti", serif; font-size: 1.15rem; color: #333; }}
        .p-stem {{ font-family: "STKaiti", "Kaiti", serif; font-size: 1.5rem; line-height: 1; white-space: nowrap; position: relative; font-weight:bold; }}
        .circle {{ color: #1a9c3e; margin-right: 2px; }}

        .legend {{ 
            font-size: 0.85rem; color: #888; 
            margin: 20px 0 40px 0; text-align: center; 
            border-top: 1px solid #eee; padding-top: 15px; 
            width: 600px; 
        }}
        .leg {{ display: inline-block; margin: 0 8px; }}

        /* 长生状态 样式 */
        .stem-group {{ display: flex; flex-direction: column; align-items: center; position: relative; margin: 0 2px; }}
        .cs-label {{ display: none; position: absolute; bottom: 100%; font-size: 0.65rem; color: #888; white-space: nowrap; font-family: sans-serif; font-weight: normal; margin-bottom: 4px; letter-spacing: 0; line-height: 1; }}
        body.show-cs .cs-label {{ display: block; }}

        /* 底部按钮栏 */
        .action-bar {{ margin-top: 10px; display: flex; gap: 8px; width: 600px; justify-content: center; }}
        .action-btn {{ flex: 1; padding: 12px 0; font-size: 0.95rem; background: #00bfa5; color: white; border: none; border-radius: 4px; cursor: pointer; text-align: center; font-weight:bold; transition: background 0.2s; user-select:none; max-width: 150px; margin: 0 5px;}}
        .action-btn:hover {{ background: #00a08a; }}
        .action-btn.active {{ background: #00a08a; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2); }}
        
        /* 日期选择器 */
        .dt-input {{ font-family:inherit; font-size:0.95rem; border:1px solid #ccc; border-radius:4px; padding:3px 6px; margin-right:6px; outline:none; }}
        .dt-btn {{ background:#00bfa5; color:white; border:none; border-radius:4px; padding:4px 12px; cursor:pointer; font-weight:bold; font-size:0.9rem; transition: background 0.2s; }}
        .dt-btn:hover {{ background:#00a08a; }}

        /* Toast Styles */
        .toast {{ 
            visibility: hidden; min-width: 250px; background-color: rgba(50, 50, 50, 0.9); 
            color: #fff; text-align: center; border-radius: 12px; padding: 16px; 
            position: fixed; z-index: 10001; left: 50%; top: 50%; 
            transform: translate(-50%, -50%); font-size: 1rem; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.2); backdrop-filter: blur(5px);
            transition: opacity 0.3s, visibility 0.3s; opacity: 0;
        }}
        .toast.show {{ visibility: visible; opacity: 1; }}

        /* Share Modal Specifics */
        #shareModal .modal-content {{
            width: 90%;
            max-width: 450px;
            padding: 0;
            background: #f8f8f8;
            overflow: hidden;
            border-radius: 12px;
        }}
        .share-card-container {{
            padding: 15px;
            text-align: center;
        }}
        #share-image-result {{
            width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            display: block;
            margin: 0 auto;
        }}
        .share-hint {{
            margin-top: 15px;
            color: #666;
            font-size: 0.9rem;
            padding-bottom: 15px;
        }}
        /* Ensure specific elements are hidden during capture */
        .no-capture {{ visibility: hidden !important; }}
    </style>
    <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
</head>
<body>
<div class="header"><h1>奇门遁甲</h1></div>

<div class="matter-header">
    <div class="matter-top">
        <span class="matter-label">事项</span>
        <textarea id="main-matter" class="matter-input" rows="1" placeholder="输入求测事项..." oninput="autoResize(this); syncMatter(this.value)" onchange="updateSaveStatus()">{matter}</textarea>
    </div>
</div>

<div class="main-info" style="border-radius: 0 0 12px 12px; border-top: 1px solid #f9f6f2; margin-top: -1px;">
  <div class="info-r" style="border-bottom: none; margin-bottom: 5px;">
      <span class="val" style="color:#b8905b; font-weight:bold; letter-spacing:1px;">转盘奇门 · 寄坤 · 置闰 · 值使起</span>
  </div>
  <div class="info-r" style="padding: 2px 0;">
      <span class="lbl">日期</span>
      <span class="val" style="display:flex; align-items:center;">
          <input type="datetime-local" id="custom-dt" class="dt-input" value="{dt_str_iso}">
          <button class="dt-btn" onclick="jumpCustom()">排盘</button>
          <button class="dt-btn" style="background:#6c757d;margin-left:5px;" onclick="window.location.href='/'">现在</button>
      </span>
  </div>
  <div class="bazi-grid">
     <div class="bazi-col"><div class="bazi-lbl">年柱</div><div class="bazi-val">{bazi_gz[0]}</div></div>
     <div class="bazi-col"><div class="bazi-lbl">月柱</div><div class="bazi-val green">{bazi_gz[1]}</div></div>
     <div class="bazi-col"><div class="bazi-lbl">日柱</div><div class="bazi-val green">{bazi_gz[2]}</div></div>
     <div class="bazi-col"><div class="bazi-lbl">时柱</div><div class="bazi-val">{bazi_gz[3]}</div></div>
  </div>
  <div class="info-r"><span class="lbl">节气</span><span class="val">{result['jieqi']} {result["jieqi_date"].strftime("%Y.%m.%d %H:%M")}</span></div>
  <div class="info-r">
      <span class="lbl">局数</span><span class="val" style="color:#666">{result['dun_type']}{result['ju_shu']}</span>
      <span class="lbl">旬首</span><span class="val" style="color:#666">{xs}</span>
  </div>
  <div class="info-r">
      <span class="lbl">值符</span><span class="val" style="color:#b8905b">{result["zhifu"]}</span>
      <span class="lbl">值使</span><span class="val" style="color:#b8905b">{result["zhishi"]}</span>
  </div>
  <div class="info-r" style="border-bottom:none; margin-bottom:0;">
      <span class="lbl">空亡</span><span class="val kv">{kong_zhi}</span>
      <span class="lbl">马星</span><span class="val kv">{ma_zhi}</span>
  </div>
</div>
<div class="grid">{cells}</div>

<div class="legend">
  <span>颜色说明：</span>
  <span class="leg" style="color:#00bfa5">符使</span>
  <span class="leg" style="color:#cc8800">入墓</span>
  <span class="leg" style="color:#8b00cc">击刑</span>
  <span class="leg" style="color:#cc0000">门迫</span>
  <span class="leg" style="color:#0066cc">刑+墓</span>
</div>

<div class="action-bar" style="margin-bottom: 120px;">
    <div class="action-btn" onclick="jmp('{prev_str}')">◀ 上一局</div>
    <div class="action-btn" id="btn-cs" onclick="toggleCS()">长生状态</div>
    <div class="action-btn" onclick="jmp('{next_str}')">下一局 ▶</div>
</div>

<div class="bottom-nav">
    <div class="nav-item" onclick="window.location.href='/'">
        <span class="nav-icon">🏠</span>
        <span>首页</span>
    </div>
    <div class="nav-item" onclick="shareChart()">
        <span class="nav-icon">📤</span>
        <span>分享</span>
    </div>
    <div class="nav-item" onclick="openNoteModal()">
        <span class="nav-icon">📝</span>
        <span>笔记</span>
    </div>
    <div class="nav-item" onclick="openFilterModal()">
        <span class="nav-icon">📅</span>
        <span>推演</span>
    </div>
    <div class="nav-item" onclick="openListModal()">
        <span class="nav-icon">📁</span>
        <span>档案</span>
    </div>
    <div class="nav-item" id="nav-naji" onclick="toggleNaji()">
        <span class="nav-icon">✨</span>
        <span>纳吉</span>
    </div>
</div>

<div id="toast" class="toast"></div>

<!-- Note Modal -->
<div id="noteModal" class="modal">
  <div class="modal-content">
    <span class="close" onclick="closeNoteModal()">&times;</span>
    <h2 style="margin-top:0">笔记内容</h2>
    <div id="note-reminder" style="text-align:center; color:#999; margin-bottom:10px; font-size:0.85rem;">您还没有笔记内容噢<br>随意添加文字、图片，让笔记更方便！</div>
    <div class="form-group">
      <label style="color:#b8905b; font-weight:bold;">求测事项</label>
      <textarea id="modal-matter" class="matter-input" rows="1" placeholder="请输入事项内容" style="border:none; border-bottom:1px solid #eee; padding:10px 0; font-size:1.1rem; border-radius:0; width:100%;" oninput="autoResize(this); syncMatter(this.value)"></textarea>
    </div>
    <div class="form-group">
      <label style="color:#b8905b; font-weight:bold;">笔记内容</label>
      <textarea id="main-note" rows="10" placeholder="请输入笔记内容" style="border:none; border-top:1px solid #eee; padding-top:10px;" oninput="updateSaveStatus()">{notes}</textarea>
    </div>
    <div style="text-align:right; margin-top:20px;">
      <button onclick="handleSaveAction(); closeNoteModal();" style="padding:10px 24px; background:#00bfa5; color:white; border:none; border-radius:4px; font-size:1em; cursor:pointer; font-weight:bold; box-shadow:0 2px 4px rgba(0,0,0,0.1)">确定保存</button>
    </div>
  </div>
</div>

<div id="promptModal" class="modal">
  <div class="modal-content" style="width: 320px; border-radius: 12px; padding: 0; overflow: hidden; margin-top: 25vh;">
    <div style="padding: 20px 15px;">
        <div style="text-align:center; font-weight:bold; margin-bottom:15px; font-size:1.1rem;">保存案例</div>
        <input type="text" id="prompt-matter" placeholder="请输入事项内容" style="width:100%; padding:10px; border:1px solid #eee; border-radius:6px; box-sizing:border-box; outline:none; background:#f9f9f9;">
    </div>
    <div style="display:flex; border-top: 1px solid #eee;">
       <button onclick="closePrompt()" style="flex:1; padding:12px; background:#fff; border:none; color:#666; cursor:pointer; font-size:1rem; border-right:1px solid #eee;">取消</button>
       <button onclick="confirmPrompt()" style="flex:1; padding:12px; background:#fff; border:none; color:#007aff; cursor:pointer; font-size:1rem; font-weight:bold;">确定</button>
    </div>
  </div>
</div>

<!-- Naji Modal -->
<div id="najiModal" class="modal" style="z-index:9999;">
    <div class="naji-modal-content">
        <span class="close" onclick="closeNajiModal()">&times;</span>
        <div id="naji-content-box"></div>
    </div>
</div>
<!-- Share Modal -->
<div id="shareModal" class="modal">
  <div class="modal-content">
    <span class="close" onclick="closeShareModal()" style="position:absolute; right:15px; top:10px; z-index:100;">&times;</span>
    <div class="share-card-container">
        <div id="share-loading" style="padding: 40px 0;">
            <div style="font-size: 1.5rem; margin-bottom: 10px;">生成分享图中...</div>
            <div style="color: #999;">请稍候</div>
        </div>
        <img id="share-image-result" style="display:none;">
        <div class="share-hint" id="share-hint" style="display:none;">长按上方图片或点击保存至相册</div>
    </div>
  </div>
</div>
  </div>
</div>

<!-- Palace Detail Modal -->
<div id="gejuModal" class="modal" style="z-index:9998;">
  <div class="modal-content" style="max-width:420px; border-radius:12px; border:2px solid #b8905b;">
    <span class="close" onclick="closeGejuModal()">&times;</span>
    <h3 style="margin-top:0; color:#b8905b; border-bottom:1px solid #eee; padding-bottom:10px;">宫位详析</h3>
    <div id="geju-content" style="line-height:1.6; font-size:1.05rem;"></div>
  </div>
</div>

<!-- Filter Modal -->
<div id="filterModal" class="modal">
  <div class="modal-content" style="width:500px">
    <span class="close" onclick="closeFilterModal()">&times;</span>
    <h2 style="margin-top:0">纳吉日历筛选</h2>
    <div class="form-group">
      <label>开始日期</label>
      <input type="date" id="filter-start" value="{datetime.now().strftime('%Y-%m-%d')}">
    </div>
    <div class="form-group">
      <label>结束日期 (含)</label>
      <input type="date" id="filter-end" value="{(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}">
    </div>
    <div style="text-align:right">
      <button onclick="startFilter()" id="filter-run-btn" style="padding:10px 20px; background:#28a745; color:white; border:none; border-radius:4px; cursor:pointer; font-weight:bold;">开始扫描纳吉时段</button>
    <button onclick="downloadAllIcal()" id="download-all-btn" style="display:none; padding:10px 20px; background:#8b4513; color:white; border:none; border-radius:4px; cursor:pointer; font-weight:bold; margin-left:10px;">批量加入日历</button>
    </div>
    <hr style="margin:20px 0; border:0; border-top:1px solid #eee">
    <div id="filter-results" style="max-height:400px; overflow-y:auto"></div>
  </div>
</div>

<!-- Case List Modal -->
<div id="listModal" class="modal" style="z-index:100000; background: rgba(0,0,0,0.5);">
  <div class="modal-content" style="width:700px; border: 2px solid #00bfa5; border-radius:12px; position:relative; margin: 10vh auto;">
    <span class="close" onclick="closeListModal()" style="position:absolute; right:15px; top:10px;">&times;</span>
    <h2 style="margin-top:0; color:#00bfa5; border-bottom:1px solid #eee; padding-bottom:10px;">案例记录中心</h2>
    <div id="case-list-container" style="max-height:65vh; overflow-y:auto; padding:5px;">
       <div style="text-align:center;color:#666;padding:30px;">正在努力加载档案库...</div>
    </div>
  </div>
</div>

<script>
// ---------- UI Logic ----------
function toggleCS() {{
    const b = document.body;
    const btn = document.getElementById('btn-cs');
    b.classList.toggle('show-cs');
    btn.classList.toggle('active');
}}

function jumpCustom() {{
    const dtVal = document.getElementById('custom-dt').value;
    if (dtVal) {{
        const formatted = dtVal.replace('T', ' ');
        jmp(formatted);
    }} else {{
        alert("请输入正确的时间");
    }}
}}

function jmp(target_dt, show_naji=false, id=null) {{
    const loc = window.location.href;
    if (loc.startsWith("file:")) {{
        let cmd = 'python3 scripts/qimen_web.py "' + target_dt + '"';
        let msg = "由于您当前在本地 file 模式下预览，页面无法自动跳转。\\n\\n如需查看，请复制以下命令在终端执行：\\n\\n" + cmd;
        prompt(msg, cmd);
    }} else {{
        let suffix = "";
        if (show_naji) suffix = "&naji=1";
        let qs = id ? ("?id=" + id) : ("?dt=" + encodeURIComponent(target_dt));
        window.location.search = qs + suffix;
    }}
}}

// ---------- Case Management Logic ----------
const currentChartInfo = {{
    id: {"null" if case_id is None else case_id},
    chart_time: "{dt_str_iso}".replace('T', ' '),
    bazi: "{bazi_gz[0]} {bazi_gz[1]} {bazi_gz[2]} {bazi_gz[3]}",
    ju_shu: "{result['dun_type']}{result['ju_shu']}局"
}};

const palaceGejuData = {json.dumps(palace_details_data)};

function showPalaceGeju(gn) {{
    const content = palaceGejuData[gn];
    if (content) {{
        document.getElementById('geju-content').innerHTML = content;
        document.getElementById('gejuModal').style.display = 'block';
    }}
}}
function closeGejuModal() {{ document.getElementById('gejuModal').style.display = 'none'; }}

function autoResize(el) {{
    el.style.height = 'auto';
    el.style.height = el.scrollHeight + 'px';
}}

function updateSaveStatus() {{
    const reminder = document.getElementById('note-reminder');
    if (reminder) {{
        const hasContent = document.getElementById('main-note').value.trim() !== "" || 
                           document.getElementById('modal-matter').value.trim() !== "";
        reminder.style.display = hasContent ? 'none' : 'block';
    }}
}}

function syncMatter(val) {{
    const mainMatter = document.getElementById('main-matter');
    const modalMatter = document.getElementById('modal-matter');
    if (mainMatter) mainMatter.value = val;
    if (modalMatter) modalMatter.value = val;
    updateSaveStatus();
}}

function handleSaveAction() {{
    const matterInput = document.getElementById('main-matter');
    const matter = matterInput ? matterInput.value.trim() : "";
    if (!matter && !currentChartInfo.id) {{
        document.getElementById('promptModal').style.display = 'block';
    }} else {{
        submitSaveCase();
    }}
}}

function closePrompt() {{ document.getElementById('promptModal').style.display = 'none'; }}
function confirmPrompt() {{
    const val = document.getElementById('prompt-matter').value;
    if (val) {{
        document.getElementById('main-matter').value = val;
        closePrompt();
        submitSaveCase();
    }} else {{
        alert('请输入内容');
    }}
}}

function openNoteModal() {{ 
    // Open modal and sync current matter to modal input
    const matterVal = document.getElementById('main-matter').value;
    const modalInput = document.getElementById('modal-matter');
    modalInput.value = matterVal;
    document.getElementById('noteModal').style.display = 'block'; 
    autoResize(modalInput);
    updateSaveStatus();
}}
function closeNoteModal() {{ document.getElementById('noteModal').style.display = 'none'; }}

function openShareModal() {{ document.getElementById('shareModal').style.display = 'block'; }}
function closeShareModal() {{ document.getElementById('shareModal').style.display = 'none'; }}

function shareChart() {{
    openShareModal();
    const loading = document.getElementById('share-loading');
    const resultImg = document.getElementById('share-image-result');
    const hint = document.getElementById('share-hint');
    
    loading.style.display = 'block';
    resultImg.style.display = 'none';
    hint.style.display = 'none';

    // Temporary hide elements we don't want in the screenshot
    const nav = document.querySelector('.bottom-nav');
    const actionBar = document.querySelector('.action-bar');
    if (nav) nav.classList.add('no-capture');
    if (actionBar) actionBar.classList.add('no-capture');

    // Use a slight delay to ensure UI is ready
    setTimeout(() => {{
        html2canvas(document.body, {{
            useCORS: true,
            scale: 2, // Higher quality
            backgroundColor: "#f5f2ed",
            ignoreElements: (el) => el.classList.contains('no-capture') || el.classList.contains('modal')
        }}).then(canvas => {{
            const dataUrl = canvas.toDataURL("image/png");
            resultImg.src = dataUrl;
            loading.style.display = 'none';
            resultImg.style.display = 'block';
            hint.style.display = 'block';
            
            // Restore hidden elements
            if (nav) nav.classList.remove('no-capture');
            if (actionBar) actionBar.classList.remove('no-capture');
        }}).catch(err => {{
            console.error("Capture failed:", err);
            loading.innerText = "生成失败，请刷新重试";
            if (nav) nav.classList.remove('no-capture');
            if (actionBar) actionBar.classList.remove('no-capture');
        }});
    }}, 100);
}}

function openSaveModal() {{ document.getElementById('saveModal').style.display = 'block'; }}
function closeSaveModal() {{ document.getElementById('saveModal').style.display = 'none'; }}
function openListModal() {{ 
    document.getElementById('listModal').style.display = 'block'; 
    loadCases();
}}
function closeListModal() {{ document.getElementById('listModal').style.display = 'none'; }}

function toggleNaji() {{
    const btn = document.getElementById('nav-naji');
    const badges = document.querySelectorAll('.naji-badge');
    
    const isActivating = !btn.classList.contains('active-nj');
    
    if (isActivating) {{
        if (badges.length === 0) {{
            showToast('此盘暂无符合纳吉条件的吉位，请另择良辰。');
            return;
        }}
        btn.classList.add('active-nj');
        btn.style.color = '#28a745';
        badges.forEach(b => b.style.display = 'flex');
        showToast('已开启纳吉视觉，点击宫位中心看方案。');
    }} else {{
        btn.classList.remove('active-nj');
        btn.style.color = '';
        badges.forEach(b => b.style.display = 'none');
    }}
}}

function showToast(msg) {{
    const t = document.getElementById('toast');
    t.innerText = msg;
    t.classList.add('show');
    setTimeout(() => {{
        t.classList.remove('show');
    }}, 2000);
}}

function showNaji(event, b64Data) {{
    event.stopPropagation();
    const htmlData = decodeURIComponent(escape(atob(b64Data)));
    document.getElementById('naji-content-box').innerHTML = htmlData;
    document.getElementById('najiModal').style.display = 'block';
}}
function closeNajiModal() {{ document.getElementById('najiModal').style.display = 'none'; }}

function openFilterModal() {{ document.getElementById('filterModal').style.display = 'block'; }}
function closeFilterModal() {{ document.getElementById('filterModal').style.display = 'none'; }}

let currentFilteredData = [];
function startFilter() {{
    const start = document.getElementById('filter-start').value;
    const end = document.getElementById('filter-end').value;
    const btn = document.getElementById('filter-run-btn');
    const dlBtn = document.getElementById('download-all-btn');
    const resBox = document.getElementById('filter-results');
    
    if (!start || !end) {{ alert('请选择完整的时间范围'); return; }}
    
    btn.innerText = '正在推演中...';
    btn.disabled = true;
    dlBtn.style.display = 'none';
    resBox.innerHTML = '';
    
    fetch(`/api/filter_naji?start=${{start}}&end=${{end}}`)
    .then(r => r.json())
    .then(data => {{
        currentFilteredData = data;
        btn.innerText = '开始扫描纳吉时段';
        btn.disabled = false;
        if (data.length === 0) {{
            resBox.innerHTML = '<div style="text-align:center;padding:20px;color:#999">该时段内未扫描到纳吉时机</div>';
            return;
        }}
        dlBtn.style.display = 'inline-block';
        resBox.innerHTML = data.map(item => `
            <div class="naji-item" style="border-left: 4px solid #28a745; padding-left: 15px;">
                <span class="naji-time" style="font-size: 1.1rem;">${{item.time.split(' ')[0]}} <span style="color:#666;font-size:0.9rem">${{item.time_span || item.time.split(' ')[1]}}</span> (${{item.gz}})</span>
                <div class="naji-details" style="margin-top:8px;">
                    ${{item.palaces.map(p => `
                        <div style="margin-bottom:10px; background:white; padding:10px; border-radius:4px; box-shadow:0 1px 3px rgba(0,0,0,0.05)">
                            <div style="color:#b8860b; font-weight:bold; border-bottom:1px solid #eee; padding-bottom:5px; margin-bottom:8px;">方向：${{p.dir}} (${{p.cat}})</div>
                            <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 5px; font-size: 0.85rem; color: #666; margin-bottom: 8px; background: #fdfdfb; padding: 5px; border-radius: 2px;">
                                <div>神：${{p.shen}}</div>
                                <div>星：${{p.xing}}</div>
                                <div>门：${{p.men}}</div>
                                <div>宫：${{p.num}}宫</div>
                                <div>干：${{p.tp}} / ${{p.dp}}</div>
                                <div>色：<span style="color:#888">${{p.color_tp}}(上) - ${{p.color_dp}}(下)</span></div>
                            </div>
                            <div style="color:#444"><b>建议行为：</b>${{p.action}}</div>
                        </div>
                    `).join('')}}
                </div>
                <div style="display:flex; gap:10px; margin-top:10px;">
                    <button class="ical-btn" style="flex:1; background:#0088cc;" onclick="jmp('${{item.time}}', true)">回到奇门</button>
                    <button class="ical-btn" style="flex:1;" onclick="downloadSingleIcal('${{item.time}}')">单条入日历</button>
                </div>
            </div>
        `).join('');
    }})
    .catch(e => {{
        btn.innerText = '扫描出错';
        btn.disabled = false;
        alert('扫描请求失败');
    }});
}}

function downloadSingleIcal(time) {{
    const item = currentFilteredData.find(d => d.time === time);
    if (item) downloadIcalFile([item], `naji_${{time.replace(/[: ]/g,'_')}}.ics`);
}}

function downloadAllIcal() {{
    if (currentFilteredData.length === 0) return;
    const s = document.getElementById('filter-start').value;
    const e = document.getElementById('filter-end').value;
    let d1 = new Date(s);
    let d2 = new Date(e);
    let ds = `${{d1.getFullYear()}}.${{d1.getMonth()+1}}.${{d1.getDate()}}`;
    let de = `${{d2.getFullYear()}}.${{d2.getMonth()+1}}.${{d2.getDate()}}`;
    let calName = `纳吉（${{ds}}-${{de}}）`;
    
    downloadIcalFile(currentFilteredData, `naji_batch_${{ds}}-${{de}}.ics`, calName);
}}

function downloadIcalFile(items, filename, calName="奇门日历") {{
    let icalContent = `BEGIN:VCALENDAR\\r\\nVERSION:2.0\\r\\nPRODID:-//Apple Inc.//Mac OS X 10.15.7//EN\\r\\nCALSCALE:GREGORIAN\\r\\nMETHOD:PUBLISH\\r\\nX-WR-CALNAME:${{calName}}\\r\\n`;
    items.forEach(item => {{
        const dtStart = item.time.replace(/[- :]/g, "") + "00";
        // End time is 2 hours later
        const [d, t] = item.time.split(' ');
        const [h, m] = t.split(':').map(Number);
        let endH = h + 2;
        let endD = d;
        if (endH >= 24) {{
            endH -= 24;
            let dateObj = new Date(d);
            dateObj.setDate(dateObj.getDate() + 1);
            endD = dateObj.toISOString().split('T')[0];
        }}
        const dtEnd = endD.replace(/-/g, "") + "T" + String(endH).padStart(2, '0') + String(m).padStart(2, '0') + "00";
        const dtStartFull = d.replace(/-/g, "") + "T" + t.replace(/:/g, "") + "00";
        
        const summary = "纳吉: " + item.palaces.map(p => p.cat).join(" & ");
        const desc = item.palaces.map(p => 
            `方向: ${{p.dir}}\\\\n类别: ${{p.cat}}\\\\n详情: ${{p.shen}}/${{p.xing}}/${{p.men}}/${{p.tp}}${{p.dp}}\\\\n颜色: ${{p.color_tp}}(上) - ${{p.color_dp}}(下)\\\\n行为: ${{p.action}}`
        ).join("\\\\n---\\\\n");

        const dtStamp = new Date().toISOString().replace(/[-:]/g, "").split('.')[0] + "Z";
        const seq = Math.floor((Date.now() - 1700000000000) / 1000);
        icalContent += "BEGIN:VEVENT\\r\\n";
        icalContent += `UID:naji_${{dtStartFull}}@qimen.local\\r\\n`;
        icalContent += `DTSTAMP:${{dtStamp}}\\r\\n`;
        icalContent += `SEQUENCE:${{seq}}\\r\\n`;
        icalContent += `SUMMARY:${{summary}}\\r\\n`;
        icalContent += `DTSTART:${{dtStartFull}}\\r\\n`;
        icalContent += `DTEND:${{dtEnd}}\\r\\n`;
        icalContent += `DESCRIPTION:${{desc}}\\r\\n`;
        icalContent += `BEGIN:VALARM\\r\\n`;
        icalContent += `ACTION:DISPLAY\\r\\n`;
        icalContent += `DESCRIPTION:纳吉提醒\\r\\n`;
        icalContent += `TRIGGER:-PT10M\\r\\n`;
        icalContent += `END:VALARM\\r\\n`;
        icalContent += "STATUS:CONFIRMED\\r\\n";
        icalContent += "END:VEVENT\\r\\n";
    }});
    icalContent += "END:VCALENDAR";
    
    const blob = new Blob([icalContent], {{ type: 'text/calendar;charset=utf-8' }});
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}}

window.onclick = function(event) {{
  if (event.target == document.getElementById('saveModal')) closeSaveModal();
  if (event.target == document.getElementById('listModal')) closeListModal();
  if (event.target == document.getElementById('najiModal')) closeNajiModal();
  if (event.target == document.getElementById('filterModal')) closeFilterModal();
  if (event.target == document.getElementById('shareModal')) closeShareModal();
  if (event.target == document.getElementById('gejuModal')) closeGejuModal();
  if (event.target == document.getElementById('noteModal')) closeNoteModal();
}}

function submitSaveCase() {{
    const isNew = !currentChartInfo.id;
    const data = {{
        id: currentChartInfo.id,
        name: document.getElementById('main-matter').value,
        question: "",
        notes: document.getElementById('main-note').value,
        bazi: currentChartInfo.bazi,
        ju_shu: currentChartInfo.ju_shu,
        chart_time: currentChartInfo.chart_time
    }};
    
    fetch('/api/save_case', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(data)
    }}).then(r => r.json()).then(res => {{
        if(res.status == 'ok') {{ 
            if (res.id) currentChartInfo.id = res.id;
            // Update any other UI elements if needed, but save-btn-text is no longer used
            showToast(isNew ? '案例保存成功！' : '案例内容已更新');
        }}
        else {{
            alert('保存失败: ' + (res.message || '未知错误'));
        }}
    }}).catch(e => {{
        console.error("Save error:", e);
        alert('请求出错，请检查服务器连接。');
    }});
}}

function loadCases() {{
    fetch('/api/cases?t=' + Date.now()).then(r => r.json()).then(data => {{
        const container = document.getElementById('case-list-container');
        if (!data || data.length === 0) {{
            container.innerHTML = '<div style="text-align:center;color:#999;padding:20px">暂无案例记录</div>';
            return;
        }}
        container.innerHTML = data.map(c => `
            <div class="case-item" onclick="jmp('${{c.chart_time}}', false, ${{c.id}})">
                <div class="case-title">${{c.name}} <span style="color:#999;font-size:0.8em;font-weight:normal;margin-left:10px">${{c.ju_shu}} | ${{c.bazi}}</span></div>
                <div class="case-meta">排盘时间：${{c.chart_time}} | 记录：${{c.create_time}}</div>
                <div style="margin-top:5px;color:#444;font-size:0.9rem">${{c.question ? c.question.substring(0,50) : (c.notes ? c.notes.substring(0,80) + (c.notes.length>80?'...':'') : '无具体求测描述')}}</div>
                <div style="margin-top:8px; display:flex; gap:10px; align-items:center;">
                    <span style="color:#00bfa5; font-size:0.85rem">点击载入详情并编辑</span>
                    <div class="case-del" style="position:static; font-size:0.85rem;" onclick="deleteCase(event, ${{c.id}}, this)">删除</div>
                </div>
            </div>
        `).join('');
    }}).catch(e => {{
        document.getElementById('case-list-container').innerHTML = '<div style="color:red;text-align:center">拉取数据失败，请检查服务。</div>';
    }});
}}

function deleteCase(event, id, btn) {{
    event.stopPropagation();
    if (btn.innerText === '删除') {{
        btn.innerText = '确认?';
        btn.style.color = 'white';
        btn.style.background = '#dc3545';
        setTimeout(() => {{ if(btn && btn.innerText === '确认?') {{ btn.innerText = '删除'; btn.style.background = 'transparent'; btn.style.color = '#cc0000'; }} }}, 3000);
        return;
    }}
    
    fetch('/api/delete_case?id=' + id, {{method: 'POST'}})
    .then(r => r.json())
    .then(res => {{
        if(res.status == 'ok') loadCases();
        else if(window.alert) alert('删除失败');
    }})
    .catch(e => console.log('请求出错: ' + e));
}}

window.addEventListener('DOMContentLoaded', () => {{
    if (new URLSearchParams(window.location.search).get('naji') === '1') {{
        toggleNaji();
    }}
    // Initialize auto-resize for main-matter
    const mm = document.getElementById('main-matter');
    if (mm) autoResize(mm);
}});
</script>
</body>
</html>'''

def main():
    import http.server
    import socketserver
    from urllib.parse import urlparse, unquote

    default_dt = datetime.now()
    static_mode = False
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--static':
            static_mode = True
        else:
            try: default_dt = datetime.strptime(sys.argv[1], "%Y-%m-%d %H:%M")
            except: print("Format error"); sys.exit(1)
            
    if static_mode:
        r = paipan(default_dt)
        h = generate_html(r, default_dt)
        f_path = os.path.join(os.path.dirname(__file__), 'qimen_chart.html')
        with open(f_path, 'w', encoding='utf-8') as f: f.write(h)
        print(f"Generated static file: {f_path}")
        webbrowser.open(f'file://{f_path}')
        return

    # 启动本地HTTP Server，支持热跳转 (下一局/上一局)
    class QimenHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            query = parsed.query
            
            if parsed.path == '/api/cases':
                conn = sqlite3.connect(DB_PATH)
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                c.execute('SELECT * FROM cases ORDER BY create_time DESC')
                rows = [dict(r) for r in c.fetchall()]
                conn.close()
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.end_headers()
                self.wfile.write(json.dumps(rows).encode('utf-8'))
                return
                
            if parsed.path.startswith('/api/delete_case'):
                idx = unquote(query.split('id=')[1].split('&')[0]) if 'id=' in query else ''
                if idx.isdigit():
                    conn = sqlite3.connect(DB_PATH)
                    c = conn.cursor()
                    c.execute('DELETE FROM cases WHERE id = ?', (int(idx),))
                    conn.commit()
                    conn.close()
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok'}).encode('utf-8'))
                return
            
            if parsed.path == '/api/filter_naji':
                start_str = query.split('start=')[1].split('&')[0] if 'start=' in query else ''
                end_str = query.split('end=')[1].split('&')[0] if 'end=' in query else ''
                
                results = []
                try:
                    start_date = datetime.strptime(start_str, "%Y-%m-%d")
                    end_date = datetime.strptime(end_str, "%Y-%m-%d") + timedelta(days=1)
                    
                    curr = start_date
                    while curr < end_date:
                        for hour in range(0, 24, 2):
                            chk_dt = curr + timedelta(hours=hour)
                            # 模拟生成纳吉逻辑 (剥离HTML生成的纯数据判断)
                            res = paipan(chk_dt)
                            # 复用 generate_html 内的逻辑，但这里为了速度和解耦，我们快速实现一个判定器
                            # 注意：这种逻辑应该被封装成函数，目前为了演示先内联
                            found_palaces = []
                            # --- 判定逻辑开始 (与 generate_html 保持同步) ---
                            jg = res['jiugong']
                            # 伏吟反吟
                            is_gan_fuyin = all(jg[g].get('tianpan') == jg[g].get('dipan') for g in [1,2,3,4,6,7,8,9])
                            original_doors = {'休门': 1, '死门': 2, '伤门': 3, '杜门': 4, '开门': 6, '惊门': 7, '生门': 8, '景门': 9}
                            opposite_doors = {'休门': 9, '死门': 8, '伤门': 7, '杜门': 6, '开门': 4, '惊门': 3, '生门': 2, '景门': 1}
                            home_stars = { k: v for k, v in [('天蓬',1),('天芮',2),('芮禽',2),('天冲',3),('天辅',4),('天禽',5),('天心',6),('天柱',7),('天任',8),('天英',9)] }
                            opposite_stars = { k: v for k, v in [('天蓬',9),('天芮',8),('芮禽',8),('天冲',7),('天辅',6),('天禽',8),('天心',4),('天柱',3),('天任',2),('天英',1)] }
                            is_men_fuyin  = all(original_doors.get(jg[g].get('men','')) == g for g in [1,3,4,6,7,9])
                            is_xing_fuyin = all(home_stars.get(jg[g].get('xing','').replace('星','')) == g for g in [1,3,4,6,7,9])
                            is_men_fanyin = all(opposite_doors.get(jg[g].get('men','')) == g for g in [1,3,4,6,7,9])
                            is_xing_fanyin = all(opposite_stars.get(jg[g].get('xing','').replace('星','')) == g for g in [1,3,4,6,7,9])
                            bad_chart = is_gan_fuyin or is_men_fuyin or is_xing_fuyin or is_men_fanyin or is_xing_fanyin
                            # 五不遇时
                            wubuyushi = ((res['day_gz'][0] == '甲' and res['hour_gz'][0] == '庚') or
                                         (res['day_gz'][0] == '乙' and res['hour_gz'][0] == '辛') or
                                         (res['day_gz'][0] == '丙' and res['hour_gz'][0] == '壬') or
                                         (res['day_gz'][0] == '丁' and res['hour_gz'][0] == '癸') or
                                         (res['day_gz'][0] == '戊' and res['hour_gz'][0] == '甲') or
                                         (res['day_gz'][0] == '己' and res['hour_gz'][0] == '乙') or
                                         (res['day_gz'][0] == '庚' and res['hour_gz'][0] == '丙') or
                                         (res['day_gz'][0] == '辛' and res['hour_gz'][0] == '丁') or
                                         (res['day_gz'][0] == '壬' and res['hour_gz'][0] == '戊') or
                                         (res['day_gz'][0] == '癸' and res['hour_gz'][0] == '己'))
                            
                            if not bad_chart and not wubuyushi:
                                marks = analyze_sihai(res)
                                valid_doors_map = {1:['开门'], 2:['开门','景门'], 3:['休门','景门'], 4:['休门','景门'], 6:['休门','生门'], 7:['休门','生门','开门'], 8:['开门','景门'], 9:['生门']}
                                # 旬空
                                xk_zhi = {'甲子':'戌亥','甲戌':'申酉','甲申':'午未','甲午':'辰巳','甲辰':'寅卯','甲寅':'子丑'}.get(res['xun_shou'], '')
                                zhi_gong = {'子':1,'丑':8,'寅':8,'卯':3,'辰':4,'巳':4,'午':9,'未':2,'申':2,'酉':7,'戌':6,'亥':6}
                                kong_gongs = {zhi_gong[z] for z in list(xk_zhi) if z in zhi_gong}
                                
                                for gn in [1,2,3,4,6,7,8,9]:
                                    g_info = jg[gn]
                                    m_name = g_info.get('men','')
                                    if m_name in valid_doors_map.get(gn, []):
                                        m_marks = marks.get(gn, {}).get('men', [])
                                        if '门迫' in m_marks: continue
                                        if gn in kong_gongs: continue
                                        tp_gan = g_info.get('tianpan','')
                                        dp_gan = g_info.get('dipan','')
                                        if '庚' in [tp_gan, dp_gan]: continue
                                        gan_tags = marks.get(gn, {}).get('gan_tags', {})
                                        if '击刑' in gan_tags.get(tp_gan, []) or '入墓' in gan_tags.get(tp_gan, []): continue
                                        if '击刑' in gan_tags.get(dp_gan, []) or '入墓' in gan_tags.get(dp_gan, []): continue
                                        if g_info.get('shen') == '白虎': continue
                                        if g_info.get('xing','').replace('星','') in ['天蓬','天芮','芮禽']: continue
                                        if m_name == '景门' and g_info.get('shen') in ['玄武', '九地']: continue
                                        
                                        # 根据组合规则提取动作
                                        action_str = get_smart_naji_action(tp_gan, dp_gan, g_info.get('shen'), g_info.get('xing'), m_name)
                                        
                                        found_palaces.append({
                                            'num': gn, 
                                            'men': m_name, 
                                            'dir': GONG_DIRECTIONS.get(gn),
                                            'cat': NAJI_CATEGORIES.get(m_name, '通用'),
                                            'action': action_str,
                                            'shen': g_info.get('shen'),
                                            'xing': g_info.get('xing','').replace('星',''),
                                            'tp': tp_gan,
                                            'dp': dp_gan,
                                            'color_tp': NAJI_COLORS.get(tp_gan, '无'),
                                            'color_dp': NAJI_COLORS.get(dp_gan, '无')
                                        })
                            # --- 判定逻辑结束 ---

                            if found_palaces:
                                # 计算时辰起始时间。奇门时辰为(单数时)-1到(单数时)+1。如 09:00-11:00。
                                h = chk_dt.hour
                                if h % 2 != 0: # 单数时 (如 01, 03...)
                                    s_dt = chk_dt.replace(minute=0, second=0, microsecond=0)
                                else: # 双数时 (如 10, 12...)
                                    s_dt = (chk_dt - timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
                                
                                s_h = s_dt.hour
                                e_h = (s_dt + timedelta(hours=2)).hour
                                
                                time_span = f"{res['hour_gz'][1]}时 ({s_h:02d}:00-{e_h:02d}:00)"
                                results.append({
                                    'time': s_dt.strftime("%Y-%m-%d %H:%M"),
                                    'time_span': time_span,
                                    'gz': f"{res['day_gz']} {res['hour_gz']}",
                                    'palaces': found_palaces
                                })
                        curr += timedelta(days=1)
                except Exception as e:
                    print(f"Filter error: {e}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(results).encode('utf-8'))
                return
                
            case_id_param = None
            if 'id=' in query:
                case_id_param = unquote(query.split('id=')[1].split('&')[0])
            
            dt_str = None
            if 'dt=' in query:
                dt_str = unquote(query.split('dt=')[1].split('&')[0])
            
            saved_matter = ""
            saved_notes = ""
            case_id = None
            
            if case_id_param and case_id_param.isdigit():
                conn = sqlite3.connect(DB_PATH)
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                c.execute('SELECT * FROM cases WHERE id = ?', (int(case_id_param),))
                row = c.fetchone()
                if row:
                    target_dt = datetime.strptime(row['chart_time'], "%Y-%m-%d %H:%M")
                    saved_matter = row['name']
                    saved_notes = row['notes']
                    case_id = row['id']
                else:
                    target_dt = default_dt
                conn.close()
            elif dt_str:
                try: target_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
                except: target_dt = default_dt
            else:
                target_dt = default_dt
            
            try:    
                r = paipan(target_dt)
                h = generate_html(r, target_dt, matter=saved_matter, notes=saved_notes, case_id=case_id)
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Expires', '0')
                self.end_headers()
                self.wfile.write(h.encode('utf-8'))
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

        def do_POST(self):
            parsed = urlparse(self.path)
            query = parsed.query
            
            if parsed.path.startswith('/api/delete_case'):
                idx = unquote(query.split('id=')[1].split('&')[0]) if 'id=' in query else ''
                if idx.isdigit():
                    conn = sqlite3.connect(DB_PATH)
                    c = conn.cursor()
                    c.execute('DELETE FROM cases WHERE id = ?', (int(idx),))
                    conn.commit()
                    conn.close()
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok'}).encode('utf-8'))
                return
                
            if parsed.path == '/api/save_case':
                try:
                    length = int(self.headers.get('Content-Length', 0))
                    body = self.rfile.read(length)
                    data = json.loads(body.decode('utf-8'))
                    
                    conn = sqlite3.connect(DB_PATH)
                    c = conn.cursor()
                    cid = data.get('id')
                    if cid:
                        c.execute('UPDATE cases SET name=?, question=?, notes=? WHERE id=?', 
                                  (data.get('name',''), data.get('question',''), 
                                   data.get('notes',''), cid))
                    else:
                        c.execute('''INSERT INTO cases (name, question, notes, bazi, ju_shu, chart_time) 
                                     VALUES (?, ?, ?, ?, ?, ?)''', 
                                     (data.get('name',''), data.get('question',''), 
                                      data.get('notes',''), data.get('bazi',''), 
                                      data.get('ju_shu',''), data.get('chart_time','')))

                    conn.commit()
                    resp_id = cid if cid else c.lastrowid
                    conn.close()
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'ok', 'id': resp_id}).encode('utf-8'))
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))
                return
            self.send_response(404)
            self.end_headers()
                
        def log_message(self, format, *args):
            pass # ignore logging in console to keep it clean

    port = 8088
    # Keep trying ports if 8088 is busy
    while True:
        try:
            server = socketserver.TCPServer(("", port), QimenHandler)
            break
        except OSError:
            port += 1

    dt_formatted = default_dt.strftime("%Y-%m-%d %H:%M")
    url = f"http://127.0.0.1:{port}/?dt={dt_formatted.replace(' ', '%20')}"
    print(f"已启动奇门遁甲本地浏览器服务！")
    print(f"自动打开网页: {url}")
    print(f"您可以直接在网页上点击[上一局]和[下一局]！按 Ctrl+C 退出。")
    
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("\n已退出服务。")

if __name__ == "__main__": main()
