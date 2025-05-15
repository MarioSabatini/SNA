import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# === 1. Carica il CSV ===
csv_file = "filtered_weekly_link_loads.csv"
df = pd.read_csv(csv_file)

# === 2. Crea grafo non diretto ===
G = nx.Graph()
for _, row in df.iterrows():
    G.add_edge(row["From"], row["To"], weight=row["Load"], line=row["Line"])

# === 3. Calcola core number per ogni nodo ===
core_numbers = nx.core_number(G)
max_core = max(core_numbers.values())

print(f"🔍 Core massimo: {max_core}")
print("📌 Esempi di nodi nel core massimo:")
for node, k in core_numbers.items():
    if k == max_core:
        print(f"- {node} (core={k})")


# === 4. Visualizzazione ===
pos = nx.spring_layout(G, seed=42, k=10.0, iterations=500)
node_colors = [core_numbers[n] for n in G.nodes()]
node_sizes = [200 + 100 * core_numbers[n] for n in G.nodes()]

plt.figure(figsize=(16, 14))
nodes = nx.draw_networkx_nodes(
    G, pos,
    node_color=node_colors,
    cmap=plt.cm.viridis,
    node_size=node_sizes
)
nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color="#888888", width=1)
nx.draw_networkx_labels(G, pos, font_size=4)

# Aggiungi colorbar
cbar = plt.colorbar(nodes)
cbar.set_label("Core Number")

plt.axis("off")
plt.tight_layout()
plt.savefig("core_periphery_graph.png", dpi=300)
plt.show()

print("✅ Grafo salvato in: core_periphery_graph.png")
