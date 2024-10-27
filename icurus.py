def check_cycle(adj, start, sequence):
    n = len(adj)
    seq_len = len(sequence)
    visited = set()
    curr = start
    pos = 0
    state_history = []
    
    while True:
        state = (curr, pos)
        if state in visited:
            cycle_start = state_history.index(state)
            cycle_nodes = set(state[0] for state in state_history[cycle_start:])
            return True, cycle_nodes
            
        visited.add(state)
        state_history.append(state)
        move = sequence[pos]
        if move == 'L':
            next_node = adj[curr][0] 
        elif move == 'R':
            next_node = adj[curr][1] 
        else:
            next_node = -1
            for parent, (left, right) in enumerate(adj):
                if left == curr or right == curr:
                    next_node = parent
                    break
        if next_node == -1 or next_node >= n:
            return False, set()
            
        curr = next_node
        pos = (pos + 1) % seq_len

def solve(sequence):
    seq_len = len(sequence)
    max_nodes = min(2 * seq_len, 2000)  
    
    for n in range(2, max_nodes + 1):
        for start in range(n):
            for target in range(n):
                if start == target:
                    continue
                
                adj = [(0, 0) for _ in range(n)]
                edges_used = 0
                
                for i in range(n-1):
                    adj[i] = (i+1, 0)
                    edges_used += 1
                cycle_exists, cycle_nodes = check_cycle(adj, start, sequence)
                
                if cycle_exists and target not in cycle_nodes:
                    return n, start, target, adj
    
    return (-1,)

def main():
    sequence = input().strip()
    result = solve(sequence)
    if len(result) == 1:
        print(-1)
        return
    n, start, target, adj = result
    print(n, start, target)
    for left, right in adj:
        print(left, right)

if __name__ == "__main__":
    main()