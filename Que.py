from typing import List, Tuple
import sys
class ArrayOperations:
    def __init__(self, n: int, permutation: List[int]):
        self.n = n
        # Convert 1-based permutation to 0-based indexing
        self.permutation = [p - 1 for p in permutation]
        self.array = [0] * n
        
    def update_regular(self, l: int, r: int, c: int) -> None:
        for i in range(l - 1, r):
            self.array[i] += c
            
    def update_permuted(self, l: int, r: int, c: int) -> None:
        for i in range(l - 1, r):
            self.array[self.permutation[i]] += c
            
    def query_regular(self, l: int, r: int) -> int:
        return sum(self.array[l-1:r])
        
    def query_permuted(self, l: int, r: int) -> int:
        total = 0
        for i in range(l - 1, r):
            total += self.array[self.permutation[i]]
        return total

def process_operations() -> List[int]:
    # Read input
    N, Q = map(int, input().split())
    permutation = list(map(int, input().split()))
    
    # Initialize array operations
    arr_ops = ArrayOperations(N, permutation)
    results = []
    
    # Process Q operations
    for _ in range(Q):
        operation = list(map(int, input().split()))
        op_type = operation[0]
        
        if op_type <= 1:  # Updates
            l, r, c = operation[1:]
            if op_type == 0:
                arr_ops.update_regular(l, r, c)
            else:
                arr_ops.update_permuted(l, r, c)
        else:  # Queries
            l, r = operation[1:]
            if op_type == 2:
                results.append(arr_ops.query_regular(l, r))
            else:
                results.append(arr_ops.query_permuted(l, r))
                
    return results

def main():
    try:
        results = process_operations()
        for result in results:
            print(result)
    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()