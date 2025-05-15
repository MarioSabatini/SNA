
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point, LineString
import numpy as np

# Load data
link_df = pd.read_csv("../data/filtered_weekly_link_loads.csv")
stations_df = pd.read_csv("../data/London stations.csv")

# Remove missing coordinates
stations_df = stations_df.dropna(subset=["Latitude", "Longitude"])

# Create GeoDataFrame of stations
stations_df["geometry"] = stations_df.apply(lambda row: Point(row["Longitude"], row["Latitude"]), axis=1)
stations_gdf = gpd.GeoDataFrame(stations_df, geometry="geometry", crs="EPSG:4326")
stations_gdf = stations_gdf.to_crs(epsg=3857)

# Build coordinate dictionary in Web Mercator
coord_dict = {row['Station']: row['geometry'] for _, row in stations_gdf.iterrows()}

# Calculate traffic (sum of loads for each station)
traffic = {}
for _, row in link_df.iterrows():
    traffic[row['From']] = traffic.get(row['From'], 0) + row['Load']
    traffic[row['To']] = traffic.get(row['To'], 0) + row['Load']

# Normalize traffic values for plotting
traffic_values = np.array(list(traffic.values()))
min_val, max_val = traffic_values.min(), traffic_values.max()
normalized_traffic = {k: (traffic[k] - min_val) / (max_val - min_val) for k in traffic}

# Create edges as lines between stations
lines = []
for _, row in link_df.iterrows():
    if row['From'] in coord_dict and row['To'] in coord_dict:
        lines.append(LineString([coord_dict[row['From']], coord_dict[row['To']]]))
edges_gdf = gpd.GeoDataFrame(geometry=lines, crs="EPSG:3857")

# Plot
fig, ax = plt.subplots(figsize=(12, 10))

# Plot edges
edges_gdf.plot(ax=ax, linewidth=0.5, color="gray", alpha=0.5)

# Plot nodes with color based on traffic
stations_gdf["traffic_norm"] = stations_gdf["Station"].map(normalized_traffic).fillna(0)
stations_gdf.plot(ax=ax,
                  markersize=40,
                  column="traffic_norm",
                  cmap="plasma",
                  legend=True,
                  alpha=0.9)

# Add OpenStreetMap background
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# Customize plot
ax.set_title("London Underground Network on OpenStreetMap (Traffic Highlighted)", fontsize=14)
ax.set_axis_off()
plt.tight_layout()
plt.savefig("../figures/london_underground_osm_traffic.png", dpi=300)
plt.show()
