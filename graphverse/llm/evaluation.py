from ..graph.walk import check_rule_compliance, generate_valid_walk

import random
import torch


def evaluate_model(model, graph, vocab, num_samples, min_start_length, max_start_length, rules):
    model.eval()

    evaluation_results = []

    for _ in range(num_samples):
        start_length = random.randint(min_start_length, max_start_length)
        start_walk = generate_valid_walk(graph, random.choice(
            list(graph.nodes)), start_length, start_length, rules)

        input_tensor = torch.tensor([vocab.token2idx[str(node)]
                                    for node in start_walk], dtype=torch.long).unsqueeze(0)

        generated_walk = start_walk[:]
        current_vertex = start_walk[-1]

        while current_vertex in graph.nodes:
            logits = model(input_tensor)
            next_vertex_idx = torch.argmax(logits[0, -1]).item()
            next_vertex = int(vocab.idx2token[next_vertex_idx])

            generated_walk.append(next_vertex)
            input_tensor = torch.cat((input_tensor, torch.tensor(
                [[next_vertex_idx]], dtype=torch.long)), dim=1)

            current_vertex = next_vertex

        rule_violations = []
        for i, rule in enumerate(rules, start=1):
            if not rule.is_satisfied_by(graph, generated_walk):
                violation_info = {
                    'rule_type': type(rule).__name__,
                    'walk_length': len(generated_walk),
                    'violation_position': rule.get_violation_position(graph, generated_walk)
                }
                rule_violations.append(violation_info)

        evaluation_results.append({
            'start_walk': start_walk,
            'generated_walk': generated_walk,
            'rule_violations': rule_violations
        })

    return evaluation_results


def count_rule_violations(walk, graph, rules):
    violations = 0
    for i in range(len(walk)):
        if not check_rule_compliance(walk[:i+1], graph, rules):
            violations += 1
    return violations
