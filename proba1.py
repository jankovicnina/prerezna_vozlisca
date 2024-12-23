import sys

class Graph:
    def __init__(self):
        """
        Initializes the graph with a dictionary for vertices.
        """
        self.vertices = {}

    def add_vertex(self, label):
        """
        Adds a vertex and returns its label.
        """
        if label not in self.vertices:
            self.vertices[label] = Vertex(label)
        return self.vertices[label]

class Vertex:
    def __init__(self, label):
        """
        Initializes a vertex with its label, neighbors, and attributes for articulation point calculation.
        """
        self.label = label
        self.neighbors = []
        self.parent = None 
        self.visited = False
        self.pre = 0  # Discovery time
        self.low = sys.maxsize  # Lowest point reachable
        self.articulation = False  # Indicates if it's an articulation point
        self.children = 0

    def add_neighbor(self, neighbor):
        """
        Adds a neighbor to the list of neighbors.
        """
        self.neighbors.append(neighbor)

def iterative_dfs(graph, start_label):
    """
    Performs an iterative DFS on the graph to compute 'pre', 'low' values and identify articulation points.
    """
    time = -1
    start = graph.vertices[start_label]
    stack = [(start, "enter")]

    while stack:
        vertex, state = stack.pop()

        if state == "enter":
            if not vertex.visited:
                vertex.visited = True
                time += 1
                vertex.pre = vertex.low = time
                stack.append((vertex, "exit"))

                for neighbor in vertex.neighbors:
                    if not neighbor.visited:
                        neighbor.parent = vertex
                        stack.append((neighbor, "enter"))
                    elif neighbor != vertex.parent:
                        vertex.low = min(vertex.low, neighbor.pre)

        elif state == "exit":
            time += 1
            if vertex.parent:
                vertex.parent.low = min(vertex.parent.low, vertex.low)
                vertex.parent.children += 1

                # vertex is not the root
                if vertex.low >= vertex.parent.pre and vertex.parent.parent is not None:
                    vertex.parent.articulation = True
            
            # vertex is the root
            if vertex.parent is None and vertex.children > 1:
                vertex.articulation = True

def solve():
    """
    Reads input data, builds the graph, and performs iterative DFS.
    Returns the graph with identified articulation points.
    """
    data = sys.stdin.read().strip().split("\n")

    # number of vertices (n) and edges (m)
    n, m = map(int, data[0].split())

    G = Graph()

    for i in range(n):
        G.add_vertex(i)

    for i in range(1, m + 1):
        u, v = map(int, data[i].split())
        G.vertices[u].add_neighbor(G.vertices[v])
        G.vertices[v].add_neighbor(G.vertices[u])

    iterative_dfs(G, 0)
    return G

if __name__ == "__main__":
    G = solve()
    result = [v.label for v in G.vertices.values() if v.articulation]    
    result.sort()

    if result:
        print(" ".join(map(str, result)))
    else:
        print(-1)