# === coesione_analysis.py ===
import pandas as pd
import networkx as nx

# Carica CSV
df = pd.read_csv("filtered_weekly_link_loads.csv")

# Crea grafo NON diretto per l'analisi della coesione
G = nx.Graph()
for _, row in df.iterrows():
    G.add_edge(row["From"], row["To"], weight=row["Load"])

# Calcola node e edge connectivity
node_conn = nx.node_connectivity(G)
edge_conn = nx.edge_connectivity(G)

print(" ANALISI DELLA COESIONE")
print(f"- Node connectivity: {node_conn}")
print(f"- Edge connectivity: {edge_conn}")

# Interpretazione semplice
if node_conn <= 2:
    print("La rete è vulnerabile: pochi nodi bastano a frammentarla.")
elif node_conn >= 5:
    print("La rete è ben connessa e coesa.")
