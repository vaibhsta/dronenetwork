import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import matplotlib.cm as cm

# Define input, hidden, and output layers
inputs = ['Farm Area', 'Seasonal Factors', 'Pheromone Levels', 'Time of Day', 'Rain', 'Wind', 'Humidity', 'Temperature']
outputs = ['Optimal Drone Path', 'Optimal Time', 'Optimal Duration']

# Important inputs for drones (stronger connections)
important_inputs = {'Farm Area', 'Seasonal Factors', 'Pheromone Levels', 'Time of Day'}

# Create the graph
G = nx.DiGraph()

# Define hidden layers with relevant neuron groups
hidden_layer1 = ['Terrain Analysis', 'Weather Impact', 'Pheromone Processing', 'Timing Optimization']
hidden_layer2 = ['Path Planning', 'Flight Stability', 'Energy Efficiency']

# Add nodes
G.add_nodes_from(inputs)
G.add_nodes_from(hidden_layer1)
G.add_nodes_from(hidden_layer2)
G.add_nodes_from(outputs)

# Define logical connections (Only meaningful ones)
connection_map = {
    'Farm Area': ['Terrain Analysis', 'Path Planning'],
    'Seasonal Factors': ['Timing Optimization', 'Weather Impact'],
    'Pheromone Levels': ['Pheromone Processing', 'Path Planning'],
    'Time of Day': ['Timing Optimization'],
    'Rain': ['Weather Impact', 'Flight Stability'],
    'Wind': ['Weather Impact', 'Flight Stability'],
    'Humidity': ['Weather Impact'],
    'Temperature': ['Weather Impact', 'Energy Efficiency']
}

hidden_connections = {
    'Terrain Analysis': ['Path Planning'],
    'Weather Impact': ['Flight Stability', 'Energy Efficiency'],
    'Pheromone Processing': ['Path Planning'],
    'Timing Optimization': ['Path Planning', 'Optimal Time']
}

output_connections = {
    'Path Planning': ['Optimal Drone Path'],
    'Flight Stability': ['Optimal Drone Path', 'Optimal Duration'],
    'Energy Efficiency': ['Optimal Duration'],
    'Optimal Time': ['Optimal Time']
}

edges, weights, colors = [], [], []

# Input to Hidden Layer 1 (Only relevant ones)
for input_node, hidden_nodes in connection_map.items():
    for hidden_node in hidden_nodes:
        weight = 3 if input_node in important_inputs else 1
        G.add_edge(input_node, hidden_node, weight=weight)
        edges.append((input_node, hidden_node))
        weights.append(weight)
        colors.append('darkgreen' if weight == 3 else 'orange')

# Hidden Layer 1 to Hidden Layer 2
for hidden_node, next_hidden_nodes in hidden_connections.items():
    for next_hidden in next_hidden_nodes:
        G.add_edge(hidden_node, next_hidden, weight=2)
        edges.append((hidden_node, next_hidden))
        weights.append(2)
        colors.append('yellowgreen')

# Hidden Layer 2 to Output
for hidden_node, output_nodes in output_connections.items():
    for output_node in output_nodes:
        G.add_edge(hidden_node, output_node, weight=2)
        edges.append((hidden_node, output_node))
        weights.append(2)
        colors.append('yellowgreen')

# Positioning nodes centrally
layer_dist = 1.5
pos = {}

# Adjust y-positions to bring the output nodes closer
y_positions = np.linspace(-4, 4, len(inputs))
for i, node in enumerate(inputs):
    pos[node] = (-layer_dist * 2, y_positions[i])

# Adjust y-positions of output nodes to bring them closer to the hidden layers
y_positions_outputs = np.linspace(-1.5, 1.5, len(outputs))
for i, node in enumerate(outputs):
    pos[node] = (layer_dist * 2, y_positions_outputs[i])  # Closer to hidden layers

# Hidden layers positioning
pos.update({hidden_layer1[i]: (-layer_dist, i - 1.5) for i in range(len(hidden_layer1))})
pos.update({hidden_layer2[i]: (0, i - 1) for i in range(len(hidden_layer2))})

# Define node colors in a gradient from orange to green
node_order = list(inputs) + hidden_layer1 + hidden_layer2 + outputs
node_colors = [cm.autumn(i / len(node_order)) for i in range(len(node_order))]

# Draw the network with custom font and colors
plt.figure(figsize=(12, 8))

nx.draw(
    G, pos, with_labels=True, node_size=2500, node_color=node_colors, font_size=12, font_weight='bold',
    font_family='Times New Roman', edge_color=colors, width=[w * 2 for w in weights], alpha=0.9, connectionstyle='arc3,rad=0.2'
)

plt.title('Optimized Neural Network for Drone Decision Making', fontweight='bold', fontsize=14, fontfamily='Times New Roman')
plt.axis('off')
plt.show()
