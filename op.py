def solve_steiner_tree(N, weights, edges):
    graph = [[] for _ in range(N + 1)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    MOD = 10**9 + 7
    
    def find_minimum_steiner_tree(terminals):
        if not terminals:
            return 0
        visited = set()
        included_weights = set()
        def dfs(node, terminals_set):
            if node in visited:
                return False
            visited.add(node)
            should_include = node in terminals_set
            for neighbor in graph[node]:
                if dfs(neighbor, terminals_set):
                    should_include = True
            if should_include:
                included_weights.add(node)
            return should_include
        start = min(terminals)
        dfs(start, set(terminals))
        return sum(weights[i-1] for i in included_weights)

    result = []
    for k in range(1, N + 1):
        total = 0
        for i in range(1, N + 1):
            visited = set()
            current_subset = set()
            def dfs_size_k(node, remaining):
                if remaining < 0:
                    return
                visited.add(node)
                current_subset.add(node)
                for next_node in graph[node]:
                    if next_node not in visited:
                        dfs_size_k(next_node, remaining - 1)
            
            dfs_size_k(i, k - 1)
            
            if len(current_subset) >= k:
                from itertools import combinations
                for subset in combinations(current_subset, k):
                    total = (total + find_minimum_steiner_tree(subset)) % MOD
        
        result.append(total)
    
    return result
N = int(input())
weights = list(map(int, input().split()))
edges = [tuple(map(int, input().split())) for _ in range(N - 1)]

result = solve_steiner_tree(N, weights, edges)
for res in result:
    print(res)