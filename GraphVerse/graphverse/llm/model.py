import torch
import torch.nn as nn
import math

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x):
        return x + self.pe[:x.size(0)]

class SimpleTransformer(nn.Module):
    """
    A simple transformer model for graph data.

    Args:
        num_vertices (int): The number of vertices in the graph.
        d_model (int): The dimensionality of the input and output embeddings.
        nhead (int): The number of attention heads in the transformer.
        num_layers (int): The number of transformer layers.

    Attributes:
        embedding (nn.Embedding): The embedding layer for input vertices.
        pos_encoder (PositionalEncoding): The positional encoding layer.
        transformer_encoder (nn.TransformerEncoder): The transformer encoder.
        fc_out (nn.Linear): The linear layer for output prediction.

    """

    def __init__(self, num_vertices, d_model, nhead, num_layers):
        super().__init__()
        self.embedding = nn.Embedding(num_vertices, d_model)
        self.pos_encoder = PositionalEncoding(d_model)
        encoder_layers = nn.TransformerEncoderLayer(d_model, nhead, dim_feedforward=4*d_model)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers)
        self.fc_out = nn.Linear(d_model, num_vertices)

    def forward(self, src):
        src = self.embedding(src) * math.sqrt(self.embedding.embedding_dim)
        src = self.pos_encoder(src)
        output = self.transformer_encoder(src)
        return self.fc_out(output)