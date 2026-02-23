from lunar_python import Solar

solar = Solar.fromYmdHms(1987, 5, 8, 16, 56, 0)
lunar = solar.getLunar()

y = lunar.getYearInGanZhiExact()
m = lunar.getMonthInGanZhiExact()
d = lunar.getDayInGanZhiExact()
h = lunar.getTimeInGanZhi()

print(f"Bazi: {y} {m} {d} {h}")
