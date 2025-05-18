import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# === Config ===
csv_file = "../data/filtered_weekly_link_loads.csv"
output_image = "grafo_statico_completo.png"

# === Line colors ===
line_colors = {
    "Bakerloo": "#B36305",
    "Central": "#E32017",
    "Circle": "#FFD300",
    "District": "#00782A",
    "H&C and Circle": "#F3A9BB",
    "Jubilee": "#A0A5A9",
    "Metropolitan": "#9B0056",
    "Northern": "#000000",
    "Piccadilly": "#003688",
    "Victoria": "#0098D4",
    "Waterloo & City": "#95CDBA"
}

# === Load dataset ===
df = pd.read_csv(csv_file)

# === Build the graph ===
G = nx.DiGraph()
for _, row in df.iterrows():
    G.add_edge(row["From"], row["To"], weight=row["Load"], line=row["Line"])

# === Compute centrality ===
centrality = nx.betweenness_centrality(G, weight='weight', normalized=True)

# === Layout ===
pos = nx.spring_layout(G, seed=42, k=35,iterations=200)

# === Node sizes ===
node_sizes = [100 + centrality.get(n, 0) * 1500 for n in G.nodes()]

# === Determine top 10% nodes by degree for labeling ===
degrees = dict(G.degree())
sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
top_n = max(1, int(0.1 * len(sorted_degrees)))  # Ensure at least one node is labeled
top_nodes = {node for node, _ in sorted_degrees[:top_n]}

# === Create labels dictionary ===
labels = {n: n for n in G.nodes() if n in top_nodes}

# === Draw ===
plt.figure(figsize=(20, 16))
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="#FFFFFF", edgecolors='black', linewidths=0.6)

# Draw colored edges by line
for u, v, data in G.edges(data=True):
    color = line_colors.get(data['line'], '#999999')
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color=color, width=2, alpha=0.6)

# Draw labels for top nodes
nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, font_weight='bold')

# === Legend ===
legend_elements = [
    Patch(facecolor=color, edgecolor='black', label=line)
    for line, color in line_colors.items()
]
plt.legend(handles=legend_elements, title="Tube Lines", loc="upper left", fontsize=9, frameon=True)


plt.axis("off")
plt.tight_layout()
plt.savefig(output_image, dpi=300)
plt.show()

print(f"\n✅ Full network graph saved as: {output_image}")
