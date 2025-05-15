import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# === 1. Carica CSV ===
df = pd.read_csv("filtered_weekly_link_loads.csv")

# === 2. Costruisci grafo non diretto ===
G = nx.Graph()
for _, row in df.iterrows():
    G.add_edge(row["From"], row["To"], weight=row["Load"])

# === 3. Trova i nodi critici (articulation points) ===
cut_nodes = list(nx.articulation_points(G))
print(f" Trovati {len(cut_nodes)} nodi critici.")
print(" Esempi:", cut_nodes[:10])

# === 4. Visualizzazione ===
pos = nx.spring_layout(G, seed=42, k=10.0, iterations=500)


plt.figure(figsize=(16, 14))

# Nodi normali (grigi)
normal_nodes = [n for n in G.nodes if n not in cut_nodes]
nx.draw_networkx_nodes(G, pos, nodelist=normal_nodes, node_color="#cccccc", node_size=80)

# Nodi critici (rossi)
nx.draw_networkx_nodes(G, pos, nodelist=cut_nodes, node_color="#ff3333", node_size=200, label="Critical Nodes")

# Archi
nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color="#999999", width=1)

# Etichette solo per i nodi critici
nx.draw_networkx_labels(G, pos, labels={n: n for n in cut_nodes}, font_size=3, font_weight="bold")


plt.legend(loc="upper left")
plt.axis("off")
plt.tight_layout()

# === 5. Salva immagine ===
plt.savefig("articulation_points_graph.png", dpi=300)
plt.show()

# === 6. Salva lista in CSV ===
pd.DataFrame(cut_nodes, columns=["Critical_Station"]).to_csv("articulation_points.csv", index=False)
print(" Grafico e lista salvati.")
