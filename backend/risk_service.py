

import math
import json
import urllib.request
import urllib.parse
import folium
from folium.plugins import HeatMap

KNOWN_PLACES = {
    "laxman jhula": {
        "coords": (30.1259, 78.3285),
        "score": 3,
        "factors": ["Popular tourist area — well patrolled", "Suspension bridge — crowded but maintained"],
        "level": "SAFE",
    },
    "ram jhula": {
        "coords": (30.1090, 78.3038),
        "score": 3,
        "factors": ["Central tourist zone", "Regular police presence", "Well-lit and maintained"],
        "level": "SAFE",
    },
    "triveni ghat": {
        "coords": (30.1036, 78.3049),
        "score": 4,
        "factors": ["Riverside location — minor flood risk in monsoon", "Heavy foot traffic — stay alert for pickpockets"],
        "level": "SAFE",
    },
    "parmarth niketan": {
        "coords": (30.1094, 78.3038),
        "score": 2,
        "factors": ["Ashram — highly secure and managed", "No major risk factors"],
        "level": "SAFE",
    },
    "tapovan": {
        "coords": (30.1374, 78.3191),
        "score": 5,
        "factors": ["Semi-urban fringe area", "Some narrow lanes", "Moderate tourist crowd"],
        "level": "MODERATE",
    },
    "aiims rishikesh": {
        "coords": (30.0869, 78.2774),
        "score": 2,
        "factors": ["Major hospital campus — highly secure", "Well-maintained roads nearby"],
        "level": "SAFE",
    },
    "rishikesh railway station": {
        "coords": (30.0869, 78.2640),
        "score": 4,
        "factors": ["Busy transit hub — watch belongings", "Well-staffed and patrolled"],
        "level": "SAFE",
    },
    "beatles ashram": {
        "coords": (30.1100, 78.3220),
        "score": 6,
        "factors": ["Forested campus — limited lighting after dark", "Isolated from main road", "Wildlife possible in surrounding forest"],
        "level": "MODERATE",
    },
    "neer waterfall": {
        "coords": (30.1580, 78.3520),
        "score": 7,
        "factors": ["Remote forest trail access", "Slippery rocks near waterfall", "No network coverage on trail", "Wildlife in surrounding jungle"],
        "level": "MODERATE",
    },
    "jumpin heights bungee": {
        "coords": (30.1450, 78.3410),
        "score": 6,
        "factors": ["Remote canyon location", "Single access road", "Managed activity — staff present", "High altitude terrain"],
        "level": "MODERATE",
    },
    "rajaji national park": {
        "coords": (30.0200, 78.2000),
        "score": 9,
        "factors": ["Dense forest — wildlife zone", "Elephants and leopards present", "No unauthorized entry", "Zero network coverage"],
        "level": "HIGH RISK",
    },
    "kunjapuri temple": {
        "coords": (30.2100, 78.3200),
        "score": 7,
        "factors": ["High altitude hilltop — 1675m", "Narrow winding road to summit", "Landslide-prone in monsoon", "Cold and foggy conditions possible"],
        "level": "MODERATE",
    },
    "neelkanth mahadev temple": {
        "coords": (30.1667, 78.3833),
        "score": 7,
        "factors": ["Deep forest location — 24km from Rishikesh", "Single mountain road", "Dense jungle surroundings", "Wildlife area"],
        "level": "MODERATE",
    },
    "shivpuri": {
        "coords": (30.1500, 78.3700),
        "score": 5,
        "factors": ["Riverside camping zone", "Rafting activity area — seasonal risk", "Well-managed by operators"],
        "level": "MODERATE",
    },
    "brahmpuri": {
        "coords": (30.1200, 78.3100),
        "score": 4,
        "factors": ["Riverside ghats", "Managed camping area", "Minor flood risk in heavy monsoon"],
        "level": "SAFE",
    },
    "swarg ashram": {
        "coords": (30.1150, 78.3100),
        "score": 3,
        "factors": ["Established ashram zone", "Pedestrian-only lanes — low traffic risk", "Well-patrolled area"],
        "level": "SAFE",
    },
    "rishikesh bus stand": {
        "coords": (30.0970, 78.2980),
        "score": 4,
        "factors": ["Busy transit point — watch belongings", "Moderate crowd density"],
        "level": "SAFE",
    },
    "market rishikesh": {
        "coords": (30.1030, 78.2990),
        "score": 5,
        "factors": ["Dense market area — pickpocket risk", "Heavy vehicular and pedestrian traffic", "Narrow lanes"],
        "level": "MODERATE",
    },
}

