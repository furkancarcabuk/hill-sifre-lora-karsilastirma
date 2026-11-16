# Ön çalışma kodları: Hill tabanlı şifreleme ve hafif AEAD karşılaştırması

TÜBİTAK 2209-A 2026 başvurusu (Furkan Çarçabuk, İTÜ Siber Güvenlik MYO) kapsamında yapılan ön çalışmaların kodudur.
Proje, pille çalışan Cortex-M0+ / LoRa sensör düğümünde Hill tabanlı matris şifrelerini standart hafif AEAD yöntemleriyle
(AES-128-CCM, Ascon-AEAD128) ve şifresiz referansla güvenlik ve enerji açısından karşılaştırır. Proje boyunca üretilecek araç ve
ölçüm veri seti bu depoya eklenecektir.

| Dosya | Ne yapar |
|---|---|
| `lora_airtime.py` | LoRa hava kalma süresini (Augustin ve ark., 2016) hesaplar; 16 baytlık doğrulama etiketinin getirdiği artışı ve %1 görev döngüsü nedeniyle uygulanamayan (maskeli) hücreleri verir. |
| `hill_kpa.py` | Klasik Hill şifresine (4×4, mod 251) bilinen düz metin saldırısını 1000 rastgele anahtarla dener. |
| `hill_mohan_varyanti.py` | Mohan ve ark. (2016) Hill varyantını uygular, makaledeki "FBS100" örneğini yeniden üretir ve aynı blok indeksindeki bilinen çiftlerle anahtar kurtarma ön denemesini yapar. |

## Çalıştırma
Yalnızca Python 3.8+ gerekir, ek paket yok:
```
python3 lora_airtime.py
python3 hill_kpa.py
python3 hill_mohan_varyanti.py
```
Rastgele sayı tohumu 2026'dır; sonuçlar yeniden üretilebilir.

## Beklenen çıktılar
- `lora_airtime.py`: AEAD için 12/64, etiketsiz paket için 11/64 hücre maskeli.
- `hill_kpa.py`: `{4: 998, 5: 1000, 6: 1000}`.
- `hill_mohan_varyanti.py`: `P44VEP` ve `968/1000`.

## Sınırlılıklar
Bunlar ön çalışmadır: hava kalma süresi yalnızca formülden hesaplanır, ölçüm değildir. Varyant denemesi küçük ölçeklidir ve kesin bir
güvenlik sonucu değildir; projede standart saldırı protokolüyle sınanacaktır.

## Kaynaklar
- Augustin, A., Yi, J., Clausen, T., & Townsley, W. M. (2016). A study of LoRa. Sensors, 16(9), 1466.
- Mohan, M., Kavithadevi, M. K., & Jeevan Prakash, V. (2016). Improved classical cipher for healthcare applications. Procedia Computer Science, 93, 742–750.
