MODULO = 998244353
from itertools import permutations
 
def count_valid_permutations(N, C, R, B):
    used = [False] * (2 * N + 1)
    unknown_indices = [i for i in range(2 * N) if C[i] == -1]
    known_values = {i: C[i] for i in range(2 * N) if C[i] != -1}
    remaining_values = [i for i in range(1, 2 * N + 1) if i not in known_values.values()]
    def backtrack(index, current_permutation):
        if index == len(unknown_indices):
            A = C[:]
            for idx, val in zip(unknown_indices, current_permutation):
                A[idx] = val
            for i in range(N):
                a1, a2 = A[2 * i], A[2 * i + 1]
                if (R[i] == 0 and B[i] != min(a1, a2)) or (R[i] == 1 and B[i] != max(a1, a2)):
                    return 0
            return 1
 
        count = 0
        for i in range(len(remaining_values)):
            if not used[i]:
                used[i] = True
                current_permutation[index] = remaining_values[i]
                count = (count + backtrack(index + 1, current_permutation)) % MODULO
                used[i] = False
        return count
    current_permutation = [-1] * len(unknown_indices)
    return backtrack(0, current_permutation)

N = int(input())
C = list(map(int, input().split()))
R = list(map(int, input().split()))
B = list(map(int, input().split()))
print(count_valid_permutations(N, C, R, B))