HEATMAP_SEEDS = [
    # ── City core — safe (low intensity) ──────────────────────────────
    (30.1036, 78.3049, 0.15),   # Triveni Ghat
    (30.1090, 78.3038, 0.15),   # Ram Jhula
    (30.1259, 78.3285, 0.20),   # Laxman Jhula (slightly crowded)
    (30.1094, 78.3038, 0.10),   # Parmarth Niketan
    (30.1150, 78.3100, 0.12),   # Swarg Ashram
    (30.0869, 78.2774, 0.10),   # AIIMS
    (30.0869, 78.2640, 0.18),   # Railway Station
    (30.0970, 78.2980, 0.20),   # Bus Stand
    (30.1030, 78.2990, 0.28),   # Market area
    (30.1200, 78.3100, 0.18),   # Brahmpuri

    # ── Semi-urban fringe — moderate (mid intensity) ───────────────────
    (30.1374, 78.3191, 0.40),   # Tapovan
    (30.1100, 78.3220, 0.50),   # Beatles Ashram
    (30.1500, 78.3700, 0.42),   # Shivpuri
    (30.1450, 78.3410, 0.52),   # Jumpin Heights
    (30.1667, 78.3833, 0.58),   # Neelkanth road

    # ── Riverside flood zone — moderate ───────────────────────────────
    (30.0950, 78.2900, 0.45),
    (30.0980, 78.2950, 0.40),
    (30.1010, 78.3000, 0.38),
    (30.1300, 78.3300, 0.42),
    (30.1400, 78.3500, 0.48),

    # ── Remote hills / forest — high risk ─────────────────────────────
    (30.1580, 78.3520, 0.72),   # Neer Waterfall trail
    (30.1700, 78.3600, 0.80),   # Deep forest
    (30.1800, 78.3700, 0.85),
    (30.1900, 78.3500, 0.88),
    (30.2100, 78.3200, 0.75),   # Kunjapuri hill
    (30.2000, 78.3000, 0.78),
    (30.1900, 78.2900, 0.70),

    # ── Rajaji National Park / dense jungle ───────────────────────────
    (30.0500, 78.2200, 0.90),
    (30.0300, 78.2000, 0.95),
    (30.0200, 78.2000, 0.95),   # Deep park interior
    (30.0100, 78.1800, 0.92),
    (30.0400, 78.2400, 0.88),
    (30.0600, 78.2500, 0.82),
    (30.0700, 78.2300, 0.78),

    # ── North hills beyond Tapovan ─────────────────────────────────────
    (30.1600, 78.3000, 0.70),
    (30.1700, 78.3100, 0.75),
    (30.1800, 78.3200, 0.80),
    (30.2200, 78.3400, 0.85),

    # ── East forest belt ──────────────────────────────────────────────
    (30.1300, 78.3800, 0.78),
    (30.1400, 78.3900, 0.82),
    (30.1500, 78.4000, 0.88),
    (30.1000, 78.3600, 0.65),
    (30.1100, 78.3700, 0.72),
]


CITY_CENTER = (30.1034, 78.2966)

def _dist_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))


def _fetch_osm_tags(lat, lon, radius=80):
    """
    Query Overpass for all OSM elements within `radius` metres of (lat,lon).
    Returns a flat dict of all tags found (merged, last-write-wins).
    Times out after 6 seconds — returns {} on failure.
    """
    query = (
        "[out:json][timeout:6];"
        "(node(around:{r},{lat},{lon});"
        "way(around:{r},{lat},{lon});"
        "relation(around:{r},{lat},{lon}););"
        "out tags;"
    ).format(r=radius, lat=lat, lon=lon)

    url = "https://overpass-api.de/api/interpreter"
    data = urllib.parse.urlencode({"data": query}).encode()
    try:
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("User-Agent", "TravelWise/1.0")
        with urllib.request.urlopen(req, timeout=7) as resp:
            result = json.loads(resp.read().decode())
        tags = {}
        for elem in result.get("elements", []):
            tags.update(elem.get("tags", {}))
        return tags
    except Exception:
        return {}

