import networkx as nx
import math
import random


def generate_random_graph(n):
    # Calculate the desired edge density
    edge_density = math.log(n) / n

    # Calculate the number of edges based on the density
    num_edges = int(edge_density * n * (n - 1))

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes
    G.add_nodes_from(range(n))

    # Add random edges
    edges = []
    while len(edges) < num_edges:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v and (u, v) not in edges:
            edges.append((u, v))

    G.add_edges_from(edges)

    # Ensure the graph is connected
    if not nx.is_strongly_connected(G):
        components = list(nx.strongly_connected_components(G))
        for i in range(len(components) - 1):
            u = random.choice(list(components[i]))
            v = random.choice(list(components[i+1]))
            G.add_edge(u, v)

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
