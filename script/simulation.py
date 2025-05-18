import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# === 1. Carica dati e crea grafo ===
df = pd.read_csv("../data/filtered_weekly_link_loads.csv")

G_full = nx.Graph()
for _, row in df.iterrows():
    G_full.add_edge(row["From"], row["To"], weight=row["Load"])

# === 2. Layout fisso ===
pos = nx.spring_layout(G_full, seed=42, k=0.35)

# === 3. METRICHE ORIGINALI ===
original_density = nx.density(G_full)
original_connected = nx.is_connected(G_full)
original_clustering = nx.average_clustering(G_full)

# === 4. RIMOZIONE MIRATA (top 5 betweenness) ===
centrality = nx.betweenness_centrality(G_full, weight='weight', normalized=True)
top_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
nodes_to_remove = [n for n, _ in top_nodes]

G_target = G_full.copy()
G_target.remove_nodes_from(nodes_to_remove)

# === 5. METRICHE DOPO LA RIMOZIONE ===
target_density = nx.density(G_target)
target_connected = nx.is_connected(G_target)
target_clustering = nx.average_clustering(G_target)

# === 6. Visualizzazione ===
# Originale
plt.figure(figsize=(15, 12))
nx.draw(G_full, pos, node_color='lightblue', node_size=80, edge_color='#aaaaaa', with_labels=False)
plt.title("Rete originale (completa)")
plt.axis("off")
plt.savefig("grafo_originale.png", dpi=300)
plt.close()

# Dopo rimozione
plt.figure(figsize=(15, 12))
nx.draw(G_target, pos, node_color='lightblue', node_size=80, edge_color='#aaaaaa', with_labels=False)
plt.title("Rimozione mirata (top 5 betweenness)")
plt.axis("off")
plt.savefig("grafo_targeted_removal.png", dpi=300)
plt.close()

# === 7. RISULTATI ===
print("METRICHE A CONFRONTO")
print("→ Rete originale:")
print(f"- Connessa? {'Sì' if original_connected else 'No'}")

print("\n→ Dopo rimozione mirata:")
print(f"- Connessa? {'Sì' if target_connected else 'No'}")
