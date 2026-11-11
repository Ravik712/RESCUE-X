import urllib.request
import json
import os

GEO_DIR = r"C:\Users\Lenovo\OneDrive\Documents\rk\RESCUE_X_V2\datasets\geographical"
os.makedirs(GEO_DIR, exist_ok=True)
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def run_query(query, filename):
    print(f"Fetching {filename}...")
    req = urllib.request.Request(
        OVERPASS_URL,
        data=query.encode("utf-8"),
        headers={"User-Agent": "RescueXAcademicGIS/2.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
        path = os.path.join(GEO_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        print(f"Saved {filename} with {len(data.get('elements', []))} elements.")
        return data
    except Exception as e:
        print(f"Failed {filename}: {e}")
        return None

# Fetch arterial roads
roads_q = """[out:json][timeout:45];
(
  way["highway"="primary"](11.71,79.73,11.78,79.80);
  way["highway"="secondary"](11.71,79.73,11.78,79.80);
  way["highway"="tertiary"](11.71,79.73,11.78,79.80);
  way["highway"="trunk"](11.71,79.73,11.78,79.80);
);
out geom;"""
run_query(roads_q, "cuddalore_roads.json")

# Fetch representative real buildings
buildings_q = """[out:json][timeout:45];
(
  way["building"](11.735,79.755,11.765,79.785);
);
out geom 300;"""
run_query(buildings_q, "cuddalore_buildings.json")
