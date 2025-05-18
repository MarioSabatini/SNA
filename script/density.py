import pandas as pd
import networkx as nx

# Carica CSV
df = pd.read_csv("../data/filtered_weekly_link_loads.csv")

# Crea grafo diretto
G = nx.DiGraph()
for _, row in df.iterrows():
    G.add_edge(row["From"], row["To"], weight=row["Load"])

# Calcola densità
density = nx.density(G)
print(f" Densità della rete: {density:.4f}")