def _score_from_tags(tags: dict, dist_km: float) -> tuple:
    """Returns (score_delta, [factor_strings])"""
    delta   = 0
    factors = []

    landuse  = tags.get("landuse",  "")
    natural  = tags.get("natural",  "")
    amenity  = tags.get("amenity",  "")
    tourism  = tags.get("tourism",  "")
    highway  = tags.get("highway",  "")
    leisure  = tags.get("leisure",  "")
    place    = tags.get("place",    "")
    waterway = tags.get("waterway", "")

    if natural in ("wood", "scrub", "grassland", "heath", "fell") or landuse == "forest":
        delta += 4
        factors.append("Forest / wilderness area — wildlife possible")

    if landuse in ("conservation", "national_park", "nature_reserve") or \
       tags.get("boundary") in ("national_park", "protected_area"):
        delta += 4
        factors.append("Protected wildlife zone — restricted access")

    if waterway in ("river", "stream") or natural == "water" or landuse == "reservoir":
        delta += 2
        factors.append("Riverside / water body — flood risk in monsoon")

    if landuse in ("residential", "commercial", "retail", "industrial"):
        delta -= 1
        factors.append("Urban / residential area")

    if amenity in ("hospital", "police", "fire_station", "school", "university",
                   "place_of_worship", "temple", "bank"):
        delta -= 1
        factors.append("Staffed public facility nearby")

    if tourism in ("attraction", "hotel", "guest_house", "hostel", "information",
                   "viewpoint", "museum"):
        delta -= 1
        factors.append("Tourist infrastructure present")

    if highway in ("track", "path", "footway", "bridleway", "unclassified"):
        delta += 2
        factors.append("Unmaintained / narrow road — limited access")

    if place in ("village", "town", "city", "suburb", "neighbourhood"):
        delta -= 1
        factors.append("Populated settlement")

    if dist_km > 15:
        delta += 3
        factors.append("Very remote — >15 km from city center")
    elif dist_km > 8:
        delta += 2
        factors.append("Remote location — limited emergency response")
    elif dist_km > 4:
        delta += 1
        factors.append("Peripheral area — some distance from city services")

    return delta, factors


def _geocode(place_name: str):
    key = place_name.strip().lower()
    if key in KNOWN_PLACES:
        return KNOWN_PLACES[key]["coords"]
    try:
        from geopy.geocoders import Nominatim
        from geopy.exc import GeocoderTimedOut
        gc = Nominatim(user_agent="travelwise_risk_v2", timeout=8)
        for q in [
            place_name + ", Rishikesh, Uttarakhand, India",
            place_name + ", Rishikesh, India",
            place_name + ", Uttarakhand, India",
        ]:
            try:
                loc = gc.geocode(q)
                if loc:
                    return (loc.latitude, loc.longitude)
            except GeocoderTimedOut:
                continue
    except Exception:
        pass
    return None


