# CMPE 411 — SmartCart gözden geçirilmiş sürüm

Bu proje dersin **#35 Shopping Cart and Discount Engine** konusudur. Lab 1 klasörüne ekleme; **yeni, ayrı bir GitHub deposu** kullan.

## Mac'te sırayla

1. ZIP'i aç; içinden çıkan `CMPE411_SmartCart_Reviewed` klasörünü kullan (eski Starter yerine).
2. Terminal'de klasöre gir (Terminal'e `cd ` yazıp klasörü sürükleyebilirsin).
3. Komutlar:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pytest -q
```

4. Yeşil sonuç geldiğinde ekran görüntüsü al. Uyarı görünürse, tüm testler geçmişse bir warning tek başına test hatası değildir.
5. Sonra GitHub Desktop'ta **File > Add Local Repository**, bu klasörü seç. "not a repository" diyorsa **Create a Repository here** de. `.gitignore` doğru: `.venv` GitHub'a gitmez. Commit ve Publish işlemine sonra geç.

## Ne işe yarıyor?

- `docs/requirements.md` = kendi yazılı kurallarımız, test oracle (asıl doğruluk kaynağı).
- `cart.py` = para hesabı ve girdi sınırları.
- `api.py` = aynı hesabın `/checkout` HTTP arayüzü.
- `tests/` = unit, API, negatif, sınır ve metamorphic testler.
- `tools/check_mutations.py` = ayrı kopyalarda seçilmiş 9 mutantın yakalanıp yakalanmadığını ölçer.
- `docs/LAB3_DEMO_AND_ORAL_QA.md` = hocanın olası sözlü soruları ve açıklamaları.
- `docs/AI_EVALUATION_PLAN.md` = AI-generated test adaylarını dürüstçe incelemek için yapılacak iş.

## Kritik tarihler

- **20 Kasım:** Lab 3 ilerleme kontrolü, en az 10 çalışan otomatik test. Katılamayacaksan hocaya GitHub bağlantısıyla uzaktan değerlendirme sor.
- **11 Aralık 23.59:** Final proje — repo linki + şablona uygun **8–12 sayfa PDF rapor**. AI değerlendirme çalışması ve bu rapor henüz bitmiş değil.

## Öğrenmen gereken üç cümle

- **BVA:** SAVE10 at 499.99 TL is not eligible, at 500.00 TL it is eligible.
- **Decision table:** Membership and SAVE10 discounts do not stack; the larger eligible rate wins.
- **Coverage vs mutation:** Coverage tells which code executed; selected mutation tests ask whether a deliberate change is detected.
