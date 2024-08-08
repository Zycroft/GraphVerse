import random
from ..graph.rules import check_rule_compliance
from .token_generation import seed_walk

def evaluate_model(model, graph, vocab, num_samples, min_start_length, max_start_length, ascenders, descenders, evens, odds):
    results = []
    
    for _ in range(num_samples):
        start_length = random.randint(min_start_length, max_start_length)
        start_sequence = random.choices(list(graph.nodes()), k=start_length)
        generated_walk = seed_walk(model, start_sequence, max_length=100, vocab=vocab)
        
        rule_violations = count_rule_violations(generated_walk, graph, ascenders, descenders, evens, odds)
        results.append({
            'start_length': start_length,
            'generated_length': len(generated_walk),
            'rule_violations': rule_violations
        })
    
    return results

def count_rule_violations(walk, graph, ascenders, descenders, evens, odds):
    violations = 0
    for i in range(len(walk)):
        if not check_rule_compliance(walk[:i+1], graph, ascenders, descenders, evens, odds):
            violations += 1
    return violations

def plot_violations(walk,graph):
    plot =[]
    return plot