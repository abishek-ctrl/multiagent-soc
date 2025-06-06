# main.py
from src.data_loader import load_pems_dataset

graphs, labels, mean, std, edge_index = load_pems_dataset("PEMS04")

print("Number of graph snapshots:", len(graphs))
print("Graph example:")
print(graphs[0])
