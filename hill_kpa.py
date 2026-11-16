"""Klasik Hill şifresine bilinen düz metin saldırısı (ön deneme).
4x4 anahtar, mod 251, 1000 rastgele tersinir anahtar; saldırgan m=4,5,6 (açık, şifreli) blok çifti bilir.
Çalıştırma: python3 hill_kpa.py
"""
import random, itertools
p = 251

def ters(M):
    n = len(M); A = [r[:] + [int(i == j) for j in range(n)] for i, r in enumerate(M)]
    for c in range(n):
        piv = next((r for r in range(c, n) if A[r][c] % p), None)
        if piv is None: return None
        A[c], A[piv] = A[piv], A[c]
        iv = pow(A[c][c], -1, p); A[c] = [x * iv % p for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] % p:
                f = A[r][c]; A[r] = [(x - f * y) % p for x, y in zip(A[r], A[c])]
    return [r[n:] for r in A]

def carp(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) % p for j in range(len(B[0]))] for i in range(len(A))]

random.seed(2026)
n, deneme = 4, 1000
basari = {4: 0, 5: 0, 6: 0}
for _ in range(deneme):
    while True:
        K = [[random.randrange(p) for _ in range(n)] for _ in range(n)]
        if ters(K): break
    P = [[random.randrange(p) for _ in range(n)] for _ in range(8)]
    C = [[sum(K[i][j] * pb[j] for j in range(n)) % p for i in range(n)] for pb in P]
    for m in (4, 5, 6):
        got = None
        for idx in itertools.combinations(range(m), n):
            PsT = [[P[i][j] for i in idx] for j in range(n)]
            iv = ters(PsT)
            if iv:
                CsT = [[C[idx[k]][j] for k in range(n)] for j in range(n)]
                got = carp(CsT, iv); break
        if got == K: basari[m] += 1
print("Anahtar kurtarma (1000 anahtardan):", basari)
