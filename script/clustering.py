import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# === 1. Caricamento dati ===
csv_file = "../data/filtered_weekly_link_loads.csv"
df = pd.read_csv(csv_file)

# === 2. Crea grafo non diretto per clustering ===
G = nx.Graph()
for _, row in df.iterrows():
    G.add_edge(row["From"], row["To"], weight=row["Load"], line=row["Line"])

# === 3. Calcola clustering per nodo ===
clustering_dict = nx.clustering(G)

# === 4. Clustering medio ===
avg_clustering = nx.average_clustering(G)
print(f" Clustering medio della rete: {avg_clustering:.4f}")

# === 5. Esporta CSV ===
clustering_df = pd.DataFrame(clustering_dict.items(), columns=["Station", "Clustering"])
clustering_df.to_csv("clustering_coefficients.csv", index=False)
print(" Dati salvati in: clustering_coefficients.csv")

# === 6. Grafico distribuzione clustering ===
plt.figure(figsize=(10, 5))
plt.hist(clustering_df["Clustering"], bins=20, color="skyblue", edgecolor="black")
plt.xlabel("Clustering coefficient")
plt.ylabel("Numer of stations")
plt.tight_layout()
plt.savefig("clustering_distribution.png", dpi=300)
plt.show()
print(" Grafico salvato in: clustering_distribution.png")
