# RESCUE-X: Real-World 3D Flood Intelligence & Evacuation Decision Support System

**Course Project:** Data Science with Python (Value Added Course)  
**Geographical Focus:** Cuddalore City & Old Town, Tamil Nadu, India ($11.715^\circ\text{ N} - 11.775^\circ\text{ N}, 79.735^\circ\text{ E} - 79.815^\circ\text{ E}$)  
**UI Reference:** Google Stitch Design (`18302644753448032741`), faithfully recreated with **Cambria** typography, MapLibre 3D GIS vector rendering, and responsive disaster command analytics.

---

## 1. Executive Summary

During severe cyclones and monsoonal surges along the Bay of Bengal coast, municipal authorities and disaster responders face significant challenges identifying submerged road arteries and deploying timely evacuation protocols. Traditional static emergency maps fail to capture non-linear inundation spread or dynamically compare physical travel distances against hazardous flood exposures.

**RESCUE-X** provides an interactive, end-to-end 3D geospatial intelligence platform tailored specifically to the vulnerable estuarine terrain of **Cuddalore District, Tamil Nadu**. It fuses:
1. **10 Years of Genuine Daily Meteorological Observations (2015-2024)**.
2. **7,846 OpenStreetMap Geographic Nodes & 905 Road Segments**.
3. **227 Real 3D Extruded Building Footprints & 172 Waterway Geometries (Gadilam River, Pennaiyar River, Uppanar Canal, Bay of Bengal)**.
4. **68 Verified Candidate Emergency Shelters & Hospitals**.
5. **Two External Regional Reference Locations:** **IFET College of Engineering** (Academic Partner, Villupuram) and **Puducherry City** (Union Territory Coastal Center) with instant camera fly-to navigation and search.
6. **NetworkX Dijkstra Dual Evacuation Routing Engine** (Shortest vs. Risk-Aware Safest Route).
7. **Transparent Empirical Hydrological Flood Plume Simulation**.

---

## 2. System Architecture

```mermaid
flowchart TD
    subgraph Data Layer [Data Science & GIS Storage]
        D1[datasets/raw/cuddalore_rainfall_raw.csv<br/>3,653 daily meteorological records]
        D2[datasets/processed/cuddalore_rainfall_cleaned.csv<br/>Pandas cleaned: rolling 3d/7d, IMD classes, IQR outliers]
        D3[datasets/geographical/*.geojson<br/>905 roads, 227 buildings, 172 waterways, 68 shelters]
    end

    subgraph Backend Core [Python FastAPI Server :8000]
        B1[GET /api/health - Server health & GIS stats]
        B2[GET /api/rainfall/summary - Statistical analysis]
        B3[GET /api/gis/layers - Vector GeoJSON server]
        B4[POST /api/simulation/run - Empirical flood risk model]
        B5[POST /api/routing/compare - NetworkX Dijkstra routing]
    end

    subgraph Frontend Client [Stitch UI Engine]
        UI1[Top Header & Live FastAPI Health Status Pill]
        UI2[Summary KPI Cards: Population, Submerged Roads, Shelters]
        UI3[MapLibre GL JS 3D Vector Canvas with Cambria Styling]
        UI4[Interactive Flood Controls: Intensity, Spread, Origin]
        UI5[Dual Route Evaluation Cards: Shortest vs Risk-Aware]
        UI6[Plotly & Chart.js Analytics: Deluges, Exposure Tiers, Route Times]
    end

    D1 & D2 & D3 --> Backend Core
    Backend Core <--> Frontend Client
```

---

## 3. Data Science with Python Concepts Demonstrated

| Concept | Python Tool / Library | Implementation in RESCUE-X |
| :--- | :--- | :--- |
| **Data Cleaning** | `Pandas` | Date-time indexing, null value handling, duplicate checks, rolling 3-day and 7-day soil saturation cumulative indices ($R_{3d}, R_{7d}$), IMD rainfall category mapping. |
| **Statistical Analysis** | `NumPy`, `Pandas` | Mean, standard deviation, max single-day precipitation ($175.7\text{ mm}$ during Cyclone Nivar), 90th & 99th percentile computation, IQR cyclonic outlier filtering. |
| **Spatial Graph Modeling** | `NetworkX` | Graph topology built from 905 genuine road segments ($4,111\text{ nodes}, 4,639\text{ edges}$). Largest connected component extraction ($3,843\text{ nodes}$). |
| **Evacuation Routing** | `NetworkX` | Dijkstra's algorithm computing both unweighted shortest physical path and risk-penalized safest path. |
| **Data Visualization** | `Matplotlib`, `Plotly`, `Chart.js` | 10-year precipitation trends, 2015 Historic Flood deluge profile, route travel times vs. hazard exposures, population exposure distribution across risk tiers. |
| **GIS Data Processing** | `GeoPandas`, `Shapely` | OpenStreetMap vector extraction, polygon building heights, waterway proximity buffers. |
| **Backend Integration** | `FastAPI`, `Uvicorn` | RESTful API endpoints with CORS, asynchronous endpoints, and static HTML serving. |

---

## 4. Mathematical Modeling & Transparent Formulas

### 4.1 Empirical Flood Risk Estimation
> **Disclaimer:** This is an empirical decision-support heuristic combining precipitation saturation, proximity to drainage channels, and topography. It is designed for academic decision modeling and is not claimed to be a full Navier-Stokes hydrodynamic solver.

$$\text{Risk}(u) = \min\left(1.0, \;\frac{I}{100} \cdot e^{-\frac{d_{\text{origin}}^2}{2\sigma^2}} \cdot \left[0.70 + 0.30 \cdot e^{-\frac{d_{\text{waterway}}^2}{2 \cdot 0.4^2}}\right] \cdot \lambda_{\text{rain}}\right)$$

