import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# === Parametri ===
THRESHOLD = 0.7
STRATEGY = 'degree'
OUTPUT_FILE = "remaining_nodes_after_collapse.csv"
GRAPH_FOLDER = "collapse_graphs"
SEED = 42  # per layout fisso

# === Carica il CSV e crea il grafo ===
df = pd.read_csv("../data/filtered_weekly_link_loads.csv")
G = nx.DiGraph()
for _, row in df.iterrows():
    G.add_edge(row['From'], row['To'], weight=row['Load'])

initial_n = G.number_of_nodes()
initial_m = G.number_of_edges()
removed_nodes = []

# === Layout fisso (sul grafo completo non orientato) ===
UG_full = G.to_undirected()
fixed_pos = nx.spring_layout(UG_full, seed=SEED)

# === Crea cartella output ===
os.makedirs(GRAPH_FOLDER, exist_ok=True)

def get_next_node(G, strategy='betweenness'):
    if strategy == 'betweenness':
        centrality = nx.betweenness_centrality(G, weight='weight')
    elif strategy == 'degree':
        centrality = dict(G.degree())
    else:
        raise ValueError("Unsupported strategy")
    return max(centrality, key=centrality.get), centrality

def is_collapsed(G, threshold):
    UG = G.to_undirected()
    if not nx.is_connected(UG):
        largest_cc = max(nx.connected_components(UG), key=len)
        return len(largest_cc) < threshold * initial_n
    return False

def draw_graph(G, step, removed_node, largest_cc_size, num_components):
    UG = G.to_undirected()
    largest_cc = max(nx.connected_components(UG), key=len)

    # Colori
    node_colors = []
    for node in UG.nodes():
        if node == removed_node:
            node_colors.append("red")
        elif node in largest_cc:
            node_colors.append("skyblue")
        else:
            node_colors.append("gray")

    plt.figure(figsize=(10, 8))
    nx.draw(
        UG, fixed_pos,
        node_color=node_colors,
        node_size=50,
        edge_color="#cccccc",
        with_labels=False
    )

    # Legenda
    patches = [
        mpatches.Patch(color="skyblue", label="Largest Component"),
        mpatches.Patch(color="gray", label="Disconnected")
    ]
    plt.legend(handles=patches, loc="lower left")

    # Titolo informativo
    title = f"Step {step}: Removed '{removed_node}' – Largest CC: {largest_cc_size} nodes – Components: {num_components}"
    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    filename = f"{GRAPH_FOLDER}/step_{step:02d}_{removed_node.replace(' ', '_')}.png"
    plt.savefig(filename, dpi=300)
    plt.close()

# === Simulazione ===
print("===== Functional Collapse Simulation =====")
print(f"Initial nodes: {initial_n}")
print(f"Initial edges: {initial_m}")
print(f"Collapse threshold: {THRESHOLD*100:.0f}% of original nodes → {int(initial_n * THRESHOLD)}")
print(f"Removal strategy: {STRATEGY}\n")

while not is_collapsed(G, THRESHOLD):
    next_node, centrality_dict = get_next_node(G, strategy=STRATEGY)
    centrality_score = centrality_dict[next_node]
    G.remove_node(next_node)
    removed_nodes.append(next_node)

    UG = G.to_undirected()
    num_components = nx.number_connected_components(UG)
    largest_cc_size = len(max(nx.connected_components(UG), key=len))
    current_n = G.number_of_nodes()
    current_m = G.number_of_edges()
    avg_degree = (2 * current_m) / current_n if current_n > 0 else 0
    density = nx.density(UG)

    step = len(removed_nodes)
    draw_graph(G, step, next_node, largest_cc_size, num_components)

    # Stampa descrittiva
    print(f"[Step {step}] Removed node: {next_node}")
    print(f"  {STRATEGY.title()} score: {centrality_score:.5f}")
    print(f"  Nodes remaining: {current_n}")
    print(f"  Edges remaining: {current_m}")
    print(f"  Avg. degree: {avg_degree:.2f}")
    print(f"  Network density: {density:.5f}")
    print(f"  Connected components: {num_components}")
    print(f"  Largest component size: {largest_cc_size}")
    print("-" * 60)

# === Salvataggio finale ===
remaining_nodes = list(G.nodes())
filtered_df = df[df['From'].isin(remaining_nodes) & df['To'].isin(remaining_nodes)]
filtered_df.to_csv(OUTPUT_FILE, index=False)
print(f"\nSaved remaining edges to: {OUTPUT_FILE}")
print(f"Graphs saved in: {GRAPH_FOLDER}/")