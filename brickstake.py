def get_optimal_strategy(ar, ab, br, bb, player_a_role):
    state = (ar, ab, br, bb, player_a_role)
    if ar == 0 or ab == 0:
        return 0.0
    if br == 0 or bb == 0:
        return 1.0
        
    if state in memo:
        return memo[state]
    prob = 0.0
    if player_a_role:
        p1 = (br / (br + bb)) * get_optimal_strategy(ar, ab, br - 1, bb, False) + \
             (bb / (br + bb)) * get_optimal_strategy(ar - 1, ab, br, bb, False)
        p2 = (br / (br + bb)) * get_optimal_strategy(ar, ab - 1, br, bb, False) + \
             (bb / (br + bb)) * get_optimal_strategy(ar, ab, br, bb - 1, False)
        prob = max(p1, p2)
    else:
        p1 = (ar / (ar + ab)) * get_optimal_strategy(ar - 1, ab, br, bb, True) + \
             (ab / (ar + ab)) * get_optimal_strategy(ar, ab, br - 1, bb, True)
        p2 = (ar / (ar + ab)) * get_optimal_strategy(ar, ab - 1, br, bb, True) + \
             (ab / (ar + ab)) * get_optimal_strategy(ar, ab, br, bb - 1, True)
        prob = min(p1, p2)
    memo[state] = prob
    return prob

def solve(ar, ab, br, bb):
    global memo
    memo = {}
    return get_optimal_strategy(ar, ab, br, bb, True)

r1, b1, r2, b2 = map(int, input().split())
result = solve(r1, b1, r2, b2)
print(result)