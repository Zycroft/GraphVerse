import networkx as nx
import matplotlib.pyplot as plt

# Draw the graph


def visualize_graph(G):
    # Create a new figure
    plt.figure(figsize=(12, 8))

    # Generate a layout for the nodes
    pos = nx.spring_layout(G)

    # Draw the nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')

    # Draw the edges with varying thickness based on probability
    for (u, v, data) in G.edges(data=True):
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=data['probability'] * 5,
                               alpha=0.7, edge_color='gray', arrows=True,
                               arrowsize=20, arrowstyle='->')

    # Draw the node labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

    # Draw the edge labels (probabilities)
    edge_labels = nx.get_edge_attributes(G, 'probability')
    edge_labels = {k: f'{v:.2f}' for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Remove axis
    plt.axis('off')

    # Show the plot
    plt.tight_layout()
    plt.show()
    return


def graph_draw(G):
    pos = nx.spring_layout(G)
    nx.draw(G)
    # nx.draw_networkx(G, arrows=True)
    # plt.show()
    return

    """    
        # values = [val_map.get(node, 0.25) for node in G.nodes()]
        # Specify the edges you want here
        # red_edges = [('A', 'C'), ('E', 'C')]
        edge_colours = ['black']
        # edge_colours = ['black' if not edge in red_edges else 'red'
        #                for edge in G.edges()]
        # black_edges = [edge for edge in G.edges() if edge not in red_edges]
        black_edges = [edge for edge in G.edges()]
        # Need to create a layout when doing
        # separate calls to draw nodes and edges
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
                                node_color='blue', node_size=500)
        nx.draw_networkx_labels(G, pos)
        # nx.draw_networkx_edges(G, pos, edgelist=red_edges,
        #                       edge_color='r', arrows=True)
        nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
        plt.show()
        return
        """
