import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
DATA_PATH = os.path.join(PROJECT_DIR, "datasets", "processed", "cuddalore_rainfall_cleaned.csv")
FIG_DIR = os.path.join(PROJECT_DIR, "documentation", "figures")
NOTEBOOK_DIR = os.path.join(PROJECT_DIR, "notebooks")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(NOTEBOOK_DIR, exist_ok=True)

print("Loading cleaned dataset with Pandas...")
df = pd.read_csv(DATA_PATH)
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

print(f"Dataset shape: {df.shape}")
print(f"Summary statistics of precipitation (mm):\n{df['precipitation_mm'].describe()}")

# -------------------------------------------------------------
# 1. MATPLOTLIB: 10-Year Rainfall Trends & Seasonality
# -------------------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), dpi=200)

# 1a. Annual Rainfall Totals
annual_totals = df.groupby('year')['precipitation_mm'].sum()
bars = ax1.bar(annual_totals.index, annual_totals.values, color='#0284C7', edgecolor='#0369A1', alpha=0.85)
ax1.set_title('RESCUE-X: Cuddalore District 10-Year Annual Precipitation (2015-2024)', fontsize=12, fontweight='bold', fontname='Cambria')
ax1.set_xlabel('Year', fontsize=10, fontname='Cambria')
ax1.set_ylabel('Total Precipitation (mm)', fontsize=10, fontname='Cambria')
ax1.set_xticks(annual_totals.index)
for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 20, f'{int(yval)}', ha='center', va='bottom', fontsize=8, fontname='Cambria')

# 1b. Monthly Monsoon Profile (Seasonality)
monthly_mean = df.groupby('month')['precipitation_mm'].sum() / 10.0 # 10 years
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ax2.plot(months, monthly_mean.values, marker='o', linewidth=2.5, color='#DC2626', label='Mean Monthly Rainfall (mm)')
ax2.fill_between(months, monthly_mean.values, color='#FCA5A5', alpha=0.3)
ax2.set_title('Northeast Monsoon Seasonality Profile (Peak Inundation Window: Oct - Dec)', fontsize=12, fontweight='bold', fontname='Cambria')
ax2.set_xlabel('Month', fontsize=10, fontname='Cambria')
ax2.set_ylabel('Average Rainfall (mm)', fontsize=10, fontname='Cambria')
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend(loc='upper left', prop={'family': 'Cambria'})

plt.tight_layout()
mpl_path = os.path.join(FIG_DIR, 'rainfall_trend_analysis.png')
plt.savefig(mpl_path)
plt.close()
print(f"Saved Matplotlib figure to {mpl_path}")

# -------------------------------------------------------------
# 2. PLOTLY: Historic Flood Events Comparison (Interactive)
# -------------------------------------------------------------
# Filter top 3 cyclonic/flood windows: Nov 2015, Nov 2020, Nov-Dec 2024
nov_2015 = df[(df['date'] >= '2015-11-01') & (df['date'] <= '2015-12-10')].copy()
nov_2020 = df[(df['date'] >= '2020-11-15') & (df['date'] <= '2020-12-10')].copy()
nov_2024 = df[(df['date'] >= '2024-11-15') & (df['date'] <= '2024-12-10')].copy()

fig_deluge = go.Figure()
fig_deluge.add_trace(go.Bar(
    x=nov_2015['date'], y=nov_2015['precipitation_mm'],
    name='Nov-Dec 2015 (Historic Catastrophic Deluge)',
    marker_color='#DC2626'
))
fig_deluge.add_trace(go.Scatter(
    x=nov_2015['date'], y=nov_2015['rolling_3d_rain_mm'],
    name='2015 3-Day Cumulative Soil Saturation',
    line=dict(color='#991B1B', width=2, dash='dot')
))
fig_deluge.update_layout(
    title='<b>RESCUE-X: 2015 Cuddalore Historic Flood Deluge Analysis (Daily mm vs 3-Day Cumulative)</b>',
    xaxis_title='Observation Date',
    yaxis_title='Precipitation (mm)',
    font=dict(family='Cambria, serif', size=12),
    template='plotly_white',
    hovermode='x unified'
)

plotly_deluge_html = os.path.join(NOTEBOOK_DIR, 'deluge_2015_analysis.html')
fig_deluge.write_html(plotly_deluge_html)
print(f"Saved Plotly 2015 Deluge figure to {plotly_deluge_html}")

# -------------------------------------------------------------
# 3. PLOTLY: Evacuation Route & Population Exposure Comparison
# -------------------------------------------------------------
fig_routes = make_subplots(
    rows=1, cols=2,
    subplot_titles=(
        '<b>Evacuation Route Clearance: Distance vs Travel Time</b>',
        '<b>Hazard Exposure Index by Route Corridor</b>'
    )
)

routes = ['Shortest Route (Yellow)', 'Risk-Aware Bypass (Green)']
distances = [3.2, 4.8]
times = [12, 19]
risks = [74, 18]

# Subplot 1: Distance & Time
fig_routes.add_trace(go.Bar(name='Distance (km)', x=routes, y=distances, marker_color='#2563EB'), row=1, col=1)
fig_routes.add_trace(go.Bar(name='Travel Time (mins)', x=routes, y=times, marker_color='#EAB308'), row=1, col=1)

# Subplot 2: Hazard Risk
fig_routes.add_trace(go.Bar(
    name='Hazard Risk (%)', x=routes, y=risks,
    marker_color=['#DC2626', '#16A34A'],
    text=[f'{r}%' for r in risks], textposition='auto'
), row=1, col=2)

fig_routes.update_layout(
    font=dict(family='Cambria, serif', size=12),
    template='plotly_white',
    showlegend=True,
    barmode='group'
)

plotly_routes_html = os.path.join(NOTEBOOK_DIR, 'route_comparison_analysis.html')
fig_routes.write_html(plotly_routes_html)
print(f"Saved Plotly Route Comparison figure to {plotly_routes_html}")

print("All Data Science course visualizations successfully generated!")

