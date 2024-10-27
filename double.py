def is_it_valid(sequence, N):
    for i in range(1, N + 1):
        if sequence.count(i) != 2:
            return False
        left = sequence.index(i)
        right = len(sequence) - 1 - sequence[::-1].index(i)
        if right - left != i:
            return False
    return True

def genDbSeq(N, sequence=None, used=None, positions=None):
    if sequence is None:
        sequence = []
        used = [0] * (N + 1)
        positions = {}
    if len(sequence) == 2 * N:
        if is_it_valid(sequence, N):
            return sequence
        return None
    current_pos = len(sequence)
    for num in range(1, N + 1):
        if used[num] == 2:
            continue
        if used[num] == 1:
            first_pos = positions[num]
            if current_pos - first_pos != num:
                continue
        sequence.append(num)
        if used[num] == 0:
            positions[num] = current_pos
        used[num] += 1
        result = genDbSeq(N, sequence, used, positions)
        if result:
            return result
        sequence.pop()
        if used[num] == 1:
            positions.pop(num)
        used[num] -= 1
    return None

def dbsequ():
    try:
        T = int(input().strip()) 
        if T < 1: 
            return
        for _ in range(T):
            try:
                N = int(input().strip()) 
                if N < 1: 
                    print(-1)
                    continue
                    
                result = genDbSeq(N)
                if result is None:
                    print(-1)
                else:
                    print(*result)
            except ValueError:
                print(-1)
            except EOFError:
                break
    except (ValueError, EOFError):
        return
if __name__ == "__main__":
    dbsequ()