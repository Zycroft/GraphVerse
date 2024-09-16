import torch
from ..graph.walk import generate_multiple_walks
from ..graph.walk import generate_valid_walk

class WalkVocabulary:
    """
    Vocabulary for walks.
    """
    def __init__(self, walks):
        self.token2idx = {'<PAD>': 0, '<START>': 1, '<END>': 2}
        self.idx2token = {0: '<PAD>', 1: '<START>', 2: '<END>'}
        self.build_vocab(walks)

    def build_vocab(self, walks):
        for walk in walks:
            for token in walk:
                if str(token) not in self.token2idx:
                    idx = len(self.token2idx)
                    self.token2idx[str(token)] = idx
                    self.idx2token[idx] = str(token)

    def __len__(self):
        return len(self.token2idx)

def prepare_training_data(graph, num_samples, min_length, max_length, rules):
    """
    Prepare training data for the model.
    """
    print(f"Generating a walk starting from each node in the graph...")
    per_node_walks = []
    for node in graph.nodes:
        print(f"Generating a walk starting from node {node}")
        valid_walk = generate_valid_walk(graph, node, min_length, max_length, rules)
        if valid_walk:
            per_node_walks.append(valid_walk)
        print()  # Print a new line after each iteration
    
    # Generate walks
    walks = generate_multiple_walks(graph, num_samples, min_length, max_length, rules)

    walks = walks + per_node_walks

    # Create vocabulary
    vocab = WalkVocabulary(walks)
    
    tensor_data = []
    for walk in walks:
        tensor_walk = [vocab.token2idx['<START>']] + [vocab.token2idx[str(node)] for node in walk] + [vocab.token2idx['<END>']]
        tensor_data.append(torch.tensor(tensor_walk))
    
    return torch.nn.utils.rnn.pad_sequence(tensor_data, batch_first=True, padding_value=vocab.token2idx['<PAD>']), vocab