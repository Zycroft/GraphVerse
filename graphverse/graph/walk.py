import random
from .rules import Rule

def check_rule_compliance(graph, walk, rules):
    return all(rule.apply(graph, walk) for rule in rules)

def generate_valid_walk(graph, start_vertex, min_length, max_length, rules, max_attempts=10):
    """
    Generate a walk that satisfies all rules.
    The walk length will be between min_length and max_length, 
    or shorter if a dead-end is reached while satisfying rules.
    """
    target_length = random.randint(min_length, max_length)
    walk = [start_vertex]
    attempts = 0
    
    print(f"Starting walk from node {start_vertex}")
    
    while len(walk) < target_length:
        valid_neighbors = [
            neighbor for neighbor in graph.neighbors(walk[-1])
            if check_rule_compliance(graph, walk + [neighbor], rules)
        ]
        
        if not valid_neighbors:
            attempts += 1
            
            if attempts >= max_attempts:
                print(f"Maximum attempts reached. Restarting walk from node {start_vertex}")
                walk = [start_vertex]
                attempts = 0
            else:
                # Backtrack to the previous vertex and try again
                walk.pop()
        else:
            next_vertex = random.choice(valid_neighbors)
            walk.append(next_vertex)
    
    if len(walk) >= min_length:
        print(f"Valid walk generated: {walk}")
        return walk
    else:
        print(f"Failed to generate a valid walk from node {start_vertex}")
        return None

def generate_multiple_walks(graph, num_walks, min_length, max_length, rules):
    """
    Generate multiple valid walks for training data.
    Includes walks that reach dead-ends while satisfying rules.
    """
    walks = []
    attempts = 0
    max_attempts = 10  # Arbitrary limit to prevent infinite loops
    
    while len(walks) < num_walks and attempts < max_attempts:
        print(f"On walk {len(walks)} out of {num_walks}")
        start_vertex = random.choice(list(graph.nodes))
        walk = generate_valid_walk(graph, start_vertex, min_length, max_length, rules)
        if walk:
            walks.append(walk)
        attempts += 1
    
    return walks