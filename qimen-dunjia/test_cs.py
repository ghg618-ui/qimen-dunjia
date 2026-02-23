def get_cs(gan, palace):
    if not gan: return ""
    starts = {'甲':'亥', '乙':'午', '丙':'寅', '丁':'酉', '戊':'寅', '己':'酉', '庚':'巳', '辛':'子', '壬':'申', '癸':'卯'}
    dirs = {'甲':1, '乙':-1, '丙':1, '丁':-1, '戊':1, '己':-1, '庚':1, '辛':-1, '壬':1, '癸':-1}
    is_yin = dirs.get(gan, 1) == -1
    
    BRANCHES = {
        1: ['子'], 8: ['丑', '寅'], 3: ['卯'], 4: ['辰', '巳'],
        9: ['午'], 2: ['未', '申'], 7: ['酉'], 6: ['戌', '亥'],
        5: ['未', '申']
    }
    targets = BRANCHES[palace]
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

print("Palace 4 - 癸:", get_cs('癸', 4))
print("Palace 4 - 庚:", get_cs('庚', 4))
print("Palace 4 - 壬:", get_cs('壬', 4))
print("Palace 2 - 丁:", get_cs('丁', 2))
print("Palace 2 - 癸:", get_cs('癸', 2))
print("Palace 2 - 庚:", get_cs('庚', 2))
print("Palace 8 - 壬:", get_cs('壬', 8))
print("Palace 8 - 乙:", get_cs('乙', 8))
print("Palace 1 - 辛:", get_cs('辛', 1))
print("Palace 1 - 己:", get_cs('己', 1))
print("Palace 9 - 丙:", get_cs('丙', 9))
print("Palace 7 - 己:", get_cs('己', 7))

