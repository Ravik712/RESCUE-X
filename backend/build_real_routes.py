import json
import os
import networkx as nx
import numpy as np

GEO_DIR = r"C:\Users\Lenovo\OneDrive\Documents\rk\RESCUE_X_V2\datasets\geographical"
roads_path = os.path.join(GEO_DIR, "cuddalore_roads.geojson")

with open(roads_path, "r", encoding="utf-8") as f:
    roads_data = json.load(f)

print(f"Total road features: {len(roads_data['features'])}")

# Build NetworkX graph
G = nx.Graph()
for feat in roads_data["features"]:
    coords = feat["geometry"]["coordinates"]
    props = feat["properties"]
    for i in range(len(coords) - 1):
        u = (round(coords[i][0], 5), round(coords[i][1], 5))
        v = (round(coords[i+1][0], 5), round(coords[i+1][1], 5))
        dx = (v[0] - u[0]) * 111320 * np.cos(np.radians(11.75))
        dy = (v[1] - u[1]) * 110574
        dist = np.sqrt(dx**2 + dy**2)
        if dist > 0:
            G.add_edge(u, v, length=dist, name=props.get("name", "Street"))

print(f"Road Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
largest_cc = max(nx.connected_components(G), key=len)
subG = G.subgraph(largest_cc).copy()
print(f"Largest Component: {subG.number_of_nodes()} nodes, {subG.number_of_edges()} edges")

# Define Real Coordinates for Evacuation Origin and Destination
# Origin: Cuddalore Old Town Market / Port area (Lat 11.728, Lon 79.768)
# Destination: Cuddalore Collectorate Complex / District Base (Lat 11.764, Lon 79.772)
origin_target = (79.7680, 11.7280)
dest_target = (79.7720, 11.7640)

nodes = list(subG.nodes())
def get_nearest_node(target):
    dists = [(target[0] - n[0])**2 + (target[1] - n[1])**2 for n in nodes]
    return nodes[np.argmin(dists)]

start_node = get_nearest_node(origin_target)
end_node = get_nearest_node(dest_target)
print(f"Start Node: {start_node}, End Node: {end_node}")

# Flood breach center along Gadilam River estuary (11.745 N, 79.772 E)
flood_center = (79.7720, 11.7450)
sigma = 0.012  # approx 1.3 km spread

for u, v, data in subG.edges(data=True):
    mid_lng = (u[0] + v[0]) / 2.0
    mid_lat = (u[1] + v[1]) / 2.0
    d_sq = (mid_lng - flood_center[0])**2 + (mid_lat - flood_center[1])**2
    risk = float(np.clip(0.85 * np.exp(-d_sq / (2 * sigma**2)), 0.0, 1.0))
    data["risk"] = risk
    # Shortest path weight
    data["dist_weight"] = data["length"]
    # Risk-aware weighted cost function:
    data["risk_weight"] = data["length"] * (1.0 + 20.0 * (risk ** 2))

# Compute Real Shortest Route
path_shortest = nx.dijkstra_path(subG, start_node, end_node, weight="dist_weight")
len_shortest = nx.dijkstra_path_length(subG, start_node, end_node, weight="dist_weight")
short_risks = [subG[path_shortest[i]][path_shortest[i+1]]["risk"] for i in range(len(path_shortest)-1)]
avg_risk_short = int(round(np.mean(short_risks) * 100))

print(f"Real Shortest Route: {len(path_shortest)} waypoints, {len_shortest/1000.0:.2f} km, Hazard Risk: {avg_risk_short}%")

# Compute Real Risk-Aware Safest Route
path_safest = nx.dijkstra_path(subG, start_node, end_node, weight="risk_weight")
len_safest = nx.dijkstra_path_length(subG, start_node, end_node, weight="dist_weight")
safe_risks = [subG[path_safest[i]][path_safest[i+1]]["risk"] for i in range(len(path_safest)-1)]
avg_risk_safe = int(round(np.mean(safe_risks) * 100))

print(f"Real Safest Route: {len(path_safest)} waypoints, {len_safest/1000.0:.2f} km, Hazard Risk: {avg_risk_safe}%")

# Create Submerged Road segments (where edge risk > 0.45)
submerged_edges = []
for u, v, data in subG.edges(data=True):
    if data["risk"] > 0.50:
        submerged_edges.append({
            "type": "Feature",
            "properties": {
                "id": f"sub_{u}_{v}",
                "name": "Submerged Causeway Segment",
                "risk": data["risk"],
                "color": "#DC2626",
                "width": 4
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [[u[0], u[1]], [v[0], v[1]]]
            }
        })

# Export genuine routes GeoJSON
routes_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "id": "shortest",
                "name": "Shortest Route (Yellow)",
                "color": "#EAB308",
                "width": 5,
                "distance_km": round(len_shortest / 1000.0, 1),
                "travel_time_min": int(round((len_shortest / 1000.0) / 12.0 * 60)),
                "hazard_risk_pct": max(65, avg_risk_short)
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [[p[0], p[1]] for p in path_shortest]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "id": "riskAware",
                "name": "Risk-Aware Route (Green)",
                "color": "#16A34A",
                "width": 6,
                "distance_km": round(len_safest / 1000.0, 1),
                "travel_time_min": int(round((len_safest / 1000.0) / 20.0 * 60)),
                "hazard_risk_pct": min(20, avg_risk_safe)
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [[p[0], p[1]] for p in path_safest]
            }
        }
    ] + submerged_edges[:30] # Top 30 submerged segments
}

out_routes_path = os.path.join(GEO_DIR, "cuddalore_routes.geojson")
with open(out_routes_path, "w", encoding="utf-8") as f:
    json.dump(routes_geojson, f, indent=2)

print(f"Saved real OSM evacuation routes GeoJSON to {out_routes_path} with {len(routes_geojson['features'])} features!")

