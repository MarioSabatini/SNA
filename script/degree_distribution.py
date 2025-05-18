import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import powerlaw

# 1. Carica il CSV
df = pd.read_csv("../data/filtered_weekly_link_loads.csv")

# 2. Crea il grafo
G = nx.Graph()
edges = list(zip(df['From'], df['To']))
G.add_edges_from(edges)

# 3. Calcola il grado dei nodi
degrees = np.array([d for n, d in G.degree()])

# 4. Fit della distribuzione di potenza
fit = powerlaw.Fit(degrees, discrete=True)

# Parametri stimati
alpha = fit.alpha
xmin = fit.xmin
p_value = fit.distribution_compare('power_law', 'lognormal')[1]

print("\n--- Power-law Fit Summary ---")
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")
print(f"Estimated alpha: {alpha:.4f}")
print(f"Estimated xmin: {xmin}")
print(f"p-value (vs. lognormal): {p_value:.4f}")

# 5. Plot della CCDF e del fit
plt.figure(figsize=(8,6))
fig = fit.plot_ccdf(linewidth=2, label='Empirical CCDF')
fit.power_law.plot_ccdf(ax=fig, color='r', linestyle='--', label='Power-law fit')
plt.xlabel("Degree")
plt.ylabel("P(X ≥ x)")
plt.title("Degree Distribution (log-log CCDF)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 6. (Opzionale) Salva gradi su CSV
degree_df = pd.DataFrame(G.degree(), columns=["Station", "Degree"])
degree_df.to_csv("node_degrees.csv", index=False)