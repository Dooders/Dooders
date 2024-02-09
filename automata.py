""""
Rule 30 specifies that a cell becomes 1 (or "alive") in the next generation if 
    exactly one of the three cells (itself and its two neighbors) was 1 in the 
    previous generation, except for the case where only the cell itself was 1.

We use a one-dimensional array to represent the cells, where 0 indicates a dead 
    cell and 1 indicates a live cell.

The new state of each cell depends on its current state and the states of its 
    left and right neighbors.
"""

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn


def apply_ca_rule(cells, rule_number):
    rule_binary = f"{rule_number:08b}"
    next_gen = []
    for i in range(len(cells)):
        left = cells[i - 1] if i > 0 else 0
        center = cells[i]
        right = cells[i + 1] if i < len(cells) - 1 else 0
        neighborhood = 4 * left + 2 * center + right
        next_state = int(rule_binary[-1 - neighborhood])
        next_gen.append(next_state)
    return next_gen


def generate_automata(rule_number, initial_state, num_generations):
    generations = [initial_state]
    for _ in range(num_generations - 1):
        next_gen = apply_ca_rule(generations[-1], rule_number)
        generations.append(next_gen)
    return np.array(generations)


# Parameters
rule_number = 30  # Rule number
num_cells = 101  # Number of cells in a row
num_generations = 100  # Number of generations
initial_state = [0] * num_cells  # Initialize with all zeros
initial_state[num_cells // 2] = 1  # Set the middle cell to 1

# Generate the cellular automata
# automata = generate_automata(rule_number, initial_state, num_generations)

# # Visualize the cellular automata
# plt.figure(figsize=(10, 10))
# plt.imshow(automata, cmap="binary", interpolation="nearest")
# plt.title(f"Cellular Automata Rule {rule_number}")
# plt.axis("off")
# plt.show()


# Generate training data
def generate_data(size=10000, length=15):
    data = []
    labels = []
    for _ in range(size):
        current_gen = np.random.randint(2, size=length)
        next_gen = apply_ca_rule(current_gen, rule_number)
        data.append(current_gen)
        labels.append(next_gen)
    return torch.tensor(data, dtype=torch.float32), torch.tensor(
        labels, dtype=torch.float32
    )


# Define a simple 1D CNN model
class Rule30CNN(nn.Module):
    def __init__(self):
        super(Rule30CNN, self).__init__()
        self.conv1 = nn.Conv1d(1, 10, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(10 * length, length)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = x.view(-1, 10 * length)
        x = torch.sigmoid(self.fc1(x))
        return x


# Prepare the data
length = 15
data, labels = generate_data(length = length)
data = data.view(-1, 1, length)
labels = labels.view(-1, length)
split = int(0.8 * len(data))
train_data, test_data = data[:split], data[split:]
train_labels, test_labels = labels[:split], labels[split:]

# Initialize the model, loss function, and optimizer
model = Rule30CNN()
criterion = nn.BCELoss()  # Binary Cross Entropy Loss for binary classification
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training loop
epochs = 9000
for epoch in range(epochs):
    optimizer.zero_grad()
    output = model(train_data)
    loss = criterion(output, train_labels)
    loss.backward()
    optimizer.step()
    if epoch % 10 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item()}")

# Evaluation
with torch.no_grad():
    test_output = model(test_data)
    test_loss = criterion(test_output, test_labels)
    print(f"Test Loss: {test_loss.item()}")
