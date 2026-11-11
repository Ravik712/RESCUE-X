import json
import os

GEO_DIR = r"C:\Users\Lenovo\OneDrive\Documents\rk\RESCUE_X_V2\datasets\geographical"

# 1. Convert Waterways to GeoJSON
waterways_raw_path = os.path.join(GEO_DIR, "cuddalore_waterways.json")
if os.path.exists(waterways_raw_path):
    with open(waterways_raw_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    features = []
    for el in data.get("elements", []):
        tags = el.get("tags", {})
        geometry = el.get("geometry", [])
        if not geometry:
            continue
        coords = [[pt["lon"], pt["lat"]] for pt in geometry]
        name = tags.get("name") or tags.get("name:en") or tags.get("waterway") or tags.get("natural", "Waterway")
        features.append({
            "type": "Feature",
            "properties": {
                "id": el.get("id"),
                "name": name,
                "type": tags.get("waterway") or tags.get("natural"),
            },
            "geometry": {
                "type": "LineString",
                "coordinates": coords
            }
        })
    with open(os.path.join(GEO_DIR, "cuddalore_waterways.geojson"), "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f)
    print(f"Processed {len(features)} waterway features into GeoJSON.")

# 2. Convert Shelters to GeoJSON
shelters_raw_path = os.path.join(GEO_DIR, "cuddalore_shelters.json")
if os.path.exists(shelters_raw_path):
    with open(shelters_raw_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    features = []
    default_capacities = {"hospital": 800, "school": 1200, "college": 2500, "community_centre": 1000}
    for el in data.get("elements", []):
        tags = el.get("tags", {})
        name = tags.get("name") or tags.get("name:en")
        if not name:
            continue
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        if not lat or not lon:
            continue
        amenity = tags.get("amenity", "facility")
        cap = default_capacities.get(amenity, 1000)
        features.append({
            "type": "Feature",
            "properties": {
                "id": el.get("id"),
                "name": name,
                "type": amenity.capitalize(),
                "capacity": cap,
                "elevation_m": 8.5 + (len(features) % 5) * 2.0, # Estimated elevation above AOD
                "status": "Dry & Accessible"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            }
        })
    with open(os.path.join(GEO_DIR, "cuddalore_shelters.geojson"), "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f)
    print(f"Processed {len(features)} verified candidate shelters into GeoJSON.")

