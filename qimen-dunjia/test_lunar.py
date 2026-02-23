from lunar_python import Solar
from datetime import datetime

# 1987-05-08
solar = Solar.fromYmdHms(1987, 5, 8, 16, 56, 0)
lunar = solar.getLunar()
prev_jieqi = lunar.getPrevJieQi(True) # True means get precise exact time

print(f"JieQi Name: {prev_jieqi.getName()}")
jq_solar = prev_jieqi.getSolar()
print(f"JieQi Time: {jq_solar.getYear()}-{jq_solar.getMonth()}-{jq_solar.getDay()} {jq_solar.getHour()}:{jq_solar.getMinute()}:{jq_solar.getSecond()}")
