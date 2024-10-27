from itertools import permutations
from math import factorial

MOD = 10**9 + 7  # large prime number for modulo operation

def count_inversions(arr):
    """Helper function to count inversions in an array."""
    inv_count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv_count += 1
    return inv_count

def min_swaps_to_target(perm, target):
    """Calculate the minimum number of adjacent swaps to transform perm into target."""
    # Here, inversion counting is an efficient way to determine adjacent swaps.
    return count_inversions(list(zip(perm, target)))

def compute_sum_of_swaps(N):
    """Compute the sum of minimum swaps for all permutations of length N modulo M."""
    target = list(range(1, (N + 1) // 2 + 1)) + list(range(N, (N + 1) // 2, -1))
    total_swaps = 0
    
    for perm in permutations(range(1, N + 1)):
        total_swaps += min_swaps_to_target(perm, target)
        total_swaps %= MOD  # keep result within MOD
    
    return total_swaps

# Main function to run for a given N
N = int(input())
print(compute_sum_of_swaps(N))