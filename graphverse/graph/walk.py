import random
from .rules import Rule

def check_rule_compliance(walk, graph, rules):
    return all(rule.apply(walk, graph) for rule in rules)

def generate_valid_walk(graph, start_vertex, min_length, max_length, rules):
    """
    Generate a walk that satisfies all rules.
    The walk length will be between min_length and max_length, 
    or shorter if a dead-end is reached while satisfying rules.
    """
    target_length = random.randint(min_length, max_length)
    walk = [start_vertex]
    
    while len(walk) < target_length:
        valid_neighbors = [
            neighbor for neighbor in graph.neighbors(walk[-1])
            if check_rule_compliance(walk + [neighbor], graph, rules)
        ]
        
        if not valid_neighbors:
            break  # Dead-end reached
        
        next_vertex = random.choice(valid_neighbors)
        walk.append(next_vertex)
    
    return walk if len(walk) >= min_length else None

def generate_multiple_walks(graph, num_walks, min_length, max_length, rules):
    """
    Generate multiple valid walks for training data.
    Includes walks that reach dead-ends while satisfying rules.
    """
    walks = []
    attempts = 0
    max_attempts = num_walks * 10  # Arbitrary limit to prevent infinite loops
    
    while len(walks) < num_walks and attempts < max_attempts:
        start_vertex = random.choice(list(graph.nodes))
        walk = generate_valid_walk(graph, start_vertex, min_length, max_length, rules)
        if walk:
            walks.append(walk)
        attempts += 1
    
    return walks