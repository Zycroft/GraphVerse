import random

def define_ascenders(graph, n):
    """Define ascender vertices near n/2."""
    mid = n // 2
    range_start = int(mid * 0.9)
    range_end = int(mid * 1.1)
    candidates = [v for v in graph.nodes() if range_start <= v <= range_end]
    return set(random.sample(candidates, k=len(candidates)//5))

def define_descenders(graph, n):
    """Define descender vertices near n/2."""
    mid = n // 2
    range_start = int(mid * 0.9)
    range_end = int(mid * 1.1)
    candidates = [v for v in graph.nodes() if range_start <= v <= range_end]
    return set(random.sample(candidates, k=len(candidates)//5))

def define_evens_odds(graph, n):
    """Randomly select even and odd vertices."""
    evens = set(random.sample([v for v in graph.nodes() if v % 2 == 0], k=n//10))
    odds = set(random.sample([v for v in graph.nodes() if v % 2 != 0], k=n//10))
    return evens, odds

def check_rule_compliance(walk, graph, ascenders, descenders, evens, odds):
    """Check if a given walk complies with all rules."""
    for i, v in enumerate(walk):
        if v in ascenders:
            if any(walk[j] <= v for j in range(i+1, len(walk))):
                return False
        if v in descenders:
            if any(walk[j] >= v for j in range(i+1, len(walk))):
                return False
        if v in evens:
            if any(walk[j] % 2 != 0 for j in range(i+1, len(walk))):
                return False
        if v in odds:
            if any(walk[j] % 2 == 0 for j in range(i+1, len(walk))):
                return False
    return True