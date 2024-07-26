import random

def designate_special_vertices(G, percentage=0.05, range_around_middle=1000):
    """
    Designate ascender and descender vertices.
    
    :param G: NetworkX Graph
    :param percentage: Percentage of vertices to designate as special
    :param range_around_middle: Range around n/2 to consider for special vertices
    """
    n = G.number_of_nodes()
    middle = n // 2
    lower_bound = max(0, middle - range_around_middle)
    upper_bound = min(n, middle + range_around_middle)
    
    candidates = list(range(lower_bound, upper_bound))
    num_special = int(n * percentage)
    special_vertices = random.sample(candidates, num_special)
    
    for v in special_vertices:
        G.nodes[v]['special'] = random.choice(['ascender', 'descender'])