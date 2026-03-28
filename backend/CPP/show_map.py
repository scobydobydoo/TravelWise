import json
import folium

with open("graph.json") as f:
    data = json.load(f)

nodes = {node["id"]: (node["lat"], node["lon"]) for node in data["nodes"]}

with open("route.txt") as f:
    route = list(map(int, f.read().split()))

route_coords = [nodes[node] for node in route if node in nodes]

m = folium.Map(location=route_coords[0], zoom_start=14)

folium.PolyLine(route_coords, color="blue", weight=5).add_to(m)

folium.Marker(route_coords[0], popup="Start", icon=folium.Icon(color='green')).add_to(m)
folium.Marker(route_coords[-1], popup="End", icon=folium.Icon(color='red')).add_to(m)

m.save("map.html")

print("Map saved as map.html")