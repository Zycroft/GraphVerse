import networkx as nx
import matplotlib.pyplot as plt
import torch
import pandas as pd
import math

from graphverse.graph.generation import generate_graph, calculate_edge_density
from graphverse.graph.rules import define_ascenders, define_descenders, define_evens_odds
from graphverse.data.preparation import prepare_training_data
from graphverse.llm.training import train_model
from graphverse.llm.evaluation import evaluate_model

def main():
    # Generate graph
    n = 1000  # Number of vertices
    c = 1.1   # Constant factor
    graph = generate_graph(n, c)

    # Calculate and print the actual edge density
    actual_density = calculate_edge_density(graph)
    expected_density = c * math.log(n) / n

    print(f"Number of nodes: {n}")
    print(f"Number of edges: {graph.number_of_edges()}")
    print(f"Expected edge density: {expected_density:.6f}")
    print(f"Actual edge density: {actual_density:.6f}")

    # Check connectivity
    print(f"Is the graph connected? {nx.is_connected(graph)}")

    # Define rule sets
    ascenders = define_ascenders(graph, n)
    descenders = define_descenders(graph, n)
    evens, odds = define_evens_odds(graph, n)

    # Prepare training data
    training_data, vocab = prepare_training_data(graph, num_samples=10000, min_length=10, max_length=50, 
                                                 ascenders=ascenders, descenders=descenders, evens=evens, odds=odds)

    # Train the model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = train_model(training_data, vocab, epochs=10, batch_size=32, learning_rate=0.001, device=device)

    # Evaluate the model
    max_corpus_length = training_data.size(1)  # Get the maximum sequence length
    evaluation_results = evaluate_model(model, graph, vocab, num_samples=1000, 
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