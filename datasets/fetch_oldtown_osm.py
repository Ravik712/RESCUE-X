import urllib.request
import xml.etree.ElementTree as ET
import json
import os

GEO_DIR = r"C:\Users\Lenovo\OneDrive\Documents\rk\RESCUE_X_V2\datasets\geographical"

# Query Old Town + Port (11.710 to 11.740 N, 79.755 to 79.790 E)
url = "https://api.openstreetmap.org/api/0.6/map?bbox=79.755,11.710,79.790,11.740"
print(f"Fetching Cuddalore Old Town & Port from {url}...")
req = urllib.request.Request(url, headers={"User-Agent": "RescueXAcademicGIS/2.0"})

try:
    with urllib.request.urlopen(req, timeout=45) as resp:
        xml_data = resp.read()
    
    xml_path = os.path.join(GEO_DIR, "cuddalore_oldtown_osm.xml")
    with open(xml_path, "wb") as f:
        f.write(xml_data)
        
    root = ET.fromstring(xml_data)
    nodes = {}
    for node in root.findall("node"):
        nid = node.get("id")
        lat = float(node.get("lat"))
        lon = float(node.get("lon"))
        nodes[nid] = (lon, lat)
        
    print(f"Old Town parsed {len(nodes)} nodes.")
    
    # Load existing roads and buildings
    roads_path = os.path.join(GEO_DIR, "cuddalore_roads.geojson")
    with open(roads_path, "r", encoding="utf-8") as f:
        existing_roads = json.load(f)
        
    buildings_path = os.path.join(GEO_DIR, "cuddalore_buildings.geojson")
    with open(buildings_path, "r", encoding="utf-8") as f:
        existing_buildings = json.load(f)
        
    existing_road_ids = {f["properties"]["id"] for f in existing_roads["features"]}
    existing_bldg_ids = {f["properties"]["id"] for f in existing_buildings["features"]}
    
    new_roads = 0
    new_bldgs = 0
    
    for way in root.findall("way"):
        wid = way.get("id")
        tags = {t.get("k"): t.get("v") for t in way.findall("tag")}
        nd_refs = [nd.get("ref") for nd in way.findall("nd")]
        coords = [nodes[ref] for ref in nd_refs if ref in nodes]
        
        if len(coords) < 2:
            continue
            
        if "highway" in tags and wid not in existing_road_ids:
            existing_roads["features"].append({
                "type": "Feature",
                "properties": {
                    "id": wid,
                    "name": tags.get("name", "Unnamed Street"),
                    "highway": tags.get("highway"),
                    "maxspeed": tags.get("maxspeed", "30")
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": coords
                }
            })
            existing_road_ids.add(wid)
            new_roads += 1
            
        elif "building" in tags and wid not in existing_bldg_ids:
            h = 10.0
            if "height" in tags:
                try:
                    h = float(tags["height"].replace("m", "").strip())
                except:
                    pass
            elif "building:levels" in tags:
                try:
                    h = float(tags["building:levels"]) * 3.2
                except:
                    pass
            else:
                # Realistic urban building height: 8m to 20m based on id hash
                h = 8.0 + (int(wid) % 5) * 3.0
                
            existing_buildings["features"].append({
                "type": "Feature",
                "properties": {
                    "id": wid,
                    "building": tags.get("building"),
                    "height": h,
                    "flooded": False
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords]
                }
            })
            existing_bldg_ids.add(wid)
            new_bldgs += 1
            
    print(f"Added {new_roads} new road segments from Old Town (Total: {len(existing_roads['features'])})")
    print(f"Added {new_bldgs} new building footprints from Old Town (Total: {len(existing_buildings['features'])})")
    
    with open(roads_path, "w", encoding="utf-8") as f:
        json.dump(existing_roads, f)
        
    with open(buildings_path, "w", encoding="utf-8") as f:
        json.dump(existing_buildings, f)
        
    print("Updated GeoJSON files successfully!")
    
except Exception as e:
    print(f"Error fetching Old Town OSM: {e}")

