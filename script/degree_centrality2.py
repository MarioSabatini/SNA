import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# === Configurazione ===
csv_file = "filtered_weekly_link_loads.csv"
output_image = "top10_degree_centrality_barplot.png"

# === Carica dati ===
df = pd.read_csv(csv_file)

# === Costruzione grafo diretto ===
G = nx.DiGraph()
for _, row in df.iterrows():
    G.add_edge(row["From"], row["To"], weight=row["Load"], line=row["Line"])

# === Calcola degree centrality (in+out normalizzata su n-1) ===
degree_centrality = nx.degree_centrality(G)

# === Crea DataFrame e ordina ===
degree_df = pd.DataFrame(degree_centrality.items(), columns=["Station", "DegreeCentrality"])
top10 = degree_df.sort_values(by="DegreeCentrality", ascending=False).head(10)

# === Plot ===
plt.figure(figsize=(12, 6))
plt.bar(top10["Station"], top10["DegreeCentrality"], color="#3498DB")

plt.xlabel("Stations")
plt.ylabel("Degree Centrality")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# === Salva grafico ===
plt.savefig(output_image, dpi=300)
plt.show()

print(f"\n✅ Grafico salvato come: {output_image}")
