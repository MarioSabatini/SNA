import pandas as pd
import matplotlib.pyplot as plt

# === 1. Carica CSV ===
df = pd.read_csv("filtered_weekly_link_loads.csv")

# === 2. Calcola traffico in uscita e in entrata ===
traffico_uscita = df.groupby("From")["Load"].sum()
traffico_entrata = df.groupby("To")["Load"].sum()

# === 3. Traffico totale per stazione ===
traffico_totale = (traffico_uscita + traffico_entrata).sort_values(ascending=False)

# === 4. Top 10 stazioni ===
top10 = traffico_totale.head(10)

# === 5. Salva CSV con tutti i dati ===
traffico_totale.to_csv("traffico_totale_per_stazione.csv", header=["Totale_Load"])

# === 6. Grafico ===
plt.figure(figsize=(12, 6))
top10.plot(kind='bar', color='teal')
plt.ylabel("Load")
plt.xlabel("Stations")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.grid(axis='y')
plt.savefig("top10_stazioni_traffico.png", dpi=300)
plt.show()

print("✅ Dati e grafico salvati:")
print("- top10_stazioni_traffico.png")
print("- traffico_totale_per_stazione.csv")
