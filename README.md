# London Underground Network Analysis 🚇

This repository contains the dataset, scripts, and report for a Social Network Analysis project on the **London Underground** system. The project models the transport network as a weighted graph and analyzes its structure using graph-theoretical measures and simulations.

---

## 📁 Repository Structure

```
.
├── data/                 # Dataset files (e.g., links, stations, weights)
├── scripts/              # Python scripts for graph analysis
└── README.md             # Project documentation
```

---

## 📊 Project Overview

### Objective
- Evaluate the **connectivity, resilience**, and **critical nodes** of the London Underground.
- Apply **centrality, clustering, core-periphery**, and **scale-free** analysis.
- Simulate node failures and assess structural vulnerability.

### Methods
- Python + NetworkX for graph modeling and metrics.
- Static and visual analysis of node importance and bottlenecks.
- Resilience simulations under random and targeted attacks.

---

## 🔧 Installation & Usage

### Prerequisites
- Python 3.8+
- `networkx`
- `matplotlib`
- `numpy`
- `pandas`
- `powerlaw` (for degree distribution)

Install dependencies:
```bash
pip install -r requirements.txt
```

### Run Analysis
```bash
cd scripts
python main_analysis.py
```

---

## 📂 Data

Data is derived from public sources (e.g., Transport for London) and includes:
- Station connections and names
- Estimated passenger loads between directly connected stations

---

## 📑 Report

The full report with methodology, figures, and interpretations is available in `/report/` as a PDF and LaTeX source.

---

## 🧠 Authors

- Emanuele Grasso
- Gregorio Petruzzi
- Mario Sabatini

Bachelor's in Computer Science – Social Network Analysis Project @ Sapienza University of Rome

---

## 📜 License

This project is for academic and educational use only. Refer to `LICENSE` for details.

---

## 🚀 Future Work

- Integrate time-based data (e.g., rush hour vs off-peak)
- Explore multilayer models (lines, modes, interchanges)
- Simulate cascading failures and recovery dynamics
