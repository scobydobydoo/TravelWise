import sys
import json
import osmnx as ox

try:
    source_name = sys.argv[1]
    destination_name = sys.argv[2]

    print("Loading Rishikesh map...")
    G = ox.graph_from_place("Rishikesh, Uttarakhand, India", network_type='drive')
    print("Graph loaded")

    def get_point(place):
        try:
            return ox.geocode(place + ", Rishikesh, India")
        except:
            print(f"⚠️ Geocoding failed for {place}, using fallback")
            return None

    source_point = get_point(source_name)
    destination_point = get_point(destination_name)

    nodes_list = list(G.nodes(data=True))

    if source_point is None:
        source_point = (nodes_list[0][1]["y"], nodes_list[0][1]["x"])
    if destination_point is None:
        destination_point = (nodes_list[-1][1]["y"], nodes_list[-1][1]["x"])

    source_node = ox.distance.nearest_nodes(G, source_point[1], source_point[0])
    destination_node = ox.distance.nearest_nodes(G, destination_point[1], destination_point[0])

    def get_speed(data):
        speed = data.get("maxspeed")

        if speed:
            if isinstance(speed, list):
                speed = speed[0]
            try:
                return float(speed)
            except:
                pass

        highway = data.get("highway", "")
        if isinstance(highway, list):
            highway = highway[0]

        speed_map = {
            "motorway": 80,
            "trunk": 60,
            "primary": 50,
            "secondary": 40,
            "tertiary": 30,
            "residential": 25,
            "service": 20
        }

        return speed_map.get(highway, 30)

    nodes = []
    edges = []

    print("Building graph...")

    for node, data in G.nodes(data=True):
        nodes.append({
            "id": int(node),
            "lat": data.get("y"),
            "lon": data.get("x")
        })

    for u, v, data in G.edges(data=True):
        length = data.get("length", 1)
        speed = get_speed(data)

        time = length / (speed * 1000 / 3600)  # seconds

        edges.append({
            "from": int(u),
            "to": int(v),
            "weight": time,
            "length": length
        })

    graph_data = {
        "source_node": int(source_node),
        "destination_node": int(destination_node),
        "nodes": nodes,
        "edges": edges
    }

    with open("graph.json", "w") as f:
        json.dump(graph_data, f, indent=4)

    print("Graph saved")

except Exception as e:
    print("ERROR:", str(e))
    exit(1)