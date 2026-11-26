# Modelis no sistēmas datiem: uzbrukumu atpazīšana tīkla plūsmās

> **Patstāvīgais darbs**  
> Projekts no tīkla plūsmu datiem (**CIC-IDS2017**) izveido modeli, kas prognozē, vai tīkla plūsma ir **normāla** vai ir **uzbrukums**. Modeļa precizitāte tiek salīdzināta ar bāzes līniju (vienmēr nosaukt biežāko atbildi).

---

## Projekta faili

* **`dati/CICIDS2017.csv`** — neapstrādātie dati tieši tādi, kā lejupielādēti (oriģināls netiek mainīts).
* **`dati/AVOTS.txt`** — datu avots, lejupielādes datums un licence.
* **`tirisana.py`** — nolasa neapstrādātos datus, iztīra tos un saglabā failā `tirs.csv`.
* **`tirs.csv`** — sakārtotie un modelim sagatavotie dati.
* **`modelis.py`** — sadala datus treniņa un testa daļā, apmāca lēmumu koku, izvada precizitāti un bāzes līniju.
* **`rezultati.md`** — rezultātu skaidrojums, pieņemtie lēmumi un pašvērtējums.

---

## Priekšnosacījumi

Lai darbinātu projektu, nepieciešams:
* **Python 3.10** vai jaunāka versija
* Bibliotēkas: `pandas`, `numpy`, `scikit-learn`

---

## Kā palaist projektu

1. **Instalē nepieciešamās bibliotēkas:**
   ```bash
   pip install pandas numpy scikit-learn
   ```

2. **Palaid skriptus šādā secībā:**
   ```bash
   python tirisana.py
   python modelis.py
   ```
