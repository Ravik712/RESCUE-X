# RESCUE-X V2 – Architecture & Implementation Plan

**Project:** RESCUE-X – Real-World 3D Flood Intelligence and Evacuation Decision Support System  
**Academic Context:** Data Science with Python Value Added Course  
**Focus Area:** Cuddalore City & Old Town, Tamil Nadu, India  
**Design Reference:** Google Stitch Project (`18302644753448032741`)  

---

## 1. Phase 1: Inspection & Findings

### 1.1 Stitch UI Inspection Status
- **Target URL:** `https://stitch.google.com/projects/18302644753448032741`
- **Inspection Outcome:** The URL was probed directly. Stitch by Google requires active Google Account authentication (`https://accounts.google.com/ServiceLogin`) to load the internal canvas RPCs (`/_/Nemo` / WebChannel). Unauthenticated requests receive the SPA shell without the interactive project canvas.
- **Protocol Adherence:** Following prompt instruction:
  > *"If the URL cannot be accessed, ask me to provide exported HTML/CSS or screenshots. Do not invent a replacement design."*
- **Action Required from User:** Please provide the exported HTML/CSS zip or paste the screenshots/markup of the Stitch UI. We will integrate it directly into `RESCUE_X_V2/frontend`.

### 1.2 Existing Project (`RESCUE_X_Starter_Project`) Inspection
- **Starter Components:** Inspected `RESCUE_X_Starter_Project (9).zip` (found in local downloads).
  - Used an $11 \times 11$ synthetic grid in Streamlit (`app.py`).
  - Lacked real geospatial coordinates (used abstract coordinates $0-10$).
  - Simple synthetic Gaussian plume with generic Plotly 3D scatter.
- **Key Shortcomings Addressed in V2:**
  1. Replaced generic Streamlit dashboard with a dedicated high-performance frontend matching Stitch design.
  2. Integrated real OpenStreetMap (OSM) vector data for Cuddalore Old Town & City (roads, 3D extruded building footprints, waterways).
  3. Integrated genuine historical meteorological rainfall observations (e.g. November-December 2015 deluge, Cyclone Nivar 2020).
  4. Applied the mandated **Cambria** font typography, strict card hierarchy, and multi-layer 3D GIS visualization.

---

## 2. Phase 2: System Architecture & Design Components

```mermaid
flowchart TD
    subgraph Data Layer
        A1[Historical IMD / ERA5 Rainfall Data] --> B1[Pandas Cleaning & Stats Pipeline]
        A2[OSM / OSMnx Cuddalore Road Network] --> B2[NetworkX Graph Construction]
        A3[OSM Building Footprints & Waterways] --> B3[GeoPandas Spatial Risk Overlay]
    end

    subgraph Backend Engine [FastAPI 0.141]
        B1 --> C1[Rainfall Analytics Endpoint]
        B2 & B3 --> C2[Empirical Flood Risk Modeler]
        C2 --> C3[Dual Routing Engine: Shortest vs Safest]
    end

    subgraph Frontend Client [Stitch UI - React / MapLibre / Cambria]
        D1[Top Navigation & Emergency Status Bar]
        D2[3D GIS Canvas: Extruded Buildings & Inundation]
        D3[Interactive Simulation Controls: Intensity, Spread, Origin]
        D4[Plotly Analytics: Rainfall Deluge & Risk Profiles]
        D5[Evacuation Decision Panel: Shortest vs Safest Comparison]
    end

    C1 & C2 & C3 <--> Frontend Client
```

---

## 3. Genuine Datasets & Spatial Scope

### 3.1 Geographic Target: Cuddalore, Tamil Nadu
- **Coordinates:** $11.7157^\circ\text{ N}, 79.7711^\circ\text{ E}$ (Old Town / Port) to $11.7557^\circ\text{ N}, 79.8111^\circ\text{ E}$ (New Town / Manjakuppam).
- **Key Waterways:**
  - **Gadilam River:** Traverses through Cuddalore, empties into the Bay of Bengal.
  - **Pennaiyar River:** Major northern drainage basin prone to severe discharge.
  - **Uppanar Canal / Estuary:** Coastal backwater flanking Cuddalore Old Town.
  - **Bay of Bengal Coastline:** Storm surge interface.

### 3.2 Dataset Collection Plan
| Dataset | Source | Temporal / Spatial Coverage | Format & Verification |
| :--- | :--- | :--- | :--- |
| **Historical Daily Rainfall** | IMD Station Records / Open-Meteo ERA5 Reanalysis | 2015 to 2024 (covers Nov 2015 142.7 mm/day deluge, Cyclone Nivar, Michaung) | Cleaned CSV (date, precipitation_mm, rain_hours) |
| **Road Network** | OpenStreetMap via OSMnx | Drive & pedestrian network for Cuddalore & Old Town | GeoJSON / NetworkX graph |
| **Building Footprints** | OSM Building polygons | Heights, building classes, centroid coordinates | GeoJSON with 3D extrusion heights |
| **Candidate Shelters & Hospitals** | OSM Amenities (`hospital`, `clinic`, `school`, `community_centre`) | Cuddalore City & Old Town verified facilities | GeoJSON with capacity estimations |
| **Waterway & Waterbodies** | OSM Natural waterways (`river`, `canal`, `coastline`) | Gadilam, Pennaiyar, Uppanar | GeoJSON lines & polygons |

