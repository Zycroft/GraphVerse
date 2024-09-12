import networkx as nx
import math
import random


def generate_random_graph(n, num_in_edges, num_out_edges):
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes
    G.add_nodes_from(range(n))

    # Add edges ensuring minimum in/out degree
    for u in range(n):
        in_neighbors = set()
        out_neighbors = set()
        while len(in_neighbors) < num_in_edges:
            v = random.randint(0, n-1)
            if v != u and (v, u) not in G.edges():
                G.add_edge(v, u)
                in_neighbors.add(v)
        while len(out_neighbors) < num_out_edges:
            v = random.randint(0, n-1)
            if v != u and (u, v) not in G.edges():
                G.add_edge(u, v)
                out_neighbors.add(v)

    # Ensure there exists a walk between any two vertices - incredibly silly method but it works
    while not nx.is_strongly_connected(G):
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if not nx.has_path(G, u, v):
            path = random.sample(range(n), n//2)
            for i in range(len(path)-1):
                G.add_edge(path[i], path[i+1])
            G.add_edge(u, path[0])
            G.add_edge(path[-1], v)

    # Assign random probability distributions to outgoing edges
    for node in G.nodes():
        out_edges = list(G.out_edges(node))
        if out_edges:
            probabilities = [random.random() for _ in range(len(out_edges))]
            total = sum(probabilities)
            normalized_probabilities = [p / total for p in probabilities]
            for (u, v), prob in zip(out_edges, normalized_probabilities):
                G[u][v]['probability'] = prob

    return G


def calculate_edge_density(G):
    """
    Calculate the actual edge density of the graph.
    """
    n = G.number_of_nodes()
    m = G.number_of_edges()
    return 2 * m / (n * (n - 1))


def save_graph(G, path='my_graph.gml'):
    """
    Save the graph to disk.
    """
    nx.write_gml(G, path)
    return True


def load_graph(path='my_graph.gml'):
    """
    Load the Graph from disk.
    """
    G = nx.read_gml(path)
    return G
