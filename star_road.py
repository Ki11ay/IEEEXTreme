from collections import defaultdict

class Graph:
    def __init__(self, n):
        self.adj_list = defaultdict(list)
        self.n = n
        self.route = []
        
    def add_edge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def find_longest_increasing_path(self, start_node, stars):
        path_lengths = {}  # Memoization hashmap to store the longest path from each node

        def dfs(node, current_path):
            if node in path_lengths:
                return path_lengths[node]  # Return the stored path length if available

            max_path = current_path[:]  # Track the longest path from the current node
            for neighbor in self.adj_list[node]:
                if stars[neighbor - 1] > stars[node - 1]:  # Continue only for increasing paths
                    new_path = dfs(neighbor, current_path + [neighbor])
                    if len(new_path) > len(max_path):
                        max_path = new_path
            
            path_lengths[node] = max_path  # Memoize the result
            return max_path

        # Start DFS from the specified start node and find the longest path
        longest_path = dfs(start_node, [start_node])
        self.route = longest_path
        return len(longest_path)

# Main program
n = int(input())
if n == 0:
    print(0)
    exit()

stars = list(map(int, input().split()))
edges = [tuple(map(int, input().split())) for _ in range(n - 1)]

graph = Graph(n)
for u, v in edges:
    graph.add_edge(u, v)

start_node = stars.index(min(stars)) + 1
result = graph.find_longest_increasing_path(start_node, stars)
# print(graph.route)
print(result)