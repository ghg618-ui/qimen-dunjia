import math
from datetime import datetime, timedelta

def get_julian_day(year, month, day, hour, minute):
    if month <= 2:
        year -= 1
        month += 12
    A = year // 100
    B = 2 - A + A // 4
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
    jd += (hour + minute / 60.0) / 24.0
    return jd

def get_jd_from_datetime(dt):
    # expect utc
    return get_julian_day(dt.year, dt.month, dt.day, dt.hour, dt.minute) + dt.second/86400.0

def sun_ecliptic_longitude(jd):
    T = (jd - 2451545.0) / 36525.0
    # Mean anomaly
    M = 357.52911 + 35999.05029 * T - 0.0001537 * T**2
    M = math.radians(M % 360)
    # Mean long
    L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T**2
    # Equation of center
    C = (1.914602 - 0.004817 * T - 0.000014 * T**2) * math.sin(M)
    C += (0.019993 - 0.000101 * T) * math.sin(2 * M)
    C += 0.000289 * math.sin(3 * M)
    # True long
    true_long = (L0 + C) % 360
    
    # Apparent long
    omega = 125.04 - 1934.136 * T
    omega = math.radians(omega % 360)
    app_long = true_long - 0.00569 - 0.00478 * math.sin(omega)
    return app_long % 360

def exact_solar_term(year, term_index):
    # term_index 0 = 冬至 (270), 1 = 小寒 (285), etc.
    target_long = (270 + term_index * 15) % 360
    
    # Base datetime (approximation)
    # rough approximation of the day of year
    base_days = [356, 6, 20, 35, 50, 65, 80, 95, 110, 126, 141, 157, 172, 187, 203, 219, 234, 250, 265, 281, 296, 311, 326, 341]
    
    # Winter solstice can fall in Dec of PREVIOUS year for index 0!
    if term_index == 0:
        dt = datetime(year - 1, 1, 1) + timedelta(days=base_days[0])
    else:
        dt = datetime(year, 1, 1) + timedelta(days=base_days[term_index])
    
    # binary search precision to minutes
    low_dt = dt - timedelta(days=5)
    high_dt = dt + timedelta(days=5)
    
    for _ in range(30):
        mid_dt = low_dt + (high_dt - low_dt) / 2
        # Use UTC for calculation then convert
        utc_mid = mid_dt - timedelta(hours=8)
        jd = get_jd_from_datetime(utc_mid)
        long = sun_ecliptic_longitude(jd)
        
        diff = (long - target_long) % 360
        if diff > 180:
            diff -= 360
            
        if diff > 0:
            high_dt = mid_dt
        else:
            low_dt = mid_dt
            
    # round to nearest minute
    mid_dt = low_dt + (high_dt - low_dt) / 2
    return mid_dt.replace(second=0, microsecond=0)

if __name__ == "__main__":
    # Test Lixia
    print("1987 立夏:", exact_solar_term(1987, 9))
    print("1987 小满:", exact_solar_term(1987, 10))
