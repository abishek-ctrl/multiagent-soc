# src/data_loader.py
import os
from src.preprocess import load_pems_npz, normalize_data, create_edge_index, create_temporal_graphs

def load_pems_dataset(dataset_name="PEMS04", base_path="./PeMS-Dataset", window_size=12):
    npz_path = os.path.join(base_path, dataset_name, f"{dataset_name}.npz")
    data, W = load_pems_npz(npz_path)
    
    data, mean, std = normalize_data(data)
    
    edge_index = create_edge_index(W, threshold=0.1)
    
    graphs, labels = create_temporal_graphs(data, edge_index, window_size=window_size)
    
    return graphs, labels, mean, std, edge_index
