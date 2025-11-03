# 方角→角度変換辞書
direction_to_angle = {
    "真　北": 0.0,
    "北北東": 22.5,
    "北　東": 45.0,
    "東北東": 67.5,
    "真　東": 90.0,
    "東南東": 112.5,
    "南南東": 157.5,
    "真　南": 180.0,
    "南南西": 202.5,
    "南　西": 225.0,
    "西南西": 247.5,
    "真　西": 270.0,
    "西北西": 292.5,
    "北　西": 315.0,
    "北北西": 337.5,
    "南西南": 232.5,
    "北　東": 45.0,
    "北　西": 315.0
}

# テキストを辞書形式に変換
boat_race_sites = {}

with open("BortRaceSiteList.txt", "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("#"):
            parts = line.strip().split()
            site_id = parts[0][1:]  # "#01" → "01"
            name = parts[1]
            latlon = parts[2].replace(",", "")  # "36.394941," → "36.394941"
            lat = float(latlon)
            lon = float(parts[3])
            direction = parts[5]
            angle = direction_to_angle.get(direction, None)

            boat_race_sites[name] = {
                "id": site_id,
                "lat": lat,
                "lon": lon,
                "direction": direction,
                "angle": angle
            }

# 結果確認
for name, info in boat_race_sites.items():
    print(f"{info['id']} {name}: 緯度{info['lat']}, 経度{info['lon']}, 方角{info['direction']}（{info['angle']}°）")