from datetime import datetime, timedelta
from qimen_paipan import get_ganzhi_day, get_san_yuan

d = datetime(2025, 7, 1)
for i in range(25):
    dt = d + timedelta(days=i)
    gz = get_ganzhi_day(dt)
    sy = get_san_yuan(gz)
    print(f"{dt.strftime('%Y-%m-%d')}: {gz} - {['Shang', 'Zhong', 'Xia'][sy]}")
