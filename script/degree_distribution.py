import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import powerlaw  # pip install powerlaw

# === Configurazione ===
csv_file = "filtered_weekly_link_loads.csv"
directed = True  # True per DiGraph (rete direzionale)

# === Carica dati ===
df = pd.read_csv(csv_file)

# === Costruisci grafo ===
G = nx.DiGraph() if directed else nx.Graph()
for _, row in df.iterrows():
    G.add_edge(row["From"], row["To"], weight=row["Load"], line=row["Line"])

# === Calcola gradi ===
degree_sequence = [d for n, d in G.degree()]
degree_count = Counter(degree_sequence)
degrees = sorted(degree_count)
counts = [degree_count[d] for d in degrees]

# === Plot: Distribuzioni ===
plt.figure(figsize=(12, 5))

# 1. Lineare
plt.subplot(1, 2, 1)
plt.bar(degrees, counts, width=0.8, color="skyblue")
plt.title("Degree Distribution (linear)")
plt.xlabel("Degree")
plt.ylabel("Number of Nodes")

# 2. Log-log
plt.subplot(1, 2, 2)
plt.scatter(degrees, counts, color="red", marker="o")
plt.xscale("log")
plt.yscale("log")
plt.title("Degree Distribution (log-log)")
plt.xlabel("log(Degree)")
plt.ylabel("log(Nodes)")

plt.tight_layout()
plt.savefig("degree_distribution_plots.png", dpi=300)
plt.show()

# === Fit legge di potenza ===
fit = powerlaw.Fit(degree_sequence, discrete=True, verbose=False)
alpha = fit.power_law.alpha
xmin = fit.power_law.xmin
p_value = fit.power_law.KS()

print("\n Risultati power law fit:")
print(f"- α (esponente): {alpha:.4f}")
print(f"- x_min (cutoff): {xmin}")
print(f"- p-value: {p_value:.4f}")

# (Facoltativo) Confronto tra power law e lognormal
R, p = fit.distribution_compare('power_law', 'lognormal')
print(f"- Confronto con lognormal → R: {R:.4f}, p-value: {p:.4f}")

