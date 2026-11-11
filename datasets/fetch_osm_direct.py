import urllib.request
import xml.etree.ElementTree as ET
import json
import os

GEO_DIR = r"C:\Users\Lenovo\OneDrive\Documents\rk\RESCUE_X_V2\datasets\geographical"
os.makedirs(GEO_DIR, exist_ok=True)

# Cuddalore City & Old Town bounding box: [min_lon, min_lat, max_lon, max_lat]
bbox = "79.755,11.735,79.785,11.765"
url = f"https://api.openstreetmap.org/api/0.6/map?bbox={bbox}"

print(f"Fetching direct OSM XML from {url}...")
req = urllib.request.Request(url, headers={"User-Agent": "RescueXAcademicGIS/2.0"})

try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        xml_data = resp.read()
    
    xml_path = os.path.join(GEO_DIR, "cuddalore_osm_raw.xml")
    with open(xml_path, "wb") as f:
        f.write(xml_data)
    print(f"Saved {len(xml_data)} bytes of direct OSM data to {xml_path}")
    
    # Parse XML into nodes and ways
    root = ET.fromstring(xml_data)
    nodes = {}
    for node in root.findall("node"):
        nid = node.get("id")
        lat = float(node.get("lat"))
        lon = float(node.get("lon"))
        nodes[nid] = (lon, lat)
    
    print(f"Parsed {len(nodes)} OSM nodes.")
    
    # Extract roads
    road_features = []
    building_features = []
    
    for way in root.findall("way"):
        wid = way.get("id")
        tags = {t.get("k"): t.get("v") for t in way.findall("tag")}
        nd_refs = [nd.get("ref") for nd in way.findall("nd")]
        coords = [nodes[ref] for ref in nd_refs if ref in nodes]
        
        if len(coords) < 2:
            continue
            
        if "highway" in tags:
            road_features.append({
                "type": "Feature",
                "properties": {
                    "id": wid,
                    "name": tags.get("name", "Unnamed Road"),
                    "highway": tags.get("highway"),
                    "maxspeed": tags.get("maxspeed", "30")
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": coords
                }
            })
        elif "building" in tags:
            building_features.append({
                "type": "Feature",
                "properties": {
                    "id": wid,
                    "building": tags.get("building"),
                    "height": float(tags.get("height", 10.0)) if tags.get("height", "").replace(".", "").isdigit() else 12.0
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords]
                }
            })
            
    print(f"Extracted {len(road_features)} genuine road segments.")
    print(f"Extracted {len(building_features)} genuine building footprints.")
    
    # Save GeoJSON files
    with open(os.path.join(GEO_DIR, "cuddalore_roads.geojson"), "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": road_features}, f)
        
    with open(os.path.join(GEO_DIR, "cuddalore_buildings.geojson"), "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": building_features}, f)
        
    print("GeoJSON files saved successfully!")

except Exception as e:
    print(f"Error fetching direct OSM: {e}")

