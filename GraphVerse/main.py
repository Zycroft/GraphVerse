import math
import random
import torch
from .graph_generator.graph_generation import generate_interesting_graph
from .graph_generator.vertex_designation import designate_special_vertices
from .graph_generator.random_walks import random_walk
from .analysis import analyze_walks, analyze_llm_output
from .llm.training import train_llm
from .llm.inference import generate_sequence

def run_simulation(n=100000, num_walks=None, llm_training_epochs=10):
    G = generate_interesting_graph(n)
    designate_special_vertices(G)
    
    if num_walks is None:
        num_walks = int(n * math.log(n) + n * math.log(math.log(n)))
    
    walks = []
    violating_walks = []
    
    for i in range(num_walks):
        start = random.randint(0, n-1)
        walk, rule_violated, violation_details = random_walk(G, start)
        walks.append(walk)
        
        if rule_violated:
            violating_walks.append((i, walk, violation_details))
    
    analyze_walks(walks, violating_walks)
    
    # Train LLM
    model = train_llm(walks, n, epochs=llm_training_epochs)
    
    # Generate sequences using LLM
    num_sequences = 1000
    max_length = 50
    generated_sequences = []
    for _ in range(num_sequences):
        start = [random.randint(0, n-1) for _ in range(5)]  # 5-vertex prompt
        generated_sequences.append(generate_sequence(model, start, max_length))
    
    # Analyze LLM output
    ascenders = [v for v, data in G.nodes(data=True) if data.get('special') == 'ascender']
    descenders = [v for v, data in G.nodes(data=True) if data.get('special') == 'descender']
    invalid_edges, rule_violations = analyze_llm_output(G, generated_sequences, ascenders, descenders)
    
    return G, walks, violating_walks, model, generated_sequences, invalid_edges, rule_violations

if __name__ == "__main__":
    run_simulation()