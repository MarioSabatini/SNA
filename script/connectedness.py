import pandas as pd
import networkx as nx

# === Caricamento CSV ===
csv_file = "filtered_weekly_link_loads.csv"
df = pd.read_csv(csv_file)

# === Costruzione del grafo diretto ===
G_directed = nx.DiGraph()
for _, row in df.iterrows():
    G_directed.add_edge(row["From"], row["To"], weight=row["Load"], line=row["Line"])

# === Conversione a grafo non diretto ===
G = G_directed.to_undirected()

# === Analisi della connettività ===
is_connected = nx.is_connected(G)
num_components = nx.number_connected_components(G)
components = list(nx.connected_components(G))
largest_component_size = max(len(c) for c in components)

# === Risultati ===
print("\n📊 Connectedness della rete:")
print(f"- La rete è connessa? {'Sì' if is_connected else 'No'}")
print(f"- Numero di componenti connesse: {num_components}")
print(f"- Numero di nodi nella componente più grande: {largest_component_size}")
print(f"- Numero totale di nodi: {G.number_of_nodes()}")
