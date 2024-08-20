from ..graph.walk import check_rule_compliance
from .token_generation import seed_walk
import random


def evaluate_model(model, graph, vocab, num_samples, min_start_length, max_start_length, rules):
    results = []

    for _ in range(num_samples):
        start_length = random.randint(min_start_length, max_start_length)
        start_sequence = random.choices(list(graph.nodes()), k=start_length)
        generated_walk = generate_walk(
            model, start_sequence, max_length=100, vocab=vocab)

        rule_violations = count_rule_violations(generated_walk, graph, rules)
        results.append({
            'start_length': start_length,
            'generated_length': len(generated_walk),
            'rule_violations': rule_violations
        })

    return results


def count_rule_violations(walk, graph, rules):
    violations = 0
    for i in range(len(walk)):
        if not check_rule_compliance(walk[:i+1], graph, rules):
            violations += 1
    return violations
