"""
TravelWise — fetch_graph.py  (FIXED)

KEY FIXES in this version:
  1. Rishikesh bounding-box validation: if Nominatim returns coordinates
     outside Rishikesh (e.g. 21°N for Nagpur instead of 30°N), the result
     is rejected and the next broader query is tried.
  2. Known-landmark fallback table: hard-coded (lat, lon) for the most
     common Rishikesh tourist spots so geocoding never fails for them.
  3. All errors to stderr; clean JSON to stdout — Flask reads stdout.
  4. ox.settings.use_cache = True (unchanged from previous version).
"""

import sys
import json

# ── Validate args first ────────────────────────────────────────────────────────
if len(sys.argv) < 3:
    print("Usage: python fetch_graph.py <source> <destination>", file=sys.stderr)
    sys.exit(1)

source_name      = sys.argv[1].strip()
destination_name = sys.argv[2].strip()

if not source_name or not destination_name:
    print("ERROR: source and destination cannot be empty", file=sys.stderr)
    sys.exit(1)

# ── Imports ────────────────────────────────────────────────────────────────────
try:
    import osmnx as ox
except ImportError:
    print("ERROR: osmnx not installed. Run: pip install osmnx", file=sys.stderr)
    sys.exit(1)

try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError
except ImportError:
    print("ERROR: geopy not installed. Run: pip install geopy", file=sys.stderr)
    sys.exit(1)

# ── osmnx settings ─────────────────────────────────────────────────────────────
ox.settings.use_cache   = True
ox.settings.log_console = False

# ── Rishikesh bounding box (generous margin) ───────────────────────────────────
# Rishikesh is roughly 30.05°N – 30.20°N, 78.20°E – 78.40°E
RISHIKESH_BOUNDS = {
    "lat_min": 29.95,
    "lat_max": 30.35,
    "lon_min": 78.10,
    "lon_max": 78.55,
}

def in_rishikesh(lat: float, lon: float) -> bool:
    b = RISHIKESH_BOUNDS
    return b["lat_min"] <= lat <= b["lat_max"] and b["lon_min"] <= lon <= b["lon_max"]

# ── Hard-coded fallback coords for common Rishikesh landmarks ─────────────────
# Use these when Nominatim geocodes to the wrong city / country.
KNOWN_PLACES = {
    # bridges
    "laxman jhula":              (30.11927, 78.32209),
    "laxman jhula bridge":       (30.11927, 78.32209),
    "ram jhula":                 (30.10800, 78.30580),
    "ram jhula bridge":          (30.10800, 78.30580),
    "shivanand jhula":           (30.10800, 78.30580),
    # ghats / temples
    "triveni ghat":              (30.10344, 78.30191),
    "parmarth niketan":          (30.10622, 78.30416),
    "neelkanth mahadev temple":  (30.17694, 78.37639),
    # areas / localities
    "tapovan":                   (30.13386, 78.32063),
    "swargashram":               (30.10680, 78.30660),
    "muni ki reti":              (30.11100, 78.30300),
    "rishikesh":                 (30.08675, 78.26777),
    "rishikesh railway station": (30.07728, 78.27219),
    "rishikesh bus stand":       (30.08540, 78.27090),
    # attractions
    "beatles ashram":            (30.10590, 78.30010),
    "neer waterfall":            (30.15200, 78.34000),
    "jumpin heights":            (30.15897, 78.34639),
    "jumpin heights bungee":     (30.15897, 78.34639),
    "aiims rishikesh":           (30.06978, 78.28494),
    "rajaji national park":      (30.02000, 78.20000),
}

def lookup_known(name: str):
    """Return (lat, lon) from the hard-coded table, case-insensitive."""
    key = name.lower().strip()
    # exact match
    if key in KNOWN_PLACES:
        return KNOWN_PLACES[key]
    # partial match — longest key that is a substring of the query wins
    best_key, best_len = None, 0
    for k in KNOWN_PLACES:
        if k in key and len(k) > best_len:
            best_key, best_len = k, len(k)
    if best_key:
        return KNOWN_PLACES[best_key]
    return None

# ── Geocoder ───────────────────────────────────────────────────────────────────
geocoder = Nominatim(user_agent="travelwise_rishikesh_v2", timeout=10)

