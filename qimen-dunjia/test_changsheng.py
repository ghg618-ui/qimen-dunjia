states = ["长生", "沐浴", "冠带", "临官", "帝旺", "衰", "病", "死", "墓", "绝", "胎", "养"]
# 十干十二长生
# 甲：亥长生
# 丙/戊：寅长生
# 庚：巳长生
# 壬：申长生
# 乙：午长生 (逆排)
# 丁/己：酉长生 (逆排)
# 辛：子长生 (逆排)
# 癸：卯长生 (逆排)

dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

start_idx = {
    '甲': dizhi.index('亥'),
    '丙': dizhi.index('寅'),
    '戊': dizhi.index('寅'),
    '庚': dizhi.index('巳'),
    '壬': dizhi.index('申'),
    '乙': dizhi.index('午'),
    '丁': dizhi.index('酉'),
    '己': dizhi.index('酉'),
    '辛': dizhi.index('子'),
    '癸': dizhi.index('卯'),
}
direction = {
    '甲': 1, '丙': 1, '戊': 1, '庚': 1, '壬': 1,
    '乙': -1, '丁': -1, '己': -1, '辛': -1, '癸': -1,
}

def get_state(gan, zhi):
    if gan not in start_idx or zhi not in dizhi:
        return ""
    start = start_idx[gan]
    target = dizhi.index(zhi)
    dir = direction[gan]
    # diff
    if dir == 1:
        steps = (target - start) % 12
    else:
        steps = (start - target) % 12
    return states[steps]

# 九宫对应地支
# 1: 子
# 8: 丑, 寅 (通常取主地支或者怎么算？奇门遁甲通常以该宫的地支为准，若有2个地支，怎么办？
# 比如艮八宫有丑寅，长生看哪个？
