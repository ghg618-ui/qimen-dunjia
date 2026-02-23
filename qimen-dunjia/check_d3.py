GANZHI = [f"{t}{d}" for t in "甲乙丙丁戊己庚辛壬癸" for d in "子丑寅卯辰巳午未申酉戌亥"] # no wait this produces 120
TIANGAN = "甲乙丙丁戊己庚辛壬癸"
DIZHI = "子丑寅卯辰巳午未申酉戌亥"
print([f"{TIANGAN[i%10]}{DIZHI[i%12]}" for i in range(60)][10])
print([f"{TIANGAN[i%10]}{DIZHI[i%12]}" for i in range(60)][43])
print([f"{TIANGAN[i%10]}{DIZHI[i%12]}" for i in range(60)][3])
