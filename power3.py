def find_power(n):
    x = 0
    if n == 1:
        return 0
    while n > 1:
        if n % 3 != 0:
            return -1
        n = n // 3
        x += 1
    return x
N = int(input())
print(find_power(N))