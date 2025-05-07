import sys
import time
import psutil

# Penalties
delta = 30
alpha = {
    'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
    'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
    'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
    'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0},
}


def time_wrapper(func, *args, **kwargs):
    """Measure execution time (ms) of func and return (time_ms, result)."""
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return (end - start) * 1000, result


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed


def generate_string(s, idxs):
    for i in idxs:
        s = s[:i+1] + s + s[i+1:]
    return s


def parse_input(path):
    with open(path) as f:
        lines = [L.strip() for L in f if L.strip()]
    # first base and its indices
    s1 = lines[0]
    idx1 = []
    i = 1
    while i < len(lines) and lines[i].isdigit():
        idx1.append(int(lines[i])); i += 1
    # second base and its indices
    s2 = lines[i]
    idx2 = [int(x) for x in lines[i+1:]]
    return s1, idx1, s2, idx2


def nw_score_row(X, Y):
    """Compute last row of Needleman–Wunsch DP in O(|Y|) space."""
    prev = [j * delta for j in range(len(Y) + 1)]
    for i in range(1, len(X) + 1):
        curr = [i * delta] + [0] * len(Y)
        for j in range(1, len(Y) + 1):
            curr[j] = min(
                prev[j-1] + alpha[X[i-1]][Y[j-1]],
                prev[j] + delta,
                curr[j-1] + delta
            )
        prev = curr
    return prev


def align_core(X, Y):
    """Full DP + backtrack for small cases."""
    m, n = len(X) + 1, len(Y) + 1
    dp = [[0] * n for _ in range(m)]
    for i in range(1, m): dp[i][0] = i * delta
    for j in range(1, n): dp[0][j] = j * delta
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = min(
                dp[i-1][j-1] + alpha[X[i-1]][Y[j-1]],
                dp[i-1][j] + delta,
                dp[i][j-1] + delta
            )
    # backtrack
    i, j = m-1, n-1
    a1, a2 = [], []
    while i > 0 and j > 0:
        if dp[i][j] == dp[i-1][j-1] + alpha[X[i-1]][Y[j-1]]:
            a1.append(X[i-1]); a2.append(Y[j-1]); i -= 1; j -= 1
        elif dp[i][j] == dp[i][j-1] + delta:
            a1.append('_'); a2.append(Y[j-1]); j -= 1
        else:
            a1.append(X[i-1]); a2.append('_'); i -= 1
    while i > 0:
        a1.append(X[i-1]); a2.append('_'); i -= 1
    while j > 0:
        a1.append('_'); a2.append(Y[j-1]); j -= 1
    return ''.join(reversed(a1)), ''.join(reversed(a2))


def hirschberg(X, Y):
    """Hirschberg's algorithm: returns aligned (X', Y')."""
    m, n = len(X), len(Y)
    if m == 0:
        return '_' * n, Y
    if n == 0:
        return X, '_' * m
    if m == 1 or n == 1:
        return align_core(X, Y)
    mid = m // 2
    # score for left half vs Y
    left_score = nw_score_row(X[:mid], Y)
    # score for right half vs Y, reversed
    right_score = nw_score_row(X[mid:][::-1], Y[::-1])[::-1]
    # find split in Y minimizing sum
    split = min(range(n+1), key=lambda j: left_score[j] + right_score[j])
    # recurse
    a1_left, a2_left = hirschberg(X[:mid], Y[:split])
    a1_right, a2_right = hirschberg(X[mid:], Y[split:])
    return a1_left + a1_right, a2_left + a2_right


def compute_cost(a1, a2):
    """Recompute alignment cost from aligned strings."""
    cost = 0
    for x, y in zip(a1, a2):
        if x == '_' or y == '_':
            cost += delta
        else:
            cost += alpha[x][y]
    return cost


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 efficient_3.py <input> <output>")
        sys.exit(1)

    s1, i1, s2, i2 = parse_input(sys.argv[1])
    X = generate_string(s1, i1)
    Y = generate_string(s2, i2)
    
    time_ms, (a1, a2) = time_wrapper(hirschberg, X, Y)
    memory_consumed = process_memory()
    
    # Calculate cost
    cost = compute_cost(a1, a2)
    
    # Write output
    with open(sys.argv[2], 'w') as f:
        f.write(f"{cost}\n{a1}\n{a2}\n{time_ms:.4f}\n{memory_consumed}\n")