---

## 4. Data Science with Python Implementation

### 4.1 Data Cleaning & Preprocessing (Pandas & NumPy)
- **Missing Value Strategy:** Forward-fill short sensor gaps; flag and document missing historical days.
- **Duplicate Removal:** Unique index constraints on `(station_id, observation_date)`.
- **Outlier Analysis:** Interquartile Range (IQR) checks on precipitation to isolate extreme cyclonic events (e.g. $>100\text{ mm/day}$).
- **Feature Engineering:** Rolling 3-day and 7-day cumulative precipitation indices ($R_{3d}$, $R_{7d}$) representing soil saturation before peak inundation.

### 4.2 Transparent Flood Scenario Model
> [!NOTE]
> This is a transparent empirical decision-support model combining rainfall saturation, proximity to drainage channels, and elevation thresholds. It does not claim to be a Navier-Stokes hydrodynamic simulation.

$$\text{Risk}(u) = \min\left(1.0, \;\frac{I}{100} \cdot e^{-\frac{d_{\text{water}}^2}{2\sigma^2}} \cdot \left[1 + \max\left(0, \frac{h_{\text{crit}} - h_{\text{elev}}}{h_{\text{crit}}}\right)\right] \cdot \lambda_{\text{rain}}\right)$$

Where:
- $I$: Scenario flood intensity control ($0-100\%$).
- $d_{\text{water}}$: Distance from node $u$ to nearest active waterway (Gadilam / Uppanar / coastline).
- $\sigma$: Spread radius parameter.
- $h_{\text{elev}}$: Topographic elevation (meters above sea level).
- $h_{\text{crit}}$: Inundation threshold elevation (default $6.0\text{ m}$).
- $\lambda_{\text{rain}}$: Rainfall saturation scaling factor derived from cumulative historical or simulated precipitation.

### 4.3 Evacuation Routing Engine (NetworkX)
We compute two concurrent paths from selected origins to candidate high-ground shelters:
1. **Shortest Route:**
   $$W_{\text{dist}}(e) = \text{length}(e)$$
   Minimizes physical road distance via Dijkstra's algorithm.

2. **Risk-Aware Safest Route:**
   $$W_{\text{risk}}(e) = \text{length}(e) \cdot \left(1 + \alpha \cdot \bar{r}_e^\beta\right)$$
   Where:
   - $\bar{r}_e = \frac{r_u + r_v}{2}$ is the average flood risk on road edge $e=(u,v)$.
   - $\alpha = 10.0$ (risk penalty multiplier).
   - $\beta = 2.0$ (exponential penalty for high inundation risk, deterring submerged segments).

3. **Routing Evaluation Metrics:**
   - Physical Distance ($\text{km}$).
   - Estimated Travel Time ($\text{minutes}$ at assumed walking speed $4.5\text{ km/h}$ or emergency vehicle speed $25\text{ km/h}$, adjusted for water impediment).
   - Mean & Peak Flood Exposure along route ($\%$).

---

## 5. UI & Presentation Requirements
- **Typography:** **Cambria** as specified for primary headings, metric values, navigation badges, and card captions.
- **Color Palette & Theme:** Professional emergency response command-center dark/light theme (Slate/Navy, Crimson/Amber alerts, Cyan/Emerald safe zones).
- **Controls & Interactions:**
  - Flood Intensity slider ($0-100\%$).
  - Flood Spread Radius slider ($500\text{ m} - 5000\text{ m}$).
  - Flood Origin dropdown (e.g., Gadilam River Breach, Old Town Port Surge, Pennaiyar Basin, Custom coordinate).
  - Evacuation Origin & Shelter Destination selectors.
  - Interactive 3D building extrusion layer toggle, flood heatmap toggle, candidate shelter marker toggles.
  - Reset to baseline scenario button.
- **Analytics Dashboards (Plotly):**
  - Historical rainfall timeline with major cyclonic events highlighted.
  - Evacuation Route risk profile comparison (Distance vs. Time vs. Exposure).
  - Population exposure breakdown across risk tiers (Low, Medium, High, Severe).

---

## 6. Execution Phases & Milestones

- [x] **Phase 1:** Inspect Stitch URL and starter project (Completed).
- [x] **Phase 2:** Report findings and present comprehensive implementation plan (Current).
- [ ] **Phase 3:** Collect and validate genuine Cuddalore datasets (IMD/ERA5 rainfall, OSM road networks, building footprints, waterways, candidate shelters).
- [ ] **Phase 4:** Build Python FastAPI backend with Pandas, NumPy, GeoPandas, and NetworkX.
- [ ] **Phase 5:** Recreate and integrate Stitch UI layout with Cambria font and MapLibre 3D GIS canvas.
- [ ] **Phase 6:** Connect frontend controls and map layers to backend REST endpoints.
- [ ] **Phase 7:** End-to-end integration testing, browser verification, and error remediation.
- [ ] **Phase 8:** Comprehensive documentation, viva presentation guide, and dataset source ledger.

