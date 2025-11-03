# 最大影響風向き（進行方向 -135°）
def get_max_effect_angle(course_angle):
    base = course_angle - 135
    return base + 360 if base < 0 else base

# 偏差（符号付き）を計算
def get_signed_deviation(wind_deg, max_effect_deg):
    diff = (wind_deg - max_effect_deg + 360) % 360
    return diff if diff <= 180 else diff - 360

# 偏差からゾーン分類（A〜H）
def classify_effect_zone(deviation):
    zones = [
        (-180, -135, "H（かなり不利）"),
        (-135, -90,  "G（とても不利）"),
        (-90, -45,   "F（やや不利）"),
        (-45, 0,     "E（普通）"),
        (0, 45,      "D（やや有利）"),
        (45, 90,     "C（とても有利）"),
        (90, 135,    "B（かなり有利）"),
        (135, 180,   "A（最大有利）"),
    ]
    for low, high, label in zones:
        if low < deviation <= high:
            return label
    return "？"

# 風向き → 矢印（8方向）
def wind_deg_to_arrow(deg):
    arrows = ["↑", "↗", "→", "↘", "↓", "↙", "←", "↖"]
    index = int(((deg + 22.5) % 360) // 45)
    return arrows[index]

# 風速 → 色分け
def wind_speed_color(speed):
    if speed >= 6.0:
        return "red"
    elif speed >= 3.0:
        return "yellow"
    else:
        return "white"