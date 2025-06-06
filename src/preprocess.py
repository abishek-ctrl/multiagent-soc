# src/preprocess.py
import numpy as np
import torch
from torch_geometric.data import Data
import os

def load_pems_npz(file_path):
    npz = np.load(file_path, allow_pickle=True)
    data = npz['data']  # shape: (num_samples, num_nodes, num_features)
    W = npz['W']        # shape: (num_nodes, num_nodes)
    return data, W

def normalize_data(data):
    # z-score normalization across time
    mean = data.mean(axis=0, keepdims=True)
    std = data.std(axis=0, keepdims=True)
    return (data - mean) / std, mean, std

def create_edge_index(adj_matrix, threshold=0.1):
    # Create PyG-compatible edge index from adjacency
    edge_index = []
    num_nodes = adj_matrix.shape[0]
    for i in range(num_nodes):
        for j in range(num_nodes):
            if adj_matrix[i, j] > threshold:
                edge_index.append([i, j])
    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
    return edge_index

def create_temporal_graphs(data, edge_index, window_size=12, horizon=1):
    graphs = []
    labels = []
    for t in range(data.shape[0] - window_size - horizon + 1):
        x = data[t:t+window_size]  # shape: (window, nodes, features)
        y = data[t+window_size+horizon-1]  # target snapshot

        x_tensor = torch.tensor(x, dtype=torch.float).transpose(0, 1)  # (nodes, window, features)
        y_tensor = torch.tensor(y, dtype=torch.float)

        graphs.append(Data(x=x_tensor, edge_index=edge_index))
        labels.append(y_tensor)
    return graphs, labels
