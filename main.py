import networkx as nx
import matplotlib.pyplot as plt
import torch
import pandas as pd
import math

from graphverse.graph.graph_generation import generate_random_graph, calculate_edge_density
from graphverse.graph.rules import AscenderRule, DescenderRule, EvenRule, OddRule
from graphverse.graph.rules import define_ascenders, define_descenders, define_evens_odds
from graphverse.data.preparation import prepare_training_data
from graphverse.llm.training import train_model
from graphverse.llm.evaluation import evaluate_model

def main():
    # Generate graph
    n = 1000  # Number of vertices
    c = 1.1   # Constant factor
    G = generate_random_graph(n)

    # Print some information about the graph
    print(f"Number of nodes: {G.number_of_nodes()}")
    print(f"Number of edges: {G.number_of_edges()}")
    print(f"Is strongly connected: {nx.is_strongly_connected(G)}")
    print(f"Is wealky connected: {nx.is_weakly_connected(G)}")

    # Print the probability distribution for a few nodes
    for node in range(min(5, n)):
      print(f"\nProbability distribution for node {node}:")
    for u, v, data in G.out_edges(node, data=True):
        print(f"  Edge ({u}, {v}): {data['probability']:.4f}")

    # Define rule sets
    ascenders = define_ascenders(G, n)
    descenders = define_descenders(G, n)
    evens, odds = define_evens_odds(G, n)

    # Create rule tuple
    rules = (
    AscenderRule(ascenders),
    DescenderRule(descenders),
    EvenRule(evens),
    OddRule(odds)
)

    # Prepare training data
    training_data, vocab = prepare_training_data(G, num_samples=10000, min_length=10, max_length=50, rules=rules)

    # Train the model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = train_model(training_data, vocab, epochs=10, batch_size=32, learning_rate=0.001, device=device)

    # Evaluate the model
    max_corpus_length = training_data.size(1)  # Get the maximum sequence length
    evaluation_results = evaluate_model(model, G, vocab, num_samples=1000,
                                        min_start_length=1, max_start_length=int(0.1 * max_corpus_length),
                                        ascenders=ascenders, descenders=descenders, evens=evens, odds=odds)

    # Analyze results
    df_results = pd.DataFrame(evaluation_results)

    print("\nEvaluation Results:")
    print(f"Average rule violations: {df_results['rule_violations'].mean():.2f}")
    print(f"Average generated walk length: {df_results['generated_length'].mean():.2f}")

    # Optional: Save results to a CSV file
    df_results.to_csv('evaluation_results.csv', index=False)
    print("Detailed results saved to 'evaluation_results.csv'")

if __name__ == "__main__":
    main()
