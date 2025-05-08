import sys
import time
import psutil

# Penalties
DELTA = 30
ALPHA = {
    'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
    'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
    'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
    'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0},
}


def time_wrapper(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return (end_time - start_time) * 1000, result


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed


def generate_string(s, idxs):
    for i in idxs:
        s = s[:i+1] + s + s[i+1:]
    return s


def parse_input(file):
    with open(file) as f:
        lines = [l.strip() for l in f if l.strip()]
    s1 = lines[0]
    idx1 = []
    i = 1
    while i < len(lines) and lines[i].isdigit():
        idx1.append(int(lines[i])); i += 1
    s2 = lines[i]
    idx2 = [int(x) for x in lines[i+1:]]
    return s1, idx1, s2, idx2


def nw_score_row(X, Y):
    prev = [j * DELTA for j in range(len(Y) + 1)]
    for i in range(1, len(X) + 1):
        curr = [i * DELTA] + [0] * len(Y)
        for j in range(1, len(Y) + 1):
            curr[j] = min(
                prev[j-1] + ALPHA[X[i-1]][Y[j-1]],
                prev[j] + DELTA,
                curr[j-1] + DELTA
            )
        prev = curr
    return prev


def align_core(X, Y):
    m, n = len(X) + 1, len(Y) + 1
    dp = [[0] * n for _ in range(m)]
    for i in range(1, m): dp[i][0] = i * DELTA
    for j in range(1, n): dp[0][j] = j * DELTA
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = min(
                dp[i-1][j-1] + ALPHA[X[i-1]][Y[j-1]],
                dp[i-1][j] + DELTA,
                dp[i][j-1] + DELTA
            )
    i, j = m-1, n-1
    a1, a2 = [], []
    while i>0 and j>0:
        if dp[i][j] == dp[i-1][j-1] + ALPHA[X[i-1]][Y[j-1]]:
            a1.append(X[i-1]); a2.append(Y[j-1]); i-=1; j-=1
        elif dp[i][j] == dp[i][j-1] + DELTA:
            a1.append('_'); a2.append(Y[j-1]); j-=1
        else:
            a1.append(X[i-1]); a2.append('_'); i-=1
    while i>0: a1.append(X[i-1]); a2.append('_'); i-=1
    while j>0: a1.append('_'); a2.append(Y[j-1]); j-=1
    return ''.join(reversed(a1)), ''.join(reversed(a2))


def sequence_alignment(s1, s2):
    # Hirschberg returns aligned strings
    def hirschberg(X, Y):
        if len(X) == 0: return '_' * len(Y), Y
        if len(Y) == 0: return X, '_' * len(X)
        if len(X) == 1 or len(Y) == 1:
            return align_core(X, Y)
        mid = len(X) // 2
        left = nw_score_row(X[:mid], Y)
        right = nw_score_row(X[mid:][::-1], Y[::-1])[::-1]
        split = min(range(len(Y)+1), key=lambda j: left[j] + right[j])
        a1L, a2L = hirschberg(X[:mid], Y[:split])
        a1R, a2R = hirschberg(X[mid:], Y[split:])
        return a1L + a1R, a2L + a2R

    a1, a2 = hirschberg(s1, s2)
    # recompute cost exactly
    cost = 0
    for x,y in zip(a1, a2):
        cost += DELTA if x=='_' or y=='_' else ALPHA[x][y]
    return cost, a1, a2


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 efficient_3.py <input> <output>")
        sys.exit(1)
    s1, idx1, s2, idx2 = parse_input(sys.argv[1])
    str1 = generate_string(s1, idx1)
    str2 = generate_string(s2, idx2)

    time_ms, (cost, a1, a2) = time_wrapper(sequence_alignment, str1, str2)
    memory = process_memory()

    with open(sys.argv[2], 'w') as f:
        f.write(f"{cost}\n{a1}\n{a2}\n{time_ms:.6f}\n{memory}\n")


