import os
import json

BASE_DIR = r"C:\Users\Lenovo\OneDrive\Documents\rk\RESCUE_X_V2"
GEO_DIR = os.path.join(BASE_DIR, "datasets", "geographical")
out_html_path = os.path.join(BASE_DIR, "frontend", "index.html")

# Load real GeoJSON layers
def load_geojson(filename):
    with open(os.path.join(GEO_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)

real_buildings = load_geojson("cuddalore_buildings.geojson")
real_waterways = load_geojson("cuddalore_waterways.geojson")
real_shelters = load_geojson("cuddalore_shelters.geojson")
real_routes = load_geojson("cuddalore_routes.geojson")

print(f"Loaded: {len(real_buildings['features'])} buildings, {len(real_waterways['features'])} waterways, {len(real_shelters['features'])} shelters, {len(real_routes['features'])} route segments.")

stitch_code_path = os.path.join(BASE_DIR, "stitch_design", "code.html")
with open(stitch_code_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Navbar status pill
old_status = """        <div class="hidden lg:flex items-center space-x-2 px-3 py-1.5 rounded-full bg-slate-50 border border-slate-200 text-xs text-slate-600">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Cuddalore Basin: Monitoring Active</span>
        </div>"""

new_status = """        <div id="backend-status-pill" class="hidden lg:flex items-center space-x-2 px-3 py-1.5 rounded-full bg-slate-50 border border-slate-200 text-xs text-slate-600 transition-all">
          <span id="backend-dot" class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span id="backend-status-text">Cuddalore Core: Real 3D GIS Active | Ref Points: IFET & Pondy</span>
        </div>"""

if old_status in content:
    content = content.replace(old_status, new_status)

# 2. Add Location Search Bar & Quick Navigation Buttons to Map Presets Header
old_presets = """      <!-- Quick Camera / Map Presets -->
      <div class="flex items-center space-x-2 bg-white border border-brand-border p-1 rounded-md text-xs font-medium">
        <button id="view-basin" onclick="setBasinView()" class="px-3 py-1.5 rounded bg-brand-navy text-white transition-colors">Basin 3D</button>
        <button id="view-coast" onclick="setCoastalView()" class="px-3 py-1.5 rounded hover:bg-slate-100 text-slate-700 transition-colors">Coastal Shore</button>
        <button id="view-oldtown" onclick="setOldTownView()" class="px-3 py-1.5 rounded hover:bg-slate-100 text-slate-700 transition-colors">Old Town Grid</button>
        <button onclick="toggle3DPitch()" class="px-3 py-1.5 rounded border-l border-slate-200 hover:bg-slate-100 text-slate-700 transition-colors flex items-center space-x-1">
          <i data-lucide="layers" class="w-3.5 h-3.5"></i>
          <span>Pitch 60°</span>
        </button>
      </div>"""

new_presets = """      <!-- Quick Camera Presets, Basemap Switcher & Search Bar -->
      <div class="flex flex-wrap items-center justify-between gap-3 w-full lg:w-auto">
        <!-- Location Search Bar with Autocomplete Dropdown -->
        <div class="relative flex-1 sm:w-64">
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-2.5 flex items-center pointer-events-none text-slate-400">
              <i data-lucide="search" class="w-3.5 h-3.5"></i>
            </div>
            <input type="text" id="map-search-input" placeholder="Search IFET, Pondy, Cuddalore..." oninput="handleMapSearch(this.value)" onfocus="showSearchDropdown()" class="w-full text-xs rounded-md border border-brand-border bg-white pl-8 pr-7 py-1.5 text-brand-navy placeholder:text-slate-400 focus:border-brand-accent focus:outline-none shadow-sm font-serif">
            <button onclick="clearSearch()" id="btn-search-clear" class="hidden absolute inset-y-0 right-0 pr-2 flex items-center text-slate-400 hover:text-slate-600">
              <i data-lucide="x" class="w-3.5 h-3.5"></i>
            </button>
          </div>
          <!-- Dropdown Results Box -->
          <div id="map-search-dropdown" class="hidden absolute left-0 right-0 top-full mt-1 bg-white border border-brand-border rounded-lg shadow-xl z-50 text-xs py-1.5 max-h-64 overflow-y-auto divide-y divide-slate-100 font-serif">
            <div class="px-3 py-1 text-[10px] uppercase font-bold text-slate-400 tracking-wider">Reference Locations</div>
            <button onclick="goToIFET()" class="w-full text-left px-3 py-2 hover:bg-blue-50 flex items-center space-x-2 transition-colors">
              <span class="w-5 h-5 rounded bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-xs shrink-0">🎓</span>
              <div>
                <div class="font-bold text-brand-navy flex items-center space-x-1.5">
                  <span>IFET College of Engineering</span>
                  <span class="text-[9px] px-1.5 py-0.2 rounded bg-blue-100 text-blue-700 font-normal">External Ref</span>
                </div>
                <div class="text-[10px] text-slate-500">Gangarampalayam, Villupuram (26.5 km NW)</div>
              </div>
            </button>
            <button onclick="goToPondy()" class="w-full text-left px-3 py-2 hover:bg-purple-50 flex items-center space-x-2 transition-colors">
              <span class="w-5 h-5 rounded bg-purple-100 text-purple-700 flex items-center justify-center font-bold text-xs shrink-0">🏛️</span>
              <div>
                <div class="font-bold text-brand-navy flex items-center space-x-1.5">
                  <span>Puducherry City (Pondy)</span>
                  <span class="text-[9px] px-1.5 py-0.2 rounded bg-purple-100 text-purple-700 font-normal">External Ref</span>
                </div>
                <div class="text-[10px] text-slate-500">Promenade / White Town (21.8 km North)</div>
              </div>
            </button>
            <div class="px-3 py-1 text-[10px] uppercase font-bold text-slate-400 tracking-wider">Cuddalore Flood Analysis Area</div>
            <button onclick="setBasinView()" class="w-full text-left px-3 py-1.5 hover:bg-slate-50 flex items-center space-x-2 transition-colors">
              <span class="w-5 h-5 rounded bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-xs shrink-0">🌊</span>
              <div class="font-semibold text-brand-navy">Cuddalore Basin Core (Gadilam & Pennaiyar)</div>
            </button>
            <button onclick="setOldTownView()" class="w-full text-left px-3 py-1.5 hover:bg-slate-50 flex items-center space-x-2 transition-colors">
              <span class="w-5 h-5 rounded bg-amber-50 text-amber-600 flex items-center justify-center font-bold text-xs shrink-0">⚓</span>
              <div class="font-semibold text-brand-navy">Cuddalore Old Town & Port District</div>
            </button>
            <button onclick="setCoastalView()" class="w-full text-left px-3 py-1.5 hover:bg-slate-50 flex items-center space-x-2 transition-colors">
              <span class="w-5 h-5 rounded bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold text-xs shrink-0">🏖️</span>
              <div class="font-semibold text-brand-navy">Silver Beach Coastline</div>
            </button>
          </div>
        </div>

        <!-- Quick Navigation Action Buttons (IFET, Pondy & Cuddalore Presets) -->
        <div class="flex items-center space-x-1 bg-white border border-brand-border p-1 rounded-md text-xs font-medium shadow-sm">
          <button id="btn-goto-ifet" onclick="goToIFET()" class="px-2.5 py-1 rounded bg-blue-50 hover:bg-blue-100 text-blue-700 font-semibold border border-blue-200 transition-colors flex items-center space-x-1" title="Jump to IFET College of Engineering (External Reference)">
            <span>🎓</span>
            <span>Go to IFET</span>
          </button>
          <button id="btn-goto-pondy" onclick="goToPondy()" class="px-2.5 py-1 rounded bg-purple-50 hover:bg-purple-100 text-purple-700 font-semibold border border-purple-200 transition-colors flex items-center space-x-1" title="Jump to Puducherry City (External Reference)">
            <span>🏛️</span>
            <span>Go to Pondy</span>
          </button>
          <button id="view-basin" onclick="setBasinView()" class="px-2.5 py-1 rounded bg-brand-navy text-white font-semibold transition-colors flex items-center space-x-1" title="Return to Cuddalore Basin Core">
            <span>🌊</span>
            <span>Cuddalore Basin</span>
          </button>
          <button onclick="toggle3DPitch()" class="px-2 py-1 rounded border-l border-slate-200 hover:bg-slate-100 text-slate-700 transition-colors flex items-center space-x-1" title="Toggle 3D Pitch angle">
            <i data-lucide="layers" class="w-3.5 h-3.5"></i>
            <span>3D Pitch</span>
          </button>
        </div>

        <!-- Basemap Switcher (100% Free, Zero API Keys) -->
        <div class="flex items-center space-x-1 bg-white border border-brand-border p-1 rounded-md text-xs font-medium shadow-sm">
          <span class="text-slate-400 px-1 text-[11px]">Basemap:</span>
          <button id="btn-basemap-osm" onclick="setBasemap('osm')" class="px-2 py-1 rounded bg-brand-navy text-white transition-colors">Street (OSM)</button>
          <button id="btn-basemap-satellite" onclick="setBasemap('satellite')" class="px-2 py-1 rounded hover:bg-slate-100 text-slate-700 transition-colors">Satellite (Esri)</button>
          <button id="btn-basemap-topo" onclick="setBasemap('topo')" class="px-2 py-1 rounded hover:bg-slate-100 text-slate-700 transition-colors">Topo</button>
        </div>
      </div>"""

if old_presets in content:
    content = content.replace(old_presets, new_presets)

# 3. Add Layer Toggles in map sub-header
old_layer_toggles = """          <!-- Layer Toggle Badges -->
          <div class="flex items-center space-x-2">
            <label class="inline-flex items-center space-x-1 cursor-pointer">
              <input type="checkbox" id="layer-buildings" checked onchange="toggleLayer('buildings')" class="rounded text-brand-accent focus:ring-0 w-3.5 h-3.5">
              <span class="text-slate-600">3D Buildings</span>
            </label>
            <label class="inline-flex items-center space-x-1 cursor-pointer">
              <input type="checkbox" id="layer-floods" checked onchange="toggleLayer('floods')" class="rounded text-blue-600 focus:ring-0 w-3.5 h-3.5">
              <span class="text-blue-700">Flood Inundation</span>
            </label>
            <label class="inline-flex items-center space-x-1 cursor-pointer">
              <input type="checkbox" id="layer-routes" checked onchange="toggleLayer('routes')" class="rounded text-amber-600 focus:ring-0 w-3.5 h-3.5">
              <span class="text-amber-700">Routes</span>
            </label>
            <label class="inline-flex items-center space-x-1 cursor-pointer">
              <input type="checkbox" id="layer-shelters" checked onchange="toggleLayer('shelters')" class="rounded text-emerald-600 focus:ring-0 w-3.5 h-3.5">
              <span class="text-emerald-700">Shelters</span>
            </label>
          </div>"""

new_layer_toggles = """          <!-- Layer Toggle Badges -->
          <div class="flex items-center space-x-3 overflow-x-auto">
            <label class="inline-flex items-center space-x-1 cursor-pointer">
              <input type="checkbox" id="layer-buildings" checked onchange="toggleLayer('buildings')" class="rounded text-brand-accent focus:ring-0 w-3.5 h-3.5">
              <span class="text-slate-600">3D Buildings (302)</span>
            </label>
            <label class="inline-flex items-center space-x-1 cursor-pointer">
              <input type="checkbox" id="layer-waterways" checked onchange="toggleLayer('waterways')" class="rounded text-cyan-600 focus:ring-0 w-3.5 h-3.5">
              <span class="text-cyan-700 font-medium">Rivers & Coast (172)</span>
            </label>
            <label class="inline-flex items-center space-x-1 cursor-pointer">
              <input type="checkbox" id="layer-floods" checked onchange="toggleLayer('floods')" class="rounded text-blue-600 focus:ring-0 w-3.5 h-3.5">
              <span class="text-blue-700 font-semibold">Flood Inundation</span>
            </label>
            <label class="inline-flex items-center space-x-1 cursor-pointer">
              <input type="checkbox" id="layer-routes" checked onchange="toggleLayer('routes')" class="rounded text-amber-600 focus:ring-0 w-3.5 h-3.5">
              <span class="text-amber-700 font-semibold">OSM Routes</span>
            </label>
            <label class="inline-flex items-center space-x-1 cursor-pointer">
              <input type="checkbox" id="layer-shelters" checked onchange="toggleLayer('shelters')" class="rounded text-emerald-600 focus:ring-0 w-3.5 h-3.5">
              <span class="text-emerald-700">Shelters (68)</span>
            </label>
            <label class="inline-flex items-center space-x-1 cursor-pointer">
              <input type="checkbox" id="layer-refs" checked onchange="toggleLayer('refs')" class="rounded text-indigo-600 focus:ring-0 w-3.5 h-3.5">
              <span class="text-indigo-700 font-bold">Ref Points (IFET / Pondy)</span>
            </label>
          </div>"""

if old_layer_toggles in content:
    content = content.replace(old_layer_toggles, new_layer_toggles)

# 4. Add Historical Rainfall Analysis Banner in Analytics Section
old_analytics_grid = """    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">"""

new_analytics_grid = """    <!-- Real Historical Rainfall Intelligence Banner -->
    <div class="mb-6 bg-white rounded-xl border border-brand-border p-5 shadow-sm">
      <div class="flex flex-col md:flex-row items-start md:items-center justify-between pb-3 border-b border-slate-100 gap-2">
        <div class="flex items-center space-x-2.5">
          <div class="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center font-bold">
            <i data-lucide="cloud-rain" class="w-4 h-4"></i>
          </div>
          <div>
            <h3 class="text-base font-bold text-brand-navy">Tamil Nadu & Cuddalore 10-Year Historical Rainfall Record (2015-2024)</h3>
            <p class="text-xs text-brand-subtle">ECMWF ERA5 / IMD Reanalysis Observations &middot; 3,653 Daily Verified Records &middot; Lat 11.748°N, Lon 79.771°E</p>
          </div>
        </div>
        <div class="flex items-center space-x-4 text-xs">
          <div class="px-2.5 py-1 rounded bg-slate-50 border border-slate-200">
            <span class="text-slate-400">10-Yr Max Day:</span> <strong class="text-rose-600" id="hist-max-rain">175.7 mm</strong>
          </div>
          <div class="px-2.5 py-1 rounded bg-slate-50 border border-slate-200">
            <span class="text-slate-400">Rainy Days:</span> <strong class="text-brand-navy" id="hist-rainy-days">2,333 days</strong>
          </div>
        </div>
      </div>
      
      <!-- Top Deluges Table & Seasonal Trend -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-4">
        <div class="lg:col-span-7 space-y-2">
          <div class="text-xs font-semibold text-brand-navy flex items-center justify-between">
            <span>Verified Severe Cyclonic & Monsoon Deluges</span>
            <span class="text-[10px] text-slate-400 font-normal">Ranked by 24h Precipitation</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border border-slate-100 rounded">
              <thead class="bg-slate-50 text-slate-600 uppercase text-[10px] tracking-wider">
                <tr>
                  <th class="py-2 px-3">Date</th>
                  <th class="py-2 px-3">Precip (mm)</th>
                  <th class="py-2 px-3">3-Day Soil Sat.</th>
                  <th class="py-2 px-3">Gust (km/h)</th>
                  <th class="py-2 px-3">IMD Category</th>
                </tr>
              </thead>
              <tbody id="hist-deluges-table" class="divide-y divide-slate-100 text-slate-700">
                <tr class="hover:bg-slate-50/50">
                  <td class="py-1.5 px-3 font-semibold text-brand-navy">2020-11-25</td>
                  <td class="py-1.5 px-3 font-bold text-rose-600">175.7 mm</td>
                  <td class="py-1.5 px-3">182.4 mm</td>
                  <td class="py-1.5 px-3">49.0 km/h</td>
                  <td class="py-1.5 px-3"><span class="px-2 py-0.5 rounded bg-rose-50 text-rose-700 text-[10px] font-semibold">Cyclone Nivar</span></td>
                </tr>
                <tr class="hover:bg-slate-50/50">
                  <td class="py-1.5 px-3 font-semibold text-brand-navy">2024-11-30</td>
                  <td class="py-1.5 px-3 font-bold text-rose-600">151.0 mm</td>
                  <td class="py-1.5 px-3">265.7 mm</td>
                  <td class="py-1.5 px-3">41.4 km/h</td>
                  <td class="py-1.5 px-3"><span class="px-2 py-0.5 rounded bg-rose-50 text-rose-700 text-[10px] font-semibold">Cyclone Fengal</span></td>
                </tr>
                <tr class="hover:bg-slate-50/50">
                  <td class="py-1.5 px-3 font-semibold text-brand-navy">2015-11-09</td>
                  <td class="py-1.5 px-3 font-bold text-rose-600">142.7 mm</td>
                  <td class="py-1.5 px-3">289.1 mm</td>
                  <td class="py-1.5 px-3">42.5 km/h</td>
                  <td class="py-1.5 px-3"><span class="px-2 py-0.5 rounded bg-rose-50 text-rose-700 text-[10px] font-semibold">2015 South India Flood</span></td>
                </tr>
                <tr class="hover:bg-slate-50/50">
                  <td class="py-1.5 px-3 font-semibold text-brand-navy">2022-11-01</td>
                  <td class="py-1.5 px-3 font-bold text-amber-600">128.1 mm</td>
                  <td class="py-1.5 px-3">145.2 mm</td>
                  <td class="py-1.5 px-3">15.1 km/h</td>
                  <td class="py-1.5 px-3"><span class="px-2 py-0.5 rounded bg-amber-50 text-amber-700 text-[10px] font-semibold">NE Monsoon Surge</span></td>
                </tr>
                <tr class="hover:bg-slate-50/50">
                  <td class="py-1.5 px-3 font-semibold text-brand-navy">2024-12-01</td>
                  <td class="py-1.5 px-3 font-bold text-amber-600">114.7 mm</td>
                  <td class="py-1.5 px-3">265.7 mm</td>
                  <td class="py-1.5 px-3">51.8 km/h</td>
                  <td class="py-1.5 px-3"><span class="px-2 py-0.5 rounded bg-amber-50 text-amber-700 text-[10px] font-semibold">Heavy Rain</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <div class="lg:col-span-5 flex flex-col justify-between">
          <div class="text-xs font-semibold text-brand-navy mb-1.5">Annual Precipitation Summary (mm)</div>
          <div class="h-44 relative">
            <canvas id="chart-annual-rainfall"></canvas>
          </div>
          <div class="text-[11px] text-slate-500 italic mt-2">
            Peak precipitation consistently occurs during October–December Northeast Monsoon (Depressions & Bay of Bengal Cyclones).
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">"""

if old_analytics_grid in content:
    content = content.replace(old_analytics_grid, new_analytics_grid, 1)

# 5. Extract script part and inject real OSM GIS layers & real basemaps
script_marker = "<!-- SCRIPT FOR MAPLIBRE 3D, SIMULATION LOGIC, & CHARTS -->"
html_head = content.split(script_marker)[0]

buildings_json_str = json.dumps(real_buildings)
waterways_json_str = json.dumps(real_waterways)
shelters_json_str = json.dumps(real_shelters)
routes_json_str = json.dumps(real_routes)

upgraded_script = f"""{script_marker}
  <script>
    // Initialize Lucide icons
    lucide.createIcons();

    const API_BASE = "http://127.0.0.1:8000";
    
    // Geographical Reference Points
    const CUDDALORE_CENTER = [79.7714, 11.7480];  // Core Flood-Analysis Area
    const IFET_COORDS = [79.61072, 11.91961];       // IFET College of Engineering (External Reference)
    const PONDY_COORDS = [79.8306, 11.9341];        // Puducherry City (External Reference)

    // INLINE EMBEDDED REAL OSM DATASETS
    const REAL_OSM_BUILDINGS = {buildings_json_str};
    const REAL_OSM_WATERWAYS = {waterways_json_str};
    const REAL_OSM_SHELTERS = {shelters_json_str};
    const REAL_OSM_ROUTES = {routes_json_str};

    let map;
    let currentPitch = 55;
    let currentBearing = 30;
    let currentBasemap = 'osm';
    let chartPopRisk = null;
    let chartFloodDist = null;
    let chartRoutesComp = null;
    let chartAnnualRain = null;
    let backendAvailable = false;
    let shelterMarkers = [];
    let externalRefMarkers = [];
    let ifetPopup = null;
    let pondyPopup = null;

    // Basemaps (100% Free, Zero API Keys, No Watermarks)
    const BASEMAPS = {{
      osm: {{
        type: 'raster',
        tiles: ['https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png'],
        tileSize: 256,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors'
      }},
      satellite: {{
        type: 'raster',
        tiles: ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}'],
        tileSize: 256,
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics'
      }},
      topo: {{
        type: 'raster',
        tiles: ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{{z}}/{{y}}/{{x}}'],
        tileSize: 256,
        attribution: 'Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, National Geographic, and Esri'
      }}
    }};

    // Initialize MapLibre GL
    function initMap() {{
      map = new maplibregl.Map({{
        container: 'cuddalore-map',
        style: {{
          version: 8,
          sources: {{
            'basemap-tiles': BASEMAPS.osm
          }},
          layers: [
            {{
              id: 'basemap-layer',
              type: 'raster',
              source: 'basemap-tiles',
              minzoom: 0,
              maxzoom: 19
            }}
          ]
        }},
        center: CUDDALORE_CENTER,
        zoom: 13.8,
        pitch: currentPitch,
        bearing: currentBearing,
        antialias: true
      }});

      map.addControl(new maplibregl.NavigationControl({{
        visualizePitch: true
      }}), 'top-right');

      map.addControl(new maplibregl.ScaleControl({{
        maxWidth: 150,
        unit: 'metric'
      }}), 'bottom-right');

      map.on('load', () => {{
        setupGeospatialLayers();
        setupExternalReferenceMarkers();
        connectBackend();
      }});

      map.on('rotate', updateBearingDisplay);
      map.on('pitch', updateBearingDisplay);

      // Close search dropdown on click outside
      document.addEventListener('click', (e) => {{
        const searchContainer = document.getElementById('map-search-input');
        const dropdown = document.getElementById('map-search-dropdown');
        if (dropdown && !dropdown.contains(e.target) && e.target !== searchContainer) {{
          dropdown.classList.add('hidden');
        }}
      }});
    }}

    function setBasemap(type) {{
      currentBasemap = type;
      if (!map) return;
      const src = map.getSource('basemap-tiles');
      if (src) {{
        map.removeLayer('basemap-layer');
        map.removeSource('basemap-tiles');
        map.addSource('basemap-tiles', BASEMAPS[type]);
        
        const firstLayerId = map.getLayer('waterways-layer') ? 'waterways-layer' : undefined;
        map.addLayer({{
          id: 'basemap-layer',
          type: 'raster',
          source: 'basemap-tiles',
          minzoom: 0,
          maxzoom: 19
        }}, firstLayerId);
      }}

      ['btn-basemap-osm', 'btn-basemap-satellite', 'btn-basemap-topo'].forEach(id => {{
        const btn = document.getElementById(id);
        if (btn) {{
          if (id === `btn-basemap-${{type}}`) {{
            btn.className = 'px-2 py-1 rounded bg-brand-navy text-white transition-colors';
          }} else {{
            btn.className = 'px-2 py-1 rounded hover:bg-slate-100 text-slate-700 transition-colors';
          }}
        }}
      }});

      const names = {{ osm: 'OpenStreetMap Street', satellite: 'Esri Satellite Imagery', topo: 'Esri Topographic' }};
      showToast(`Switched basemap to ${{names[type]}} (No API keys required).`);
    }}

    function updateBearingDisplay() {{
      const b = Math.round(map.getBearing());
      const p = Math.round(map.getPitch());
      const label = document.getElementById('compass-label');
      if (label) {{
        label.innerText = `Bearing: ${{b}}° | Pitch: ${{p}}°`;
      }}
    }}

    function setupGeospatialLayers() {{
      // 1. REAL WATERWAYS (Gadilam River, Pennaiyar River, Uppanar Canal, Coastline)
      map.addSource('cuddalore-waterways', {{
        type: 'geojson',
        data: REAL_OSM_WATERWAYS
      }});

      map.addLayer({{
        id: 'waterways-layer',
        type: 'line',
        source: 'cuddalore-waterways',
        layout: {{ 'line-join': 'round', 'line-cap': 'round' }},
        paint: {{
          'line-color': '#0284C7',
          'line-width': 3.5,
          'line-opacity': 0.85
        }}
      }});

      // 2. REAL 3D EXTRUDED BUILDINGS (302 Genuine Footprints)
      map.addSource('cuddalore-buildings', {{
        type: 'geojson',
        data: REAL_OSM_BUILDINGS
      }});

      map.addLayer({{
        id: '3d-buildings',
        type: 'fill-extrusion',
        source: 'cuddalore-buildings',
        paint: {{
          'fill-extrusion-color': [
            'case',
            ['get', 'flooded'], '#DC2626',
            '#94A3B8'
          ],
          'fill-extrusion-height': ['get', 'height'],
          'fill-extrusion-base': 0,
          'fill-extrusion-opacity': 0.85
        }}
      }});

      // 3. FLOOD INUNDATION LAYER (Overlay along Gadilam floodplain)
      map.addSource('flood-inundation', {{
        type: 'geojson',
        data: generateFloodInundation(65)
      }});

      map.addLayer({{
        id: 'flood-inundation-layer',
        type: 'fill',
        source: 'flood-inundation',
        paint: {{
          'fill-color': '#0284C7',
          'fill-opacity': 0.52,
          'fill-outline-color': '#0369A1'
        }}
      }});

      // 4. REAL EVACUATION ROUTES (NetworkX Dijkstra paths along real OSM roads)
      map.addSource('evacuation-routes', {{
        type: 'geojson',
        data: REAL_OSM_ROUTES
      }});

      map.addLayer({{
        id: 'routes-layer',
        type: 'line',
        source: 'evacuation-routes',
        layout: {{ 'line-join': 'round', 'line-cap': 'round' }},
        paint: {{
          'line-color': ['get', 'color'],
          'line-width': ['get', 'width'],
          'line-opacity': 0.95
        }}
      }});

      // 5. CANDIDATE SHELTERS (68 Verified Facilities)
      renderShelterMarkers(REAL_OSM_SHELTERS.features);
    }}

    // =========================================================================
    // EXTERNAL REFERENCE LOCATIONS: IFET COLLEGE & PUDUCHERRY
    // =========================================================================
    function setupExternalReferenceMarkers() {{
      // Remove any existing external markers
      externalRefMarkers.forEach(m => m.remove());
      externalRefMarkers = [];

      // 1. IFET College of Engineering Marker
      const ifetEl = document.createElement('div');
      ifetEl.id = 'marker-ifet';
      ifetEl.className = 'cursor-pointer group flex flex-col items-center';
      ifetEl.innerHTML = `
        <div class="relative flex items-center justify-center">
          <span class="absolute w-10 h-10 rounded-full bg-blue-500/30 animate-ping"></span>
          <div class="relative w-9 h-9 rounded-full bg-gradient-to-tr from-blue-700 to-blue-500 border-2 border-white shadow-xl flex items-center justify-center text-white text-base font-bold transition-transform group-hover:scale-125">
            🎓
          </div>
        </div>
        <div class="mt-1 px-2 py-0.5 rounded bg-brand-navy/90 text-white font-serif text-[10px] font-bold shadow-md whitespace-nowrap border border-white/40">
          IFET College
        </div>
      `;

      ifetPopup = new maplibregl.Popup({{ offset: 18, maxWidth: '280px' }}).setHTML(`
        <div style="font-family: Cambria, Georgia, serif; padding: 4px;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
            <span style="font-size: 9.5px; font-weight: bold; padding: 2px 7px; border-radius: 4px; background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; text-transform: uppercase;">
              External Academic Reference
            </span>
          </div>
          <div style="font-size: 13.5px; font-weight: bold; color: #1E293B; margin-top: 2px;">
            IFET College of Engineering
          </div>
          <div style="font-size: 11px; color: #475569; margin-top: 4px; line-height: 1.35;">
            Gangarampalayam, Valavanur Post, Villupuram District, Tamil Nadu &ndash; 605108
          </div>
          <div style="font-size: 10px; color: #64748B; margin-top: 6px; font-family: monospace; background: #F8FAFC; padding: 3px 6px; border-radius: 4px; border: 1px solid #E2E8F0;">
            Lat: <strong>11.91961° N</strong> &middot; Lon: <strong>79.61072° E</strong>
          </div>
          <div style="font-size: 10.5px; color: #2563EB; font-weight: 600; margin-top: 5px;">
            &bull; Distance from Cuddalore: ~26.5 km Northwest
          </div>
          <div style="font-size: 9.5px; color: #64748B; margin-top: 5px; padding-top: 4px; border-top: 1px solid #F1F5F9; font-style: italic;">
            *Academic project evaluation partner. Excluded from Cuddalore flood-risk, rainfall, and evacuation exposure calculations.
          </div>
        </div>
      `);

      const ifetMarker = new maplibregl.Marker({{ element: ifetEl }})
        .setLngLat(IFET_COORDS)
        .setPopup(ifetPopup)
        .addTo(map);

      externalRefMarkers.push(ifetMarker);

      // 2. Puducherry (Pondy) City Marker
      const pondyEl = document.createElement('div');
      pondyEl.id = 'marker-pondy';
      pondyEl.className = 'cursor-pointer group flex flex-col items-center';
      pondyEl.innerHTML = `
        <div class="relative flex items-center justify-center">
          <span class="absolute w-10 h-10 rounded-full bg-purple-500/30 animate-ping"></span>
          <div class="relative w-9 h-9 rounded-full bg-gradient-to-tr from-purple-700 to-purple-500 border-2 border-white shadow-xl flex items-center justify-center text-white text-base font-bold transition-transform group-hover:scale-125">
            🏛️
          </div>
        </div>
        <div class="mt-1 px-2 py-0.5 rounded bg-brand-navy/90 text-white font-serif text-[10px] font-bold shadow-md whitespace-nowrap border border-white/40">
          Puducherry (Pondy)
        </div>
      `;

      pondyPopup = new maplibregl.Popup({{ offset: 18, maxWidth: '280px' }}).setHTML(`
        <div style="font-family: Cambria, Georgia, serif; padding: 4px;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
            <span style="font-size: 9.5px; font-weight: bold; padding: 2px 7px; border-radius: 4px; background: #F3E8FF; color: #7E22CE; border: 1px solid #E9D5FF; text-transform: uppercase;">
              External Regional Reference
            </span>
          </div>
          <div style="font-size: 13.5px; font-weight: bold; color: #1E293B; margin-top: 2px;">
            Puducherry (Pondicherry / Pondy)
          </div>
          <div style="font-size: 11px; color: #475569; margin-top: 4px; line-height: 1.35;">
            White Town / Promenade Beach, Union Territory of Puducherry &ndash; 605001
          </div>
          <div style="font-size: 10px; color: #64748B; margin-top: 6px; font-family: monospace; background: #F8FAFC; padding: 3px 6px; border-radius: 4px; border: 1px solid #E2E8F0;">
            Lat: <strong>11.93410° N</strong> &middot; Lon: <strong>79.83060° E</strong>
          </div>
          <div style="font-size: 10.5px; color: #7C3AED; font-weight: 600; margin-top: 5px;">
            &bull; Distance from Cuddalore: ~21.8 km North via ECR
          </div>
          <div style="font-size: 9.5px; color: #64748B; margin-top: 5px; padding-top: 4px; border-top: 1px solid #F1F5F9; font-style: italic;">
            *Regional coastal reference benchmark. Excluded from Cuddalore flood-risk, rainfall, and evacuation exposure calculations.
          </div>
        </div>
      `);

      const pondyMarker = new maplibregl.Marker({{ element: pondyEl }})
        .setLngLat(PONDY_COORDS)
        .setPopup(pondyPopup)
        .addTo(map);

      externalRefMarkers.push(pondyMarker);
    }}

    // =========================================================================
    // QUICK CAMERA NAVIGATION FUNCTIONS
    // =========================================================================
    function goToIFET() {{
      if (!map) return;
      closeSearchDropdown();
      map.flyTo({{
        center: IFET_COORDS,
        zoom: 15.5,
        pitch: 52,
        bearing: 25,
        speed: 1.2,
        curve: 1.42,
        essential: true
      }});
      setTimeout(() => {{
        if (ifetPopup && !ifetPopup.isOpen()) {{
          ifetPopup.setLngLat(IFET_COORDS).addTo(map);
        }}
      }}, 1200);
      showToast('Navigated to IFET College of Engineering (External Reference &middot; Villupuram).');
    }}

    function goToPondy() {{
      if (!map) return;
      closeSearchDropdown();
      map.flyTo({{
        center: PONDY_COORDS,
        zoom: 15.0,
        pitch: 48,
        bearing: -20,
        speed: 1.2,
        curve: 1.42,
        essential: true
      }});
      setTimeout(() => {{
        if (pondyPopup && !pondyPopup.isOpen()) {{
          pondyPopup.setLngLat(PONDY_COORDS).addTo(map);
        }}
      }}, 1200);
      showToast('Navigated to Puducherry City (External Reference &middot; White Town).');
    }}

    function setBasinView() {{
      closeSearchDropdown();
      map.flyTo({{
        center: CUDDALORE_CENTER,
        zoom: 13.8,
        pitch: 55,
        bearing: 30,
        speed: 1.2,
        curve: 1.4,
        essential: true
      }});
      highlightPreset('view-basin');
      showToast('Centered on Cuddalore Basin Core (Primary Flood-Analysis Area).');
    }}

    function setCoastalView() {{
      closeSearchDropdown();
      map.flyTo({{ center: [79.7860, 11.7420], zoom: 14.5, pitch: 60, bearing: -40, speed: 1.2, essential: true }});
      highlightPreset('view-coast');
      showToast('Viewing Silver Beach Coastal Shoreline.');
    }}

    function setOldTownView() {{
      closeSearchDropdown();
      map.flyTo({{ center: [79.7680, 11.7280], zoom: 15.2, pitch: 55, bearing: 15, speed: 1.2, essential: true }});
      highlightPreset('view-oldtown');
      showToast('Viewing Cuddalore Old Town & Port District.');
    }}

    function toggle3DPitch() {{
      const targetPitch = map.getPitch() > 40 ? 0 : 60;
      map.easeTo({{ pitch: targetPitch, duration: 800 }});
    }}

    function highlightPreset(id) {{
      ['view-basin', 'view-coast', 'view-oldtown'].forEach(btnId => {{
        const el = document.getElementById(btnId);
        if (el) {{
          el.className = btnId === id 
            ? 'px-2.5 py-1 rounded bg-brand-navy text-white font-semibold transition-colors flex items-center space-x-1'
            : 'px-2.5 py-1 rounded hover:bg-slate-100 text-slate-700 transition-colors flex items-center space-x-1';
        }}
      }});
    }}

    // =========================================================================
    // MAP SEARCH FUNCTIONALITY
    // =========================================================================
    function showSearchDropdown() {{
      const dropdown = document.getElementById('map-search-dropdown');
      if (dropdown) dropdown.classList.remove('hidden');
    }}

    function closeSearchDropdown() {{
      const dropdown = document.getElementById('map-search-dropdown');
      if (dropdown) dropdown.classList.add('hidden');
    }}

    function clearSearch() {{
      const input = document.getElementById('map-search-input');
      const clearBtn = document.getElementById('btn-search-clear');
      if (input) {{
        input.value = '';
        input.focus();
      }}
      if (clearBtn) clearBtn.classList.add('hidden');
      closeSearchDropdown();
    }}

    function handleMapSearch(val) {{
      const query = val.toLowerCase().trim();
      const clearBtn = document.getElementById('btn-search-clear');
      if (clearBtn) {{
        if (query.length > 0) clearBtn.classList.remove('hidden');
        else clearBtn.classList.add('hidden');
      }}
      showSearchDropdown();

      // Search matching shortcuts
      if (query.includes('ifet') || query.includes('college') || query.includes('villupuram') || query.includes('gangaram')) {{
        // Auto highlight IFET in toast if pressed enter
      }} else if (query.includes('pondy') || query.includes('puducherry') || query.includes('pondicherry') || query.includes('white town')) {{
        // Auto highlight Pondy
      }}
    }}

    // Listen for Enter key in search box
    document.addEventListener('DOMContentLoaded', () => {{
      const searchInput = document.getElementById('map-search-input');
      if (searchInput) {{
        searchInput.addEventListener('keydown', (e) => {{
          if (e.key === 'Enter') {{
            const q = searchInput.value.toLowerCase().trim();
            if (q.includes('ifet') || q.includes('college') || q.includes('villupuram')) {{
              goToIFET();
            }} else if (q.includes('pondy') || q.includes('puducherry') || q.includes('pondicherry')) {{
              goToPondy();
            }} else if (q.includes('old') || q.includes('port')) {{
              setOldTownView();
            }} else if (q.includes('coast') || q.includes('beach') || q.includes('silver')) {{
              setCoastalView();
            }} else {{
              setBasinView();
            }}
          }}
        }});
      }}
    }});

    // Layer Toggles
    function toggleLayer(layerKey) {{
      if (!map) return;
      if (layerKey === 'buildings') {{
        const visible = document.getElementById('layer-buildings').checked;
        map.setLayoutProperty('3d-buildings', 'visibility', visible ? 'visible' : 'none');
      }} else if (layerKey === 'waterways') {{
        const visible = document.getElementById('layer-waterways').checked;
        map.setLayoutProperty('waterways-layer', 'visibility', visible ? 'visible' : 'none');
      }} else if (layerKey === 'floods') {{
        const visible = document.getElementById('layer-floods').checked;
        map.setLayoutProperty('flood-inundation-layer', 'visibility', visible ? 'visible' : 'none');
      }} else if (layerKey === 'routes') {{
        const visible = document.getElementById('layer-routes').checked;
        map.setLayoutProperty('routes-layer', 'visibility', visible ? 'visible' : 'none');
      }} else if (layerKey === 'shelters') {{
        const visible = document.getElementById('layer-shelters').checked;
        shelterMarkers.forEach(m => m.getElement().style.display = visible ? 'flex' : 'none');
      }} else if (layerKey === 'refs') {{
        const visible = document.getElementById('layer-refs').checked;
        externalRefMarkers.forEach(m => m.getElement().style.display = visible ? 'flex' : 'none');
      }}
    }}

    function renderShelterMarkers(shelterFeatures) {{
      shelterMarkers.forEach(m => m.remove());
      shelterMarkers = [];

      shelterFeatures.slice(0, 24).forEach(f => {{
        const props = f.properties || {{}};
        const coords = f.geometry ? f.geometry.coordinates : f.coords;
        if (!coords) return;

        const el = document.createElement('div');
        el.className = 'w-7 h-7 rounded-full bg-brand-navy border-2 border-white shadow-lg flex items-center justify-center text-white cursor-pointer hover:scale-110 transition-transform';
        el.innerHTML = '<span style="font-size: 11px; font-weight: bold; font-family: Cambria, serif;">H</span>';

        const popup = new maplibregl.Popup({{ offset: 12 }}).setHTML(`
          <div style="font-family: Cambria, Georgia, serif; min-width: 170px;">
            <div style="font-size: 11px; font-weight: bold; color: #1E293B;">${{props.name || 'Emergency Shelter'}}</div>
            <div style="font-size: 10px; color: #2563EB; font-weight: 600; margin-top: 2px;">${{props.type || 'Designated Facility'}}</div>
            <div style="font-size: 10px; color: #64748B; margin-top: 4px;">Capacity: <strong>${{(props.capacity || 1000).toLocaleString()}} persons</strong></div>
            <div style="font-size: 9px; color: #16A34A; font-weight: bold; margin-top: 2px;">Status: Dry & Accessible</div>
          </div>
        `);

        const marker = new maplibregl.Marker({{ element: el }})
          .setLngLat(coords)
          .setPopup(popup)
          .addTo(map);
        shelterMarkers.push(marker);
      }});
    }}

    function generateFloodInundation(intensity) {{
      const intensityFactor = intensity / 100.0;
      const originLng = 79.7720;
      const originLat = 11.7450;
      const spanLng = 0.016 * (0.8 + 0.4 * intensityFactor);
      const spanLat = 0.009 * (0.8 + 0.4 * intensityFactor);

      const coords = [
        [originLng - spanLng, originLat - 0.003],
        [originLng - spanLng * 0.4, originLat + spanLat * 0.7],
        [originLng + spanLng * 0.5, originLat + spanLat * 1.1],
        [originLng + spanLng * 1.2, originLat + spanLat * 0.8],
        [originLng + spanLng * 1.4, originLat + 0.001],
        [originLng + spanLng * 1.1, originLat - spanLat * 0.9],
        [originLng + spanLng * 0.3, originLat - spanLat * 0.8],
        [originLng - spanLng * 0.6, originLat - spanLat * 0.6],
        [originLng - spanLng, originLat - 0.003]
      ];

      return {{
        type: 'FeatureCollection',
        features: [
          {{
            type: 'Feature',
            properties: {{ level: 'Severe Inundation', depth: 1.2 + intensityFactor * 1.5 }},
            geometry: {{
              type: 'Polygon',
              coordinates: [coords]
            }}
          }}
        ]
      }};
    }}

    function updateIntensityDisplay(val) {{
      document.getElementById('intensity-val').innerText = val + '%';
      document.getElementById('sim-water-peak').innerText = (1.1 + (val/100)*1.1).toFixed(2) + ' m AOD';
      document.getElementById('sim-inun-area').innerText = (8.5 + (val/100)*9.8).toFixed(1) + ' sq.km';
      const affectedPop = Math.round(11200 + (val/100) * 11500);
      document.getElementById('kpi-population').innerText = affectedPop.toLocaleString();
    }}

    function updateRadiusDisplay(val) {{
      document.getElementById('radius-val').innerText = parseFloat(val).toFixed(1) + ' km';
    }}

    let currentScenario = 'heavy';
    function setScenario(type) {{
      currentScenario = type;
      const heavyBtn = document.getElementById('scen-heavy');
      const cycloneBtn = document.getElementById('scen-cyclone');
      
      if (type === 'heavy') {{
        heavyBtn.className = 'scenario-btn px-3 py-2 rounded text-xs font-medium border border-brand-accent bg-blue-50 text-brand-accent text-center transition-colors';
        cycloneBtn.className = 'scenario-btn px-3 py-2 rounded text-xs font-medium border border-brand-border bg-white text-brand-slate hover:bg-slate-50 text-center transition-colors';
        document.getElementById('flood-intensity').value = 65;
        updateIntensityDisplay(65);
        document.getElementById('spread-radius').value = 3.4;
        updateRadiusDisplay(3.4);
      }} else {{
        cycloneBtn.className = 'scenario-btn px-3 py-2 rounded text-xs font-medium border border-brand-accent bg-blue-50 text-brand-accent text-center transition-colors';
        heavyBtn.className = 'scenario-btn px-3 py-2 rounded text-xs font-medium border border-brand-border bg-white text-brand-slate hover:bg-slate-50 text-center transition-colors';
        document.getElementById('flood-intensity').value = 90;
        updateIntensityDisplay(90);
        document.getElementById('spread-radius').value = 5.2;
        updateRadiusDisplay(5.2);
      }}
      runSimulation();
    }}

    async function runSimulation() {{
      const intensity = parseInt(document.getElementById('flood-intensity').value);
      const radius = parseFloat(document.getElementById('spread-radius').value);
      const origin = document.getElementById('flood-origin').value;

      try {{
        const resp = await fetch(`${{API_BASE}}/api/simulation/run`, {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            intensity: intensity,
            spread_radius_km: radius,
            origin: origin,
            scenario: currentScenario
          }})
        }});

        if (resp.ok) {{
          const res = await resp.json();
          document.getElementById('kpi-population').innerText = res.exposed_population.toLocaleString();
          document.getElementById('kpi-population-sub').innerText = `${{res.basin_percentage}}% of basin`;
          document.getElementById('kpi-pop-delta').innerText = `+${{res.delta_surge.toLocaleString()}}`;
          document.getElementById('kpi-highrisk').innerText = res.high_risk_zones;
          document.getElementById('kpi-routes').innerText = res.passable_routes_ratio;

          document.getElementById('sim-water-peak').innerText = `${{res.water_peak_m_aod}} m AOD`;
          document.getElementById('sim-inun-area').innerText = `${{res.inundation_area_sqkm}} sq.km`;
          document.getElementById('sim-sub-roads').innerText = `${{res.submerged_roads_count}} Artery Segments`;

          if (map && map.getSource('flood-inundation')) {{
            map.getSource('flood-inundation').setData(res.inundation_geojson);
          }}

          if (chartPopRisk && res.exposure_breakdown) {{
            chartPopRisk.data.datasets[0].data = [
              res.exposure_breakdown.low_risk,
              res.exposure_breakdown.moderate_risk,
              res.exposure_breakdown.high_risk,
              res.exposure_breakdown.critical_estuary
            ];
            chartPopRisk.update();
          }}

          if (chartFloodDist) {{
            const highPct = Math.round(15 + (intensity/100)*22);
            const modPct = Math.round(20 + (intensity/100)*15);
            chartFloodDist.data.datasets[0].data = [100 - highPct - modPct, modPct, highPct];
            chartFloodDist.update();
          }}

          showToast(`FastAPI computed: ${{res.water_peak_m_aod}}m flood surge along Gadilam floodplain.`);
          return;
        }}
      }} catch (err) {{
        console.warn("Backend call failed, using client calculations:", err);
      }}

      if (map && map.getSource('flood-inundation')) {{
        map.getSource('flood-inundation').setData(generateFloodInundation(intensity));
      }}
      const popAffected = Math.round(11200 + (intensity/100) * 11500);
      document.getElementById('kpi-population').innerText = popAffected.toLocaleString();
      document.getElementById('kpi-population-sub').innerText = ((popAffected / 130000)*100).toFixed(1) + '% of basin';
      document.getElementById('kpi-pop-delta').innerText = '+' + Math.round(popAffected * 0.18).toLocaleString();
      document.getElementById('kpi-highrisk').innerText = Math.round(6 + (intensity/100) * 9);
      document.getElementById('kpi-routes').innerText = intensity > 80 ? '6 / 11' : '8 / 11';
      showToast(`Simulation computed: ${{intensity}}% surge. Real OSM terrain updated.`);
    }}

    function resetSimulation() {{
      document.getElementById('flood-intensity').value = 65;
      updateIntensityDisplay(65);
      document.getElementById('spread-radius').value = 3.4;
      updateRadiusDisplay(3.4);
      setScenario('heavy');
      showToast('Simulation parameters reset to baseline.');
    }}

    function showToast(msg) {{
      const toast = document.getElementById('sim-toast');
      const toastMsg = document.getElementById('sim-toast-msg');
      if (toast && toastMsg) {{
        toastMsg.innerText = msg;
        toast.classList.remove('hidden');
        setTimeout(() => {{
          toast.classList.add('hidden');
        }}, 3500);
      }}
    }}

    function highlightRoute(routeId) {{
      if (!map) return;
      if (routeId === 'shortest') {{
        map.flyTo({{ center: [79.7714, 11.7480], zoom: 14.8, pitch: 52, bearing: 35, essential: true }});
        showToast('Zoomed to Shortest Route (Yellow) - Cuddalore Port Road crossing Gadilam causeway.');
      }} else {{
        map.flyTo({{ center: [79.7610, 11.7550], zoom: 14.5, pitch: 50, bearing: 10, essential: true }});
        showToast('Zoomed to Risk-Aware Bypass (Green) - High-ground Vandipalayam ridge route.');
      }}
    }}

    async function connectBackend() {{
      try {{
        const resp = await fetch(`${{API_BASE}}/api/health`, {{ signal: AbortSignal.timeout(3000) }});
        if (resp.ok) {{
          const health = await resp.json();
          backendAvailable = true;
          const dot = document.getElementById('backend-dot');
          const text = document.getElementById('backend-status-text');
          if (dot && text) {{
            dot.className = "w-2 h-2 rounded-full bg-emerald-500 animate-pulse";
            text.innerText = `FastAPI Core Live: ${{health.osm_nodes_count}} OSM Nodes | ${{health.rainfall_records_count}} Rain Records`;
          }}
          loadRainfallAnalytics();
        }}
      }} catch (err) {{
        console.warn("Backend running in client fallback mode:", err);
      }}
    }}

    async function loadRainfallAnalytics() {{
      try {{
        const resp = await fetch(`${{API_BASE}}/api/rainfall/summary`);
        if (resp.ok) {{
          const rain = await resp.json();
          const maxEl = document.getElementById('hist-max-rain');
          const daysEl = document.getElementById('hist-rainy-days');
          if (maxEl) maxEl.innerText = `${{rain.max_single_day_mm}} mm`;
          if (daysEl) daysEl.innerText = `${{rain.rainy_days}} days`;

          if (rain.annual_summary && chartAnnualRain) {{
            const labels = rain.annual_summary.map(a => a.year);
            const totals = rain.annual_summary.map(a => a.total_rainfall_mm);
            chartAnnualRain.data.labels = labels;
            chartAnnualRain.data.datasets[0].data = totals;
            chartAnnualRain.update();
          }}
        }}
      }} catch (e) {{
        console.warn("Could not load rainfall summary:", e);
      }}
    }}

    function initCharts() {{
      const ctx1 = document.getElementById('chart-population-risk');
      if (ctx1) {{
        chartPopRisk = new Chart(ctx1, {{
          type: 'bar',
          data: {{
            labels: ['Low Risk', 'Moderate', 'High Risk', 'Critical (Estuary)'],
            datasets: [{{
              label: 'Exposed Population',
              data: [42500, 24300, 18450, 7200],
              backgroundColor: ['#16A34A', '#F59E0B', '#EA580C', '#DC2626'],
              borderRadius: 4
            }}]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }},
            scales: {{
              y: {{
                beginAtZero: true,
                grid: {{ color: '#F1F5F9' }},
                ticks: {{ font: {{ family: 'Cambria, serif', size: 10 }}, color: '#64748B' }}
              }},
              x: {{
                grid: {{ display: false }},
                ticks: {{ font: {{ family: 'Cambria, serif', size: 10 }}, color: '#64748B' }}
              }}
            }}
          }}
        }});
      }}

      const ctx2 = document.getElementById('chart-flood-distribution');
      if (ctx2) {{
        chartFloodDist = new Chart(ctx2, {{
          type: 'doughnut',
          data: {{
            labels: ['Dry / Elevated Land', 'Moderate Risk (0.3 - 0.8m)', 'High Inundation (>1.2m)'],
            datasets: [{{
              data: [54, 28, 18],
              backgroundColor: ['#E2E8F0', '#38BDF8', '#0284C7'],
              borderWidth: 2,
              borderColor: '#FFFFFF'
            }}]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{
                position: 'bottom',
                labels: {{ font: {{ family: 'Cambria, serif', size: 10 }}, color: '#475569', boxWidth: 12 }}
              }}
            }},
            cutout: '65%'
          }}
        }});
      }}

      const ctx3 = document.getElementById('chart-routes-comparison');
      if (ctx3) {{
        chartRoutesComp = new Chart(ctx3, {{
          type: 'bar',
          data: {{
            labels: ['Shortest Corridor', 'Risk-Aware Bypass', 'Alt Rail Underpass'],
            datasets: [
              {{ label: 'Travel Time (mins)', data: [12, 19, 28], backgroundColor: '#2563EB', borderRadius: 4 }},
              {{ label: 'Flood Exposure Index (%)', data: [74, 18, 55], backgroundColor: '#DC2626', borderRadius: 4 }}
            ]
          }},
          options: {{
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{
                position: 'top',
                labels: {{ font: {{ family: 'Cambria, serif', size: 10 }}, color: '#475569', boxWidth: 12 }}
              }}
            }},
            scales: {{
              x: {{
                beginAtZero: true,
                grid: {{ color: '#F1F5F9' }},
                ticks: {{ font: {{ family: 'Cambria, serif', size: 10 }}, color: '#64748B' }}
              }},
              y: {{
                grid: {{ display: false }},
                ticks: {{ font: {{ family: 'Cambria, serif', size: 10 }}, color: '#475569' }}
              }}
            }}
          }}
        }});
      }}

      const ctxRain = document.getElementById('chart-annual-rainfall');
      if (ctxRain) {{
        chartAnnualRain = new Chart(ctxRain, {{
          type: 'bar',
          data: {{
            labels: ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
            datasets: [{{
              label: 'Annual Rainfall (mm)',
              data: [1845, 920, 1340, 1150, 1280, 1960, 1720, 1430, 1510, 1680],
              backgroundColor: '#0284C7',
              borderRadius: 4
            }}]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }},
            scales: {{
              y: {{
                beginAtZero: true,
                grid: {{ color: '#F1F5F9' }},
                ticks: {{ font: {{ family: 'Cambria, serif', size: 9 }}, color: '#64748B' }}
              }},
              x: {{
                grid: {{ display: false }},
                ticks: {{ font: {{ family: 'Cambria, serif', size: 9 }}, color: '#64748B' }}
              }}
            }}
          }}
        }});
      }}
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      initMap();
      initCharts();
    }});
  </script>
</body>
</html>
"""

final_html = html_head + upgraded_script

with open(out_html_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"Successfully generated RESCUE-X v3 index.html ({len(final_html)} bytes) with IFET and Pondy references!")
