import sys
import time
import psutil

#Penalties
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
    return int(process.memory_info().rss / 1024)


def generate_string(s, idxs):
    for i in idxs:
        s = s[:i+1] + s + s[i+1:]
    return s


def parse_input(file):
    with open(file) as f:
        lines = [l.strip() for l in f if l.strip()]
    
    # Parse first string and its indices
    s1 = lines[0]
    idx1 = []
    i = 1
    while i < len(lines) and lines[i].isdigit():
        idx1.append(int(lines[i]))
        i += 1
    
    # Parse second string and its indices
    s2 = lines[i]
    idx2 = [int(x) for x in lines[i+1:]]
    
    return s1, idx1, s2, idx2


def sequence_alignment(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    
    # Initialize
    for i in range(1,m+1): dp[i][0] = i*DELTA
    for j in range(1,n+1): dp[0][j] = j*DELTA
    
    # Fill DP
    for i in range(1,m+1):
        for j in range(1,n+1):
            dp[i][j] = min(
                dp[i-1][j-1] + ALPHA[s1[i-1]][s2[j-1]],
                dp[i-1][j] + DELTA,
                dp[i][j-1] + DELTA
            )
    
    # Backtrack
    a1, a2 = [], []
    i, j = m, n
    while i > 0 and j > 0:
        if dp[i][j] == dp[i-1][j-1] + ALPHA[s1[i-1]][s2[j-1]]:
            a1.append(s1[i-1])
            a2.append(s2[j-1])
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i][j-1] + DELTA:
            a1.append('_')
            a2.append(s2[j-1])
            j -= 1
        else:
            a1.append(s1[i-1])
            a2.append('_')
            i -= 1
    while i > 0:
        a1.append(s1[i-1])
        a2.append('_')
        i -= 1
    while j > 0:
        a1.append('_')
        a2.append(s2[j-1])
        j -= 1
    return dp[m][n], ''.join(reversed(a1)), ''.join(reversed(a2))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 basic_3.py <input> <output>")
        sys.exit(1)

    s1, idx1, s2, idx2 = parse_input(sys.argv[1])
    str1 = generate_string(s1, idx1)
    str2 = generate_string(s2, idx2)

    mem_before = process_memory()
    time_ms, (cost, a1, a2) = time_wrapper(sequence_alignment, str1, str2)
    mem_after = process_memory()

    with open(sys.argv[2], 'w') as f:
        f.write(f"{cost}\n{a1}\n{a2}\n{time_ms:.4f}\n{mem_after - mem_before}\n")
