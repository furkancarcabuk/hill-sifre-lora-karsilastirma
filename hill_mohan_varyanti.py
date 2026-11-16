"""Mohan, Kavithadevi ve Jeevan Prakash (2016) Hill varyantı: C' = K1·P + K*, K* = satırtoplam(K2^i) mod 37.
1) Makaledeki "FBS100" örneğini yeniden üretir (beklenen: P44VEP).
2) Aynı blok indeksindeki bilinen çiftlerin farkı alınınca ofsetin yok olduğunu ve K1'in
   klasik Hill gibi kurtarılabildiğini küçük bir denemeyle gösterir (ön işaret, kesin sonuç değil).
Çalıştırma: python3 hill_mohan_varyanti.py
"""
import random
m = 37
AL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789."

def carp(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) % m for j in range(len(B[0]))] for i in range(len(A))]

def us(A, e):
    n = len(A); R = [[int(i == j) for j in range(n)] for i in range(n)]
    for _ in range(e): R = carp(R, A)
    return R

def ofset(K2, i):           # K*: K2^i matrisinin satır toplamları
    return [sum(r) % m for r in us(K2, i)]

def sifrele(K1, K2, P, i):  # P: blok, i: blok indeksi (1'den başlar)
    c = [sum(K1[r][j] * P[j] for j in range(len(P))) % m for r in range(len(P))]
    return [(a + b) % m for a, b in zip(c, ofset(K2, i))]

def ters(A):
    n = len(A); M = [r[:] + [int(i == j) for j in range(n)] for i, r in enumerate(A)]
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] % m), None)
        if piv is None: return None
        M[c], M[piv] = M[piv], M[c]
        iv = pow(M[c][c], -1, m); M[c] = [x * iv % m for x in M[c]]
        for r in range(n):
            if r != c and M[r][c]:
                f = M[r][c]; M[r] = [(x - f * y) % m for x, y in zip(M[r], M[c])]
    return [r[n:] for r in M]

def rastgele_tersinir(n):
    while True:
        A = [[random.randrange(m) for _ in range(n)] for _ in range(n)]
        if ters(A): return A

if __name__ == "__main__":
    # 1) makale örneği
    K1 = [[1, 5, 2], [7, 3, 9], [12, 5, 7]]; K2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    cikti = ""
    for i, blok in enumerate(["FBS", "100"], 1):
        cikti += "".join(AL[x] for x in sifrele(K1, K2, [AL.index(c) for c in blok], i))
    print("Makale örneği ->", cikti, "(makalede: P44VEP)")
    # 2) aynı indeksli bilinen çiftlerle anahtar kurtarma
    random.seed(2026)
    n, deneme, kurtarilan, gecersiz = 3, 1000, 0, 0
    for _ in range(deneme):
        K1 = rastgele_tersinir(n); K2 = [[random.randrange(m) for _ in range(n)] for _ in range(n)]
        Ps = [[random.randrange(m) for _ in range(n)] for _ in range(n + 1)]
        Cs = [sifrele(K1, K2, P, 1) for P in Ps]          # hepsi 1. blok indeksinde
        dP = [[(Ps[j + 1][r] - Ps[0][r]) % m for j in range(n)] for r in range(n)]
        dC = [[(Cs[j + 1][r] - Cs[0][r]) % m for j in range(n)] for r in range(n)]
        iv = ters(dP)
        if iv is None: gecersiz += 1; continue
        kurtarilan += (carp(dC, iv) == K1)
    print(f"K1 kurtarma: {kurtarilan}/{deneme} (fark vektörleri doğrusal bağımlı olan {gecersiz} deneme geçersiz)")
