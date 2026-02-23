from datetime import datetime
from scripts.qimen_paipan import *
dt = datetime(2026, 2, 22, 9, 46)
print(get_ganzhi_year(dt), get_ganzhi_month(dt), get_ganzhi_day(dt), get_ganzhi_hour(dt))
