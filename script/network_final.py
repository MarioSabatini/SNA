import pandas as pd
import networkx as nx
from pyvis.network import Network

# === Config ===
csv_file = "filtered_weekly_link_loads.csv"
output_file = "grafo_senza_critici.html"

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

# === Load data ===
df = pd.read_csv(csv_file)

# === Build graph ===
G = nx.DiGraph()
for _, row in df.iterrows():
    G.add_edge(row["From"], row["To"], weight=row["Load"], line=row["Line"])

# === Calculate betweenness centrality ===
centrality = nx.betweenness_centrality(G, weight='weight', normalized=True)
top3_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:3]
#nodes_to_remove = [n for n, _ in top3_nodes]

print(" Rimuovendo i nodi critici:")
#for name in nodes_to_remove:
#    print(f"- {name}")

# === Remove critical nodes ===
#G.remove_nodes_from(nodes_to_remove)

# === Create PyVis network ===
net = Network(height="800px", width="100%", directed=True)
net.set_options("""
{
  "physics": {
    "enabled": true,
    "barnesHut": {
      "gravitationalConstant": -20000,
      "centralGravity": 0.3,
      "springLength": 150,
      "springConstant": 0.005,
      "damping": 0.09
    },
    "stabilization": {
      "enabled": true,
      "iterations": 1000,
      "updateInterval": 25
    }
  }
}
""")

# === Add nodes ===
for node in G.nodes():
    size = 10 + centrality.get(node, 0) * 200
    net.add_node(
        node,
        label=node,
        size=size,
        color="#FFFFFF",
        borderWidth=1,
        title=f"Centralità: {centrality.get(node, 0):.4f}"
    )

# === Add edges ===
for u, v, data in G.edges(data=True):
    color = line_colors.get(data["line"], "#999999")
    net.add_edge(
        u, v,
        value=data["weight"],
        color=color,
        title=f"Load: {data['weight']:.0f} - Linea: {data['line']}"
    )

# === Save HTML ===
net.save_graph(output_file)

# === Add legend manually ===
legend_html = """
<div style="position:absolute; top:10px; right:10px; background:#fff; padding:10px; border:1px solid #ccc; font-family:Arial">
<h4>Legenda linee</h4>
<ul style="list-style:none; padding:0; margin:0;">
""" + "\n".join([
    f'<li><span style="display:inline-block;width:12px;height:12px;background:{color};margin-right:6px;"></span>{line}</li>'
    for line, color in line_colors.items()
]) + """
</ul>
</div>
"""

with open(output_file, "r", encoding="utf-8") as f:
    html_content = f.read()

html_with_legend = html_content.replace("</body>", legend_html + "\n</body>")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_with_legend)

print(f"\n Grafo salvato in: {output_file}")
