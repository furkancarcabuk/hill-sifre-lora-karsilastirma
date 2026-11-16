"""LoRa hava kalma süresi, etiket (doğrulama etiketi) ek yükü ve %1 görev döngüsü maskesi.
Kullanılan formül: Augustin ve ark. (2016), Sensors 16(9):1466.
Varsayımlar: BW=125 kHz, CR=4/5, 8 sembol ön başlık, açık başlık, CRC açık.
Çalıştırma: python3 lora_airtime.py
"""
import math

def hava_kalma_ms(L, SF, BW=125000, CR=1, npre=8, IH=0, CRC=1):
    DE = 1 if SF >= 11 else 0
    ts = 2 ** SF / BW
    n = 8 + max(math.ceil((8 * L - 4 * SF + 28 + 16 * CRC - 20 * IH) / (4 * (SF - 2 * DE))) * (CR + 4), 0)
    return (npre + 4.25 + n) * ts * 1000  # ms

if __name__ == "__main__":
    SFLER, YUKLER, PERIYOTLAR = (7, 9, 11, 12), (16, 32, 64, 128), (60, 300, 900, 3600)
    satirlar = []
    print("SF  yük  L_etiketsiz  t_etiketsiz(ms)  L_AEAD  t_AEAD(ms)  etiket artışı(%)  etiketsiz kazanç(%)")
    for sf in SFLER:
        for yuk in YUKLER:
            tb = hava_kalma_ms(8 + yuk, sf)        # 8 B başlık + yük
            ta = hava_kalma_ms(8 + yuk + 16, sf)   # + 16 B etiket
            satirlar.append((sf, yuk, tb, ta))
            print(sf, yuk, 8 + yuk, round(tb, 1), 24 + yuk, round(ta, 1),
                  round((ta / tb - 1) * 100, 1), round((1 - tb / ta) * 100, 1))
    for ad, idx in (("AEAD", 3), ("etiketsiz", 2)):
        maske = sum(1 for r in satirlar for T in PERIYOTLAR if r[idx] / 1000 > 0.01 * T)
        print(f"{ad}: uygulanamaz (maskeli) hücre sayısı = {maske} / 64")
