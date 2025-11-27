import random

def sample_b():
    return 0 if random.random() < 0.1 else 1

def sample_g():
    return 0 if random.random() < 0.05 else 1

def sample_r(b):
    if b == 0:
        return 0
    return 0 if random.random() < 0.1 else 1

def sample_i(b):
    if b == 0:
        return 0
    return 0 if random.random() < 0.05 else 1

def sample_s(i, g):
    if i == 1 and g == 1:
        return 0 if random.random() < 0.01 else 1
    return 0

def sample_m(s):
    if s == 1:
        return 0 if random.random() < 0.01 else 1
    return 0

def generate(n):
    data = []
    for _ in range(n):
        B = sample_b()
        G = sample_g()
        R = sample_r(B)
        I = sample_i(B)
        S = sample_s(I, G)
        M = sample_m(S)
        data.append((B, R, I, G, S, M))
    return data

def prob_b_given_r_g_not_s(data):
    total = 0
    count = 0
    for B, R, I, G, S, M in data:
        if R == 1 and G == 1 and S == 0:
            total += 1
            if B == 1:
                count += 1
    return count / total if total else 0.0

def prob_s_given_r_i_g(data):
    total = 0
    count = 0
    for B, R, I, G, S, M in data:
        if R == 1 and I == 1 and G == 1:
            total += 1
            if S == 1:
                count += 1
    return count / total if total else 0.0

def prob_s_given_not_r_i_g(data):
    total = 0
    count = 0
    for B, R, I, G, S, M in data:
        if R == 0 and I == 1 and G == 1:
            total += 1
            if S == 1:
                count += 1
    return count / total if total else 0.0

N = 100000
data = generate(N)

print("P(B | R, G, ¬S) =", prob_b_given_r_g_not_s(data))
print("P(S | R, I, G) =", prob_s_given_r_i_g(data))
print("P(S | ¬R, I, G) =", prob_s_given_not_r_i_g(data))
