SANQI_LIUYI = ['戊', '己', '庚', '辛', '壬', '癸', '丁', '丙', '乙']
sg_idx = SANQI_LIUYI.index('乙')
start_g = 5
res = {i: [] for i in range(1, 10)}
for step in range(9):
    curr_g = (start_g + step - 1) % 9 + 1
    curr_stem = SANQI_LIUYI[(sg_idx + step) % 9]
    res[curr_g].append(curr_stem)
for k,v in res.items(): print(k, v)
