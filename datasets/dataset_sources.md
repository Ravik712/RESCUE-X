# RESCUE-X Datasets & Sources Ledger

**Geographical Focus:** Cuddalore City & Old Town, Tamil Nadu, India  
**Coordinates:** $11.715^\circ\text{ N} - 11.775^\circ\text{ N}, 79.735^\circ\text{ E} - 79.815^\circ\text{ E}$

---

## 1. Historical Rainfall Dataset

- **Primary Source:** ECMWF ERA5 Reanalysis Meteorological Archive & IMD Daily Station Observations via Open-Meteo Historical API.
- **Station / Point of Reference:** Cuddalore Weather Station Coordinates ($11.748^\circ\text{ N}, 79.771^\circ\text{ E}$).
- **Period:** January 1, 2015 to December 31, 2024 (10 Complete Years, 3,653 daily observations).
- **Recorded Parameters:**
  - `date`: ISO observation date (`YYYY-MM-DD`).
  - `precipitation_mm`: Total daily precipitation in millimeters.
  - `rain_mm`: Liquid rainfall component.
  - `precipitation_hours`: Duration of precipitation event in hours.
  - `wind_speed_max_kmh`: Peak wind gust at 10m altitude.
  - `rolling_3d_rain_mm`: 3-day antecedent moisture precipitation index.
  - `rolling_7d_rain_mm`: 7-day cumulative precipitation index.
  - `imd_category`: Official India Meteorological Department classification (No Rain, Light, Moderate, Heavy, Very Heavy, Extremely Heavy).
  - `is_extreme_outlier`: Statistical IQR flag ($Q_3 + 1.5 \times \text{IQR}$).
- **Verified Historic Deluges in Dataset:**
  - **Cyclone Nivar:** November 25, 2020 ($175.7\text{ mm/day}$, $49.0\text{ km/h}$ gusts).
  - **Cyclone Fengal:** November 30, 2024 ($151.0\text{ mm/day}$).
  - **Historic 2015 South India Flood Event:** November 9, 2015 ($142.7\text{ mm/day}$, causing catastrophic inundation across Gadilam & Pennaiyar basins).
  - **Northeast Monsoon Surge:** November 1, 2022 ($128.1\text{ mm/day}$).

---

## 2. Geographical Infrastructure Datasets

- **Primary Source:** OpenStreetMap (OSM) Contributors & Overpass API.
- **Bounding Box:** $11.71^\circ\text{ N} - 11.78^\circ\text{ N}, 79.73^\circ\text{ E} - 79.81^\circ\text{ E}$ (EPSG:4326 / WGS 84).
- **Components Extracted:**
  1. **Road Network (`cuddalore_roads.geojson`):** 905 genuine road segments classified by OSM highway taxonomy (`primary`, `secondary`, `tertiary`, `residential`, `trunk`).
  2. **Building Footprints (`cuddalore_buildings.geojson`):** 227 genuine building polygons in central Cuddalore and Old Town with height extrusions ($8\text{ m} - 28\text{ m}$).
  3. **Waterways & Coastline (`cuddalore_waterways.geojson`):** 172 line/polygon geometries detailing the **Gadilam River**, **Pennaiyar River**, **Uppanar Canal**, and the **Bay of Bengal Coastline**.
  4. **Emergency Shelters & Medical Hubs (`cuddalore_shelters.geojson`):** 68 verified facilities across Cuddalore including:
     - St. Joseph Higher Secondary School
     - Cuddalore Collectorate Complex
     - Government Arts College
     - Vandipalayam Community Hall
     - Cuddalore Government Headquarters Hospital

---

## 3. Flood Disaster Reference Documentation

- **Official Reference:** District Disaster Management Plan (DDMP), Cuddalore District, Revenue & Disaster Management Department, Government of Tamil Nadu.
- **ISRO/NRSC Flood Atlas:** Historical flood extent maps from IRS-1C/1D and RISAT-1 radar satellites documenting Gadilam and Pennaiyar flood plain inundation.
- **Data Integrity Statement:**
  - Raw records (`datasets/raw/`) are preserved intact and unmodified.
  - Processed records (`datasets/processed/`) undergo documented Pandas type conversion, imputation, and outlier detection.
  - No synthetic or fabricated rainfall records are claimed as real observations.

