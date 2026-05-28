import osmnx as ox
import folium

# -----------------------------
# INPUT PLACE
# -----------------------------

place = input("Enter place in Rishikesh: ")

full_place = place + ", Rishikesh, Uttarakhand, India"

# -----------------------------
# GEOCODE LOCATION
# -----------------------------

try:
    lat, lon = ox.geocode(full_place)

except:
    print("Place not found!")
    exit()

print(f"\nAnalyzing risk for: {place}")
print(f"Coordinates: {lat}, {lon}")

# -----------------------------
# RISK ANALYSIS
# -----------------------------

risk = 2
reasons = []

# Tourist zones
if 30.120 <= lat <= 30.140 and 78.320 <= lon <= 78.340:
    risk += 4
    reasons.append("Heavy tourist congestion")

# Riverside / flood-prone
if 30.090 <= lat <= 30.115 and 78.285 <= lon <= 78.310:
    risk += 3
    reasons.append("Flood-prone riverside area")

# Hilly terrain
if lat < 30.050:
    risk += 2
    reasons.append("Hilly terrain")

# Narrow roads zone
if 30.100 <= lat <= 30.130:
    risk += 1
    reasons.append("Narrow roads / traffic bottlenecks")

risk = min(risk, 10)

# -----------------------------
# RISK LEVEL
# -----------------------------

if risk <= 3:
    level = "SAFE"
    color = "green"

elif risk <= 6:
    level = "MODERATE"
    color = "orange"

else:
    level = "HIGH RISK"
    color = "red"

# -----------------------------
# REPORT
# -----------------------------

print("\n========== RISK REPORT ==========")
print(f"Place       : {place}")
print(f"Risk Score  : {risk}/10")
print(f"Risk Level  : {level}")

print("\nRisk Factors:")

if reasons:
    for r in reasons:
        print(f"- {r}")
else:
    print("- No major risks detected")

print("=================================\n")

# -----------------------------
# MAP VISUALIZATION
# -----------------------------

m = folium.Map(location=[lat, lon], zoom_start=15)

folium.CircleMarker(
    location=[lat, lon],
    radius=15,
    color=color,
    fill=True,
    fill_opacity=0.7,
    popup=f"{place}\nRisk: {risk}/10"
).add_to(m)

folium.Marker(
    [lat, lon],
    popup=f"{place} ({level})"
).add_to(m)

m.save("risk_map.html")

print("Risk map saved as risk_map.html")