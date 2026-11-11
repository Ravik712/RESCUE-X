import json
import os

NOTEBOOK_PATH = r"C:\Users\Lenovo\OneDrive\Documents\rk\RESCUE_X_V2\notebooks\data_science_analysis.ipynb"

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# RESCUE-X: Data Science with Python - Geospatial Flood Intelligence & Evacuation Analysis\n",
            "**Author:** Data Science with Python Value Added Course Student  \n",
            "**Region of Study:** Cuddalore City & Old Town, Tamil Nadu, India  \n",
            "**Core Modules Demonstrated:** Pandas, NumPy, Matplotlib, Plotly, NetworkX, GeoPandas  \n",
            "\n",
            "---"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Environment Setup & Library Imports"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": [],
        "source": [
            "import os\n",
            "import pandas as pd\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "import plotly.express as px\n",
            "import plotly.graph_objects as go\n",
            "import networkx as nx\n",
            "import json\n",
            "\n",
            "print('All essential Data Science libraries successfully imported.')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Dataset Loading & Data Cleaning (Pandas)\n",
            "- Inspecting 10-year daily meteorological records (2015-2024) for Cuddalore Station (11.748°N, 79.771°E).\n",
            "- Handling missing values, duplicate checks, date-time indexing, and IMD rainfall classification."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 2,
        "metadata": {},
        "outputs": [],
        "source": [
            "DATA_PATH = os.path.join('..', 'datasets', 'processed', 'cuddalore_rainfall_cleaned.csv')\n",
            "df = pd.read_csv(DATA_PATH)\n",
            "df['date'] = pd.to_datetime(df['date'])\n",
            "df['year'] = df['date'].dt.year\n",
            "df['month'] = df['date'].dt.month\n",
            "\n",
            "print(f'Total Daily Observations: {len(df)}')\n",
            "print('Null values per column:\\n', df.isnull().sum())\n",
            "print('Unique date records check:', df['date'].is_unique)\n",
            "df.head()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Statistical Analysis & Outlier Detection (NumPy & Pandas)\n",
            "- Descriptive statistics (mean, variance, max, 90th & 99th percentiles).\n",
            "- Interquartile Range (IQR) outlier detection for extreme cyclonic events."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 3,
        "metadata": {},
        "outputs": [],
        "source": [
            "precip = df['precipitation_mm'].to_numpy()\n",
            "non_zero = precip[precip > 0]\n",
            "\n",
            "print('--- Statistical Summary of Precipitation ---')\n",
            "print(f'Mean Daily Rainfall: {np.mean(precip):.2f} mm')\n",
            "print(f'Standard Deviation: {np.std(precip):.2f} mm')\n",
            "print(f'Max Single-Day Record: {np.max(precip):.2f} mm')\n",
            "print(f'90th Percentile (Rainy Days): {np.percentile(non_zero, 90):.2f} mm')\n",
            "print(f'99th Percentile (Rainy Days): {np.percentile(non_zero, 99):.2f} mm')\n",
            "\n",
            "# Top 5 Highest Cyclonic Deluge Days\n",
            "top_5 = df.sort_values(by='precipitation_mm', ascending=False).head(5)\n",
            "top_5[['date', 'precipitation_mm', 'rolling_3d_rain_mm', 'wind_speed_max_kmh', 'imd_category']]"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Data Visualization (Matplotlib & Plotly)\n",
            "- Annual rainfall trend analysis.\n",
            "- Seasonality profile demonstrating the Northeast Monsoon concentration (Oct - Dec)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 4,
        "metadata": {},
        "outputs": [],
        "source": [
            "fig, ax = plt.subplots(figsize=(10, 5), dpi=150)\n",
            "annual = df.groupby('year')['precipitation_mm'].sum()\n",
            "bars = ax.bar(annual.index, annual.values, color='#0284C7', edgecolor='#0369A1', alpha=0.85)\n",
            "ax.set_title('Cuddalore Annual Precipitation Totals (2015-2024)', fontsize=12, fontweight='bold')\n",
            "ax.set_xlabel('Year')\n",
            "ax.set_ylabel('Precipitation (mm)')\n",
            "ax.set_xticks(annual.index)\n",
            "for bar in bars:\n",
            "    yval = bar.get_height()\n",
            "    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 15, f'{int(yval)}', ha='center', va='bottom', fontsize=8)\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. NetworkX Graph Construction & Evacuation Routing\n",
            "- Constructing graph topology from OpenStreetMap arterial road network.\n",
            "- Shortest route ($W_{dist} = length$) vs Risk-Aware Safest route ($W_{risk} = length \\times (1 + 15 \\cdot r^2)$)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 5,
        "metadata": {},
        "outputs": [],
        "source": [
            "ROADS_GEOJSON = os.path.join('..', 'datasets', 'geographical', 'cuddalore_roads.geojson')\n",
            "with open(ROADS_GEOJSON, 'r', encoding='utf-8') as f:\n",
            "    roads_data = json.load(f)\n",
            "\n",
            "G = nx.Graph()\n",
            "for feat in roads_data['features']:\n",
            "    coords = feat['geometry']['coordinates']\n",
            "    props = feat['properties']\n",
            "    for i in range(len(coords) - 1):\n",
            "        u = (round(coords[i][0], 5), round(coords[i][1], 5))\n",
            "        v = (round(coords[i+1][0], 5), round(coords[i+1][1], 5))\n",
            "        dx = (v[0] - u[0]) * 111320 * np.cos(np.radians(11.75))\n",
            "        dy = (v[1] - u[1]) * 110574\n",
            "        dist = np.sqrt(dx**2 + dy**2)\n",
            "        if dist > 0:\n",
            "            G.add_edge(u, v, length=dist, name=props.get('name'))\n",
            "\n",
            "print(f'Graph constructed: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges')\n",
            "largest_cc = max(nx.connected_components(G), key=len)\n",
            "subG = G.subgraph(largest_cc).copy()\n",
            "nodes = list(subG.nodes())\n",
            "path = nx.dijkstra_path(subG, nodes[0], nodes[-1], weight='length')\n",
            "dist = nx.dijkstra_path_length(subG, nodes[0], nodes[-1], weight='length')\n",
            "print(f'Computed Route: {len(path)} waypoints, {dist/1000.0:.2f} km physical length.')"
        ]
    }
]

notebook_json = {
    "cells": cells,
    "metadata": {
        "language_info": {
            "name": "python",
            "version": "3.12.10"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
    json.dump(notebook_json, f, indent=2)

print(f"Jupyter Notebook successfully written to {NOTEBOOK_PATH}")

