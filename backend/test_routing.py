import json
import os
import networkx as nx
import numpy as np

GEO_DIR = r"C:\Users\Lenovo\OneDrive\Documents\rk\RESCUE_X_V2\datasets\geographical"
roads_path = os.path.join(GEO_DIR, "cuddalore_roads.geojson")

with open(roads_path, "r", encoding="utf-8") as f:
    roads_data = json.load(f)

print(f"Total road features: {len(roads_data['features'])}")

# Build NetworkX Graph
G = nx.Graph()

for feat in roads_data["features"]:
    coords = feat["geometry"]["coordinates"]
    props = feat["properties"]
    for i in range(len(coords) - 1):
        u = (round(coords[i][0], 5), round(coords[i][1], 5))
        v = (round(coords[i+1][0], 5), round(coords[i+1][1], 5))
        # Compute euclidean distance in meters approx (at latitude 11.7 deg)
        dx = (v[0] - u[0]) * 111320 * np.cos(np.radians(11.75))
        dy = (v[1] - u[1]) * 110574
        dist = np.sqrt(dx**2 + dy**2)
        if dist > 0:
            G.add_edge(u, v, length=dist, road_id=props.get("id"), name=props.get("name"))

print(f"NetworkX Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
print(f"Connected components: {nx.number_connected_components(G)}")

# Get the largest connected component
largest_cc = max(nx.connected_components(G), key=len)
subG = G.subgraph(largest_cc).copy()
print(f"Largest Component: {subG.number_of_nodes()} nodes, {subG.number_of_edges()} edges")

# Test Dijkstra routing between two distant nodes in the largest component
nodes_list = list(subG.nodes())
start_node = nodes_list[0]
end_node = nodes_list[-1]

path = nx.dijkstra_path(subG, start_node, end_node, weight="length")
length = nx.dijkstra_path_length(subG, start_node, end_node, weight="length")
print(f"Test Route: {len(path)} steps, {length:.1f} meters ({length/1000:.2f} km)")