def _build_map(lat, lon, place_name, score, level, color, factors) -> str:
    m = folium.Map(location=[lat, lon], zoom_start=14, tiles="OpenStreetMap")

    # Heatmap
    HeatMap(
        [[s[0], s[1], s[2]] for s in HEATMAP_SEEDS],
        radius=40,
        blur=30,
        max_zoom=16,
        min_opacity=0.40,
        gradient={
            "0.0":  "#00ff00",
            "0.25": "#80ff00",
            "0.45": "#ffff00",
            "0.65": "#ff8000",
            "0.80": "#ff4000",
            "1.0":  "#ff0000",
        },
        name="Safety Heatmap"
    ).add_to(m)

    folium.CircleMarker(
        location=[lat, lon],
        radius=16,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.50,
        weight=3,
    ).add_to(m)

    icon_map = {"green": "check", "orange": "exclamation-triangle", "red": "times"}
    popup_html = (
        "<div style='font-family:sans-serif;min-width:160px'>"
        "<b style='font-size:13px'>" + place_name + "</b><br>"
        "<span style='color:" + color + ";font-weight:700;font-size:16px'>" + str(score) + "/10</span>"
        " &nbsp;<span style='color:" + color + ";font-weight:600'>" + level + "</span><br><br>"
        "<b>Risk factors:</b><br>" +
        "".join("<span style='font-size:11px'>• " + f + "</span><br>" for f in factors) +
        "</div>"
    )
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=260),
        icon=folium.Icon(color=color, icon=icon_map.get(color, "info"), prefix="fa"),
        tooltip=place_name + " — " + level + " (" + str(score) + "/10)",
    ).add_to(m)

    level_color_map = {"SAFE": "green", "MODERATE": "orange", "HIGH RISK": "red"}
    for name, info in KNOWN_PLACES.items():
        if name == place_name.strip().lower():
            continue
        c = level_color_map.get(info["level"], "gray")
        folium.CircleMarker(
            location=info["coords"],
            radius=6,
            color=c,
            fill=True,
            fill_color=c,
            fill_opacity=0.7,
            weight=2,
            tooltip=name.title() + " — " + info["level"],
        ).add_to(m)

    legend = """
    <div style="
        position:fixed;bottom:28px;left:28px;z-index:9999;
        background:rgba(13,17,23,0.93);color:#e6edf3;
        padding:14px 18px;border-radius:12px;
        font-family:sans-serif;font-size:12px;
        border:1px solid rgba(255,255,255,0.12);
        box-shadow:0 4px 24px rgba(0,0,0,0.5);
        min-width:160px;
    ">
        <b style="font-size:13px">🛡 Safety Heatmap</b>
        <div style="margin-top:8px;line-height:1.9">
            <span style="color:#00ff00">●</span> Safe zones<br>
            <span style="color:#ffff00">●</span> Moderate risk<br>
            <span style="color:#ff8000">●</span> High risk<br>
            <span style="color:#ff0000">●</span> Danger zones<br>
        </div>
        <hr style="border-color:rgba(255,255,255,0.1);margin:8px 0">
        <b>Dots = known places</b><br>
        <span style="color:green">●</span> Safe &nbsp;
        <span style="color:orange">●</span> Moderate &nbsp;
        <span style="color:red">●</span> High Risk
    </div>"""
    m.get_root().html.add_child(folium.Element(legend))
    folium.LayerControl().add_to(m)

    return m._repr_html_()


def analyse_risk(place_name: str) -> dict:
    """
    Returns full risk report dict for a place in Rishikesh.
    Raises ValueError if place cannot be geocoded.
    """
    key = place_name.strip().lower()

    if key in KNOWN_PLACES:
        info   = KNOWN_PLACES[key]
        lat, lon = info["coords"]
        score  = info["score"]
        level  = info["level"]
        factors = list(info["factors"])
        color  = {"SAFE": "green", "MODERATE": "orange", "HIGH RISK": "red"}.get(level, "blue")
        map_html = _build_map(lat, lon, place_name, score, level, color, factors)
        return {
            "place": place_name, "lat": lat, "lon": lon,
            "score": score, "level": level, "color": color,
            "factors": factors, "map_html": map_html,
            "method": "curated"
        }

    coords = _geocode(place_name)
    if coords is None:
        raise ValueError(
            "Could not find '" + place_name + "' in Rishikesh. "
            "Try a more specific name or pick from the suggestions."
        )

    lat, lon = coords
    dist     = _dist_km(lat, lon, CITY_CENTER[0], CITY_CENTER[1])
    tags     = _fetch_osm_tags(lat, lon)

    delta, factors = _score_from_tags(tags, dist)
    score = max(1, min(10, 2 + delta))

    if not factors:
        if dist < 3:
            factors = ["Central city area — generally safe"]
        else:
            factors = ["No major risk data found — exercise normal caution"]

    if score <= 3:
        level = "SAFE";      color = "green"
    elif score <= 6:
        level = "MODERATE";  color = "orange"
    else:
        level = "HIGH RISK"; color = "red"

    map_html = _build_map(lat, lon, place_name, score, level, color, factors)

    return {
        "place": place_name, "lat": round(lat, 6), "lon": round(lon, 6),
        "score": score, "level": level, "color": color,
        "factors": factors, "map_html": map_html,
        "method": "osm"
    }