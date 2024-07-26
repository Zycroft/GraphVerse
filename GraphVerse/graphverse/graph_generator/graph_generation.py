import networkx as nx
import random
import math

def generate_interesting_graph(n, c=5):
    """
    Generate a random graph with n vertices that is likely to be connected but not complete.
    
    :param n: Number of vertices
    :param c: Constant factor for edge probability
    :return: NetworkX Graph
    """
    p = c * math.log(n) / n
    G = nx.erdos_renyi_graph(n, p)
    
    # Ensure the graph is connected
    while not nx.is_connected(G):
        components = list(nx.connected_components(G))
        if len(components) > 1:
            comp1, comp2 = components[0], components[1]
            v1, v2 = random.choice(list(comp1)), random.choice(list(comp2))
            G.add_edge(v1, v2)
    
    return G