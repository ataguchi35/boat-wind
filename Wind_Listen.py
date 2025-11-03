from boat_race_sites import boat_race_sites
from wind_utils import (
    get_max_effect_angle,
    get_signed_deviation,
    classify_effect_zone,
    wind_deg_to_arrow,
    wind_speed_color
)
import requests

API_KEY = "437eb35265e0910b36492fc732d1fec7"  # ← ご自身のAPIキーを入力

for site_name, info in boat_race_sites.items():
    lat = info["lat"]
    lon = info["lon"]
    course_angle = info["angle"]
    direction = info["direction"]
    site_id = info["id"]

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        res = requests.get(url)
        data = res.json()
        wind_deg = data["wind"]["deg"]
        wind_speed = data["wind"]["speed"]

        max_effect_deg = get_max_effect_angle(course_angle)
        deviation = get_signed_deviation(wind_deg, max_effect_deg)
        zone = classify_effect_zone(deviation)
        arrow = wind_deg_to_arrow(wind_deg)
        color = wind_speed_color(wind_speed)

        print(f"#{site_id} {site_name}　1st {direction}　風{arrow} {wind_speed:.1f}m（{color}）　ゾーン {zone}")

    except Exception as e:
        print(f"#{site_id} {site_name}　データ取得失敗：{e}")