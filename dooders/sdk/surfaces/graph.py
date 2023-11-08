
import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        self._graph = self.create_grid_graph(height, width)
        self.pos = self.get_pos(height, width)

    def create_grid_graph(self):
        G = nx.grid_2d_graph(self.height, self.width)
        
        # Wrap around the edges
        for x in range(self.height):
            G.add_edge((x, 0), (x, self.width - 1))
        for y in range(self.width):
            G.add_edge((0, y), (self.height - 1, y))

        # Label nodes with integers instead of (x, y) coordinates
        relabel_dict = {(x, y): y*dim + x for x, y in G.nodes()}
        G = nx.relabel_nodes(G, relabel_dict)

        return G

    def coordinate_to_node_label(x, y, dim):
        return y * dim + x

    def get_neighbors(self, node_number):
        neighbor_nodes = list(self._graph.neighbors(node_number))
        print(f"Neighbors of node {node}: {neighbor_nodes}")

# Draw the graph with updated position mapping
dim = 10
pos = {(x + y*10): (x, dim - 1 - y) for x in range(dim) for y in range(dim)}
nx.draw(G, pos, with_labels=True, node_size=400, node_color="lightblue")
plt.show()