Where:
- $I$: Scenario flood intensity slider ($10\% - 100\%$).
- $d_{\text{origin}}$: Distance in km from the selected flood breach origin (e.g. Gadilam River Bridge, Thenpennai Estuary, or Silver Beach tidal surge).
- $\sigma$: Spread radius parameter ($1.0\text{ km} - 6.0\text{ km}$).
- $d_{\text{waterway}}$: Orthogonal distance to the nearest natural drainage channel.
- $\lambda_{\text{rain}}$: Antecedent precipitation saturation factor from historical observations.

### 4.2 NetworkX Dual-Path Routing Engine
1. **Shortest Route (Yellow on Map):**
   $$W_{\text{dist}}(e) = \text{length}(e)$$
   Minimizes physical road distance. Passable in early flood phases, but exposed to low-lying causeway inundation.

2. **Risk-Aware Safest Route (Green on Map):**
   $$W_{\text{risk}}(e) = \text{length}(e) \cdot \left(1.0 + \alpha \cdot \bar{r}_e^\beta\right)$$
   Where:
   - $\bar{r}_e = \frac{r_u + r_v}{2}$ is the average flood risk on road edge $e=(u, v)$.
   - $\alpha = 15.0$ (steep penalty multiplier).
   - $\beta = 2.0$ (quadratic penalty deterring submerged road segments).
   - The algorithm automatically routes traffic along elevated ridges (such as the Vandipalayam Bypass) to ensure $100\%$ all-weather viability.

---

## 5. Project Directory Structure

```
RESCUE_X_V2/
├── backend/
│   ├── main.py                  # FastAPI server with all REST endpoints & static frontend mount
│   └── test_routing.py          # Standalone NetworkX graph routing verification script
├── datasets/
│   ├── raw/
│   │   └── cuddalore_rainfall_2015_2024_raw.csv   # Raw meteorological dataset (3,653 days)
│   ├── processed/
│   │   └── cuddalore_rainfall_cleaned.csv        # Cleaned dataset with rolling 3d/7d, IMD tags
│   ├── geographical/
│   │   ├── cuddalore_roads.geojson               # 905 genuine road segments
│   │   ├── cuddalore_buildings.geojson           # 227 3D extruded building polygons
│   │   ├── cuddalore_waterways.geojson           # 172 waterways (Gadilam, Pennaiyar, Uppanar, Bay)
│   │   ├── cuddalore_shelters.geojson            # 68 verified schools, hospitals, community centres
│   │   └── cuddalore_osm_raw.xml                 # Raw OpenStreetMap XML (1.97 MB)
│   ├── dataset_sources.md       # Complete data sources ledger and verification documentation
│   ├── fetch_gis_data.py        # Automated Overpass GIS extractor
│   └── process_gis_layers.py    # GeoJSON normalization script
├── frontend/
│   ├── index.html               # Stitch UI implementation (Cambria font, MapLibre 3D, Chart.js)
│   └── build_frontend.py        # Build script embedding live backend sync into Stitch template
├── notebooks/
│   ├── data_science_analysis.ipynb   # Complete student coursework Jupyter Notebook
│   ├── generate_course_visualizations.py # Matplotlib & Plotly generation script
│   ├── deluge_2015_analysis.html     # Interactive Plotly 2015 Historic Flood chart
│   └── route_comparison_analysis.html# Interactive Plotly Route Clearance chart
├── documentation/
│   ├── IMPLEMENTATION_PLAN.md   # Architectural design document
│   ├── VIVA_EXPLANATION.md      # Comprehensive Viva defense presentation guide
│   └── figures/
│       └── rainfall_trend_analysis.png # High-res 10-year rainfall trend chart
├── run_server.py                # Single-command launcher for backend + frontend
├── test_e2e.py                  # Automated 6-point end-to-end integration test
└── README.md                    # Project documentation (this file)
```

---

## 6. How to Run the Application

### Option A: Complete Live Application (Recommended)
Launch the unified FastAPI server, which hosts both the REST backend and the Stitch UI frontend on a single port:

```bash
cd RESCUE_X_V2
python run_server.py
```

Then open your browser at:
👉 **`http://127.0.0.1:8000`**

- The navigation bar status pill will pulse green: `Cuddalore Core: Real 3D GIS Active | Ref Points: IFET & Pondy`.
- The 3D MapLibre map renders extruded buildings, waterways, road networks, candidate shelters, and external reference markers.
- **Quick Navigation Buttons:** Click **Go to IFET** or **Go to Pondy** to smoothly fly the 3D camera to the external reference locations and view their information popups! Click **Cuddalore Basin** to return to the core flood study area.
- **Location Search:** Use the search bar in the map header to quickly search for IFET, Pondy, Cuddalore Old Town, Collectorate, or Silver Beach with auto-complete and keyboard navigation.
- Adjusting the **Flood Intensity** slider, **Spread Radius**, or **Flood Origin** and clicking **Run Simulation** updates the live inundation mesh, KPI cards, and Chart.js analytics via the Python backend!
- Clicking **Highlight on 3D Map** under either route dynamically queries NetworkX Dijkstra paths and animates the camera along the evacuation corridor.

### Option B: Standalone Frontend
You can also directly open `RESCUE_X_V2/frontend/index.html` in Google Chrome, Microsoft Edge, or Firefox. It contains built-in graceful fallbacks that function immediately even without the server running.

### Option C: Jupyter Notebook Evaluation
Open and execute the data science coursework notebook:

```bash
cd RESCUE_X_V2/notebooks
jupyter notebook data_science_analysis.ipynb
```

### Option D: Run Automated Integration Verification
```bash
python RESCUE_X_V2/test_e2e.py
```
Outputs instant `[PASS]` verification across all 6 core API endpoints and frontend assets.
