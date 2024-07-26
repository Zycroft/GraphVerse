import torch
import torch.nn as nn
import torch.optim as optim
from .model import SimpleTransformer

def train_llm(walks, num_vertices, d_model=128, nhead=4, num_layers=2, epochs=10, batch_size=32):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleTransformer(num_vertices, d_model, nhead, num_layers).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters())

    walk_tensors = [torch.tensor(walk, dtype=torch.long) for walk in walks]

    for epoch in range(epochs):
        total_loss = 0
        for i in range(0, len(walk_tensors), batch_size):
            batch = walk_tensors[i:i+batch_size]
            batch = nn.utils.rnn.pad_sequence(batch, batch_first=True).to(device)
            
            input_seq = batch[:, :-1]
            target_seq = batch[:, 1:]

            output = model(input_seq)
            loss = criterion(output.view(-1, num_vertices), target_seq.view(-1))

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss:.4f}")

    return model