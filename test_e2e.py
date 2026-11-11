import time
import requests
import subprocess
import sys
import os

print("--- STARTING END-TO-END VERIFICATION OF RESCUE-X V2 ---")

# Start uvicorn server as subprocess
cmd = [sys.executable, "-m", "uvicorn", "RESCUE_X_V2.backend.main:app", "--host", "127.0.0.1", "--port", "8000"]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

try:
    print("Waiting for FastAPI server to initialize on http://127.0.0.1:8000...")
    time.sleep(3)
    
    # 1. Test Root (Frontend HTML)
    r_root = requests.get("http://127.0.0.1:8000/", timeout=5)
    assert r_root.status_code == 200, f"Root returned {r_root.status_code}"
    assert "RESCUE-X" in r_root.text, "RESCUE-X title not in HTML"
    assert "cuddalore-map" in r_root.text, "Map canvas not in HTML"
    assert "chart-population-risk" in r_root.text, "Chart canvas not in HTML"
    print(f"[PASS] Frontend HTML served at '/' ({len(r_root.text)} bytes, Status {r_root.status_code})")

    # 2. Test /api/health
    r_health = requests.get("http://127.0.0.1:8000/api/health", timeout=5)
    assert r_health.status_code == 200, f"Health returned {r_health.status_code}"
    h_data = r_health.json()
    assert h_data["status"] == "online"
    print(f"[PASS] /api/health: {h_data['osm_nodes_count']} nodes, {h_data['osm_edges_count']} edges, {h_data['shelters_count']} shelters, {h_data['rainfall_records_count']} rainfall records")

    # 3. Test /api/rainfall/summary
    r_rain = requests.get("http://127.0.0.1:8000/api/rainfall/summary", timeout=5)
    assert r_rain.status_code == 200
    rain_data = r_rain.json()
    assert rain_data["total_days"] == 3653
    print(f"[PASS] /api/rainfall/summary: 3,653 days, Max single day = {rain_data['max_single_day_mm']} mm, Rainy days = {rain_data['rainy_days']}")

    # 4. Test /api/gis/layers
    r_gis = requests.get("http://127.0.0.1:8000/api/gis/layers", timeout=5)
    assert r_gis.status_code == 200
    gis_data = r_gis.json()
    print(f"[PASS] /api/gis/layers: {len(gis_data['waterways']['features'])} waterways, {len(gis_data['shelters']['features'])} shelters, {len(gis_data['buildings']['features'])} buildings")

    # 5. Test /api/simulation/run
    sim_payload = {"intensity": 80, "spread_radius_km": 4.5, "origin": "gadilam", "scenario": "heavy"}
    r_sim = requests.post("http://127.0.0.1:8000/api/simulation/run", json=sim_payload, timeout=5)
    assert r_sim.status_code == 200
    sim_data = r_sim.json()
    print(f"[PASS] /api/simulation/run: Water peak = {sim_data['water_peak_m_aod']}m, Area = {sim_data['inundation_area_sqkm']} sq.km, Exposed pop = {sim_data['exposed_population']}")

    # 6. Test /api/routing/compare
    route_payload = {"intensity": 80}
    r_route = requests.post("http://127.0.0.1:8000/api/routing/compare", json=route_payload, timeout=5)
    assert r_route.status_code == 200
    route_data = r_route.json()
    print(f"[PASS] /api/routing/compare: Shortest = {route_data['shortest_route']['distance_km']} km (Hazard {route_data['shortest_route']['hazard_risk_pct']}%), Safest = {route_data['risk_aware_route']['distance_km']} km (Hazard {route_data['risk_aware_route']['hazard_risk_pct']}%)")

    print("\nALL 6 ENDPOINTS AND FRONTEND ASSETS VERIFIED WITH 100% SUCCESS!")

finally:
    proc.terminate()
    proc.wait()
    print("Test server stopped cleanly.")

