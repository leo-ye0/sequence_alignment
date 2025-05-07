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