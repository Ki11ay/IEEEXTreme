import bisect

N, K, L = map(int, input().split())

def union(N, K, L):
    events = []
    for i in range(N):
        x_start = i * K - L
        x_end = i * K + L
        y_start = i * K - L
        y_end = i * K + L
        events.append((x_start, y_start, y_end, 0))  # Start of interval
        events.append((x_end, y_start, y_end, 1))    # End of interval

    # Sort by x coordinate, then by type to prioritize adding over removing
    events.sort()

    active_intervals = []
    total_area = 0
    prev_x = events[0][0]

    for x, y_start, y_end, typ in events:
        delta_x = x - prev_x
        if delta_x > 0 and active_intervals:
            # Calculate the union of all intervals in active_intervals
            total_y_length = 0
            curr_start, curr_end = active_intervals[0]
            for ys, ye in active_intervals[1:]:
                if ys <= curr_end:
                    curr_end = max(curr_end, ye)
                else:
                    total_y_length += curr_end - curr_start
                    curr_start, curr_end = ys, ye
            total_y_length += curr_end - curr_start
            total_area += delta_x * total_y_length

        if typ == 0:  # Add interval
            bisect.insort(active_intervals, (y_start, y_end))
        else:  # Remove interval
            idx = bisect.bisect_left(active_intervals, (y_start, y_end))
            if idx < len(active_intervals) and active_intervals[idx] == (y_start, y_end):
                active_intervals.pop(idx)

        prev_x = x

    return total_area

print(union(N, K, L))