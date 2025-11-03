import json
from boat_race_sites import boat_race_sites

site_config = {}
for name, info in boat_race_sites.items():
    site_id = info["id"]
    site_config[site_id] = {
        "name": name,
        "time_slot": "モーニング",  # 初期値（後で編集可）
        "active": True,
        "manual_state": None
    }

with open("data/site_config.json", "w", encoding="utf-8") as f:
    json.dump(site_config, f, ensure_ascii=False, indent=2)

print("site_config.json を初期化しました。")