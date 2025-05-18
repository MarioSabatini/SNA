import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# === Configurazione ===
csv_file = "../data/filtered_weekly_link_loads.csv"
output_image = "top10_betweenness_barplot.png"

# === Carica dati CSV ===
df = pd.read_csv(csv_file)

# === Costruzione grafo diretto ===
G = nx.DiGraph()
for _, row in df.iterrows():
    G.add_edge(row["From"], row["To"], weight=row["Load"], line=row["Line"])

# === Calcola betweenness centrality pesata ===
print("Calcolo della betweenness centrality...")
betweenness = nx.betweenness_centrality(G, weight="weight", normalized=True)

# === Crea DataFrame e ordina ===
betweenness_df = pd.DataFrame(betweenness.items(), columns=["Station", "Betweenness"])
top10 = betweenness_df.sort_values(by="Betweenness", ascending=False).head(10)

# === Plot grafico a barre ===
plt.figure(figsize=(12, 6))
bars = plt.bar(top10["Station"], top10["Betweenness"], color="#FF5733")
plt.xlabel("Stations")
plt.ylabel("Betweenness Centrality")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# === Salva immagine ===
plt.savefig(output_image, dpi=300)
plt.show()

print(f"\n Grafico salvato come: {output_image}")
