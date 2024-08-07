import networkx as nx
import math
import random

def generate_graph(n, c):
    """
    Generate a random graph with n vertices and edge density c*log(n)/n.
    
    :param n: Number of vertices
    :param c: Constant factor for edge density
    :return: NetworkX Graph object
    """
    p = c * math.log(n) / n
    G = nx.erdos_renyi_graph(n, p)
    
    while not nx.is_connected(G):
        components = list(nx.connected_components(G))
        if len(components) > 1:
            comp1 = random.choice(list(components[0]))
            comp2 = random.choice(list(components[1]))
            G.add_edge(comp1, comp2)
    
    return G

def calculate_edge_density(G):
    """
    Calculate the actual edge density of the graph.
    """
    n = G.number_of_nodes()
    m = G.number_of_edges()
    return 2 * m / (n * (n - 1))