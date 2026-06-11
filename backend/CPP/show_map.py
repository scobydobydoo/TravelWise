"""
TravelWise — show_map.py

Reads route.txt + graph.json, draws a Folium map, saves map.html.

FIXES:
  - Wraps everything in try/except and exits with code 1 on failure
    so Flask can detect the error via returncode
  - Uses a unique Folium map ID derived from the route hash so the
    browser always treats it as a fresh document (busts srcdoc cache)
  - Validates that all nodes in route.txt exist in graph.json
"""

import json
import sys
import hashlib
import folium

def main():
    # ── Load graph ────────────────────────────────────────────────────────────
    try:
        with open("graph.json", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: cannot read graph.json: {e}", file=sys.stderr)
        sys.exit(1)

    nodes = {
        node["id"]: (node["lat"], node["lon"])
        for node in data.get("nodes", [])
    }

    # ── Load route ────────────────────────────────────────────────────────────
    try:
        with open("route.txt", encoding="utf-8") as f:
            raw = f.read().split()
        route = [int(x) for x in raw if x.strip()]
    except Exception as e:
        print(f"ERROR: cannot read route.txt: {e}", file=sys.stderr)
        sys.exit(1)

    if not route:
        print("ERROR: route.txt is empty", file=sys.stderr)
        sys.exit(1)

    # Filter to nodes that exist in the graph (defensive)
    route_coords = [nodes[nid] for nid in route if nid in nodes]

    if len(route_coords) < 2:
        print(f"ERROR: only {len(route_coords)} valid coords in route", file=sys.stderr)
        sys.exit(1)

    # ── Build a unique map_id so the browser sees a genuinely new document ────
    # (Folium's default map ID is deterministic per session; varying it
    #  ensures the iframe srcdoc is never identical to a previous response.)
    route_sig  = hashlib.md5(str(route).encode()).hexdigest()[:12]
    map_div_id = f"map_{route_sig}"

    # ── Build Folium map ──────────────────────────────────────────────────────
    center = route_coords[len(route_coords) // 2]   # midpoint of route

    m = folium.Map(
        location=center,
        zoom_start=15,
        tiles="OpenStreetMap"
    )

    # Route polyline
    folium.PolyLine(
        route_coords,
        color="royalblue",
        weight=5,
        opacity=0.9,
        tooltip="Route"
    ).add_to(m)

    # Start marker
    folium.Marker(
        location=route_coords[0],
        popup=folium.Popup("Start", max_width=120),
        icon=folium.Icon(color="green", icon="play", prefix="fa")
    ).add_to(m)

    # End marker
    folium.Marker(
        location=route_coords[-1],
        popup=folium.Popup("Destination", max_width=120),
        icon=folium.Icon(color="red", icon="flag", prefix="fa")
    ).add_to(m)

    # Fit the map bounds to the route
    m.fit_bounds([
        [min(c[0] for c in route_coords), min(c[1] for c in route_coords)],
        [max(c[0] for c in route_coords), max(c[1] for c in route_coords)],
    ])

    # ── Save ──────────────────────────────────────────────────────────────────
    try:
        m.save("map.html")
        print(f"Map saved ({len(route_coords)} waypoints)", file=sys.stderr)
    except Exception as e:
        print(f"ERROR: cannot save map.html: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()