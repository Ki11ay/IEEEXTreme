from itertools import product

N, M = map(int, input().split())

if M == 0:
    print( "infinity")
    exit(0)

lows = []
highs = []
indices = []
adjusted_indices = []

MOD = 998244353

for _ in range(M):
    try:
        line = list(map(int, input().split()))
        if len(line) < 3:
            raise ValueError()
        lows.append(line[0])
        highs.append(line[1])
        indices.append(line[3:])
    except ValueError as e:
        exit(0)

for i in indices:
    adjusted_constraints = []

    for j in i:
        adjusted_constraints.append(j - 1)

    adjusted_indices.append(adjusted_constraints)


def satisfies_constraints(assignment):
    for i in range(len(lows)):
        low = lows[i]
        high = highs[i]
        constraint_indices = adjusted_indices[i]

        subset_sum = sum(assignment[idx] for idx in constraint_indices)

        if subset_sum < low or subset_sum > high:
            return False
    return True


def count_valid_assignments(N, lows, highs, indices):

    c = 0
    
    MAX_VALUE = max(highs)
    
    for x in product(range(MAX_VALUE + 1), repeat=N):
        if satisfies_constraints(x):
            c = (c + 1) % MOD 
    return c

print(count_valid_assignments(N, lows, highs, indices))