def geocode_place(name: str):
    """
    1. Check hard-coded landmark table first.
    2. Try Nominatim with progressively broader queries.
    3. Validate every result is inside the Rishikesh bounding box.
    Returns (lat, lon) or None.
    """
    # 1. Known landmark fast-path
    known = lookup_known(name)
    if known:
        print(f"  Known-landmark '{name}' → {known}", file=sys.stderr)
        return known

    # 2. Nominatim with bounding-box validation
    queries = [
        f"{name}, Rishikesh, Uttarakhand, India",
        f"{name}, Rishikesh, India",
        f"{name}, Uttarakhand, India",
    ]
    for q in queries:
        try:
            loc = geocoder.geocode(q)
            if loc:
                lat, lon = loc.latitude, loc.longitude
                if in_rishikesh(lat, lon):
                    print(f"  Geocoded '{name}' via Nominatim → ({lat:.4f}, {lon:.4f})",
                          file=sys.stderr)
                    return (lat, lon)
                else:
                    print(f"  Nominatim result for '{q}' is OUTSIDE Rishikesh "
                          f"({lat:.4f}, {lon:.4f}) — skipping", file=sys.stderr)
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"  Geocoder warning for '{q}': {e}", file=sys.stderr)

    return None


def get_speed(data: dict) -> float:
    speed = data.get("maxspeed")
    if speed:
        if isinstance(speed, list):
            speed = speed[0]
        try:
            return float(str(speed).split()[0])
        except (ValueError, IndexError):
            pass
    highway = data.get("highway", "")
    if isinstance(highway, list):
        highway = highway[0]
    speed_map = {
        "motorway": 80, "trunk": 60, "primary": 50,
        "secondary": 40, "tertiary": 30, "unclassified": 25,
        "residential": 25, "service": 20, "living_street": 15, "track": 15,
    }
    return speed_map.get(str(highway), 30)


# ── Main ───────────────────────────────────────────────────────────────────────
try:
    print("Fetching OSM graph for Rishikesh...", file=sys.stderr)
    G = ox.graph_from_place("Rishikesh, Uttarakhand, India", network_type="drive")
    print(f"Graph loaded: {len(G.nodes)} nodes, {len(G.edges)} edges", file=sys.stderr)

    print(f"Geocoding '{source_name}'...", file=sys.stderr)
    source_point = geocode_place(source_name)

    print(f"Geocoding '{destination_name}'...", file=sys.stderr)
    destination_point = geocode_place(destination_name)

    # Hard failure if either point is unresolvable
    if source_point is None:
        print(f"ERROR: could not geocode '{source_name}' within Rishikesh. "
              "Try a more specific name.", file=sys.stderr)
        sys.exit(1)

    if destination_point is None:
        print(f"ERROR: could not geocode '{destination_name}' within Rishikesh. "
              "Try a more specific name.", file=sys.stderr)
        sys.exit(1)

    # Snap to nearest graph nodes
    source_node = ox.distance.nearest_nodes(G, X=source_point[1],  Y=source_point[0])
    destination_node = ox.distance.nearest_nodes(G, X=destination_point[1], Y=destination_point[0])

    print(f"Source node:      {source_node}", file=sys.stderr)
    print(f"Destination node: {destination_node}", file=sys.stderr)

    if source_node == destination_node:
        print("ERROR: source and destination resolved to the same graph node. "
              "Try more specific place names.", file=sys.stderr)
        sys.exit(1)

    # Build nodes
    nodes_out = [
        {"id": int(n), "lat": float(d.get("y", 0)), "lon": float(d.get("x", 0))}
        for n, d in G.nodes(data=True)
    ]

    # Build edges
    edges_out = []
    for u, v, data in G.edges(data=True):
        length = float(data.get("length", 1))
        speed  = get_speed(data)
        time   = length / (speed * 1000.0 / 3600.0)
        edges_out.append({"from": int(u), "to": int(v), "weight": time, "length": length})

    graph_data = {
        "source_node":      int(source_node),
        "destination_node": int(destination_node),
        "nodes":            nodes_out,
        "edges":            edges_out,
    }

    with open("graph.json", "w", encoding="utf-8") as f:
        json.dump(graph_data, f)

    print(f"graph.json written: {len(nodes_out)} nodes, {len(edges_out)} edges", file=sys.stderr)
    print(f"OK source_node={source_node} dest_node={destination_node}")

except KeyboardInterrupt:
    print("Interrupted", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    import traceback
    traceback.print_exc(file=sys.stderr)
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)