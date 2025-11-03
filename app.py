from flask import Flask, render_template, request, redirect
from boat_race_sites import boat_race_sites
from datetime import datetime, timedelta
from wind_utils import ( get_max_effect_angle, get_signed_deviation, classify_effect_zone, wind_deg_to_arrow, wind_speed_color )
import json
import requests

app = Flask(__name__)
API_KEY = "437eb35265e0910b36492fc732d1fec7"

@app.route("/config", methods=["GET"])
def config():
    with open("data/site_config.json", "r", encoding="utf-8") as f:
        site_config = json.load(f)
    with open("data/time_slots.json", "r", encoding="utf-8") as f:
        time_slots = json.load(f)
    return render_template("config.html", site_config=site_config, time_slots=time_slots)

@app.route("/save_time_slots", methods=["POST"])
def save_time_slots():
    try:
        print("📨 request.form:", request.form)

        time_slots = {}
        for index in request.form.getlist("slot_names"):
            label = request.form.get(f"slot_label_{index}", "")
            start = request.form.get(f"start_{index}", "")
            end = request.form.get(f"end_{index}", "")
            print(f"▶ index={index}, label={label}, start={start}, end={end}")

            if not label:
                raise ValueError(f"label が空です（index={index}）")

            time_slots[label] = {"start": start, "end": end}

        with open("data/time_slots.json", "w", encoding="utf-8") as f:
            json.dump(time_slots, f, indent=2, ensure_ascii=False)

        return redirect("/config")

    except Exception as e:
        print("❌ エラー:", e)
        return "Internal Server Error", 500

@app.route("/save_config", methods=["POST"])
def save_config():
    # 現在の設定を読み込む
    with open("data/site_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    #フォームからのデータで更新
    for site_id in config.keys():
        config[site_id]["active"] = site_id in request.form.getlist("active")
        config[site_id]["time_slot"] = request.form.get(f"time_slot_{site_id}", config[site_id]["time_slot"])
        config[site_id]["manual_state"] = request.form.get(f"manual_state_{site_id}", None)

     #上書き保存
    with open("data/site_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    return redirect("/config")

@app.route("/refresh_data", methods=["POST"])
def refresh_data():
    raw_value = request.form.get("national_view", "false")
    print("📥 national_view raw:", raw_value)
    national_view = raw_value.lower() == "true"
    return redirect(f"/?national_view={'true' if national_view else 'false'}")

@app.route("/")
def index():
    # 全国表示スイッチの状態を取得（GETパラメータ）
    national_view = request.args.get("national_view", "false").lower() == "true"

    # サイト設定を読み込み
    with open("data/site_config.json", "r", encoding="utf-8") as f:
        site_config = json.load(f)

    # 表示対象をフィルタリング
    filtered_sites = {
        name: info for name, info in boat_race_sites.items()
        if national_view or site_config.get(info["id"], {}).get("active", False)
    }

    sites = []
    now = datetime.now()
    timestamp = now.strftime("%Y/%m/%d %H:%M:%S")

    for name, info in filtered_sites.items():
        lat = info["lat"]
        lon = info["lon"]
        angle = info["angle"]
        direction = info["direction"]
        site_id = info["id"]

        try:
            #url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            #res = requests.get(url)
            #data = res.json()
            #wind_deg = data["wind"]["deg"]
            #wind_speed = data["wind"]["speed"]

            wind_deg = 45.0  # 北東風
            wind_speed = 3.5  # 3.5m/s

            max_effect_deg = get_max_effect_angle(angle)
            deviation = get_signed_deviation(wind_deg, max_effect_deg)
            zone = classify_effect_zone(deviation)
            arrow = wind_deg_to_arrow(wind_deg)
            color = wind_speed_color(wind_speed)

            sites.append({
                "id": site_id,
                "name": name,
                "direction": direction,
                "arrow": arrow,
                "speed": f"{wind_speed:.1f}",
                "color": color,
                "zone": zone
            })

        except Exception as e:
            sites.append({
                "id": site_id,
                "name": name,
                "direction": direction,
                "arrow": "？",
                "speed": "--",
                "color": "white",
                "zone": f"取得失敗（{e}）"
            })

    return render_template("index.html", sites=sites, timestamp=timestamp, national_view=national_view)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) #(debug=True)