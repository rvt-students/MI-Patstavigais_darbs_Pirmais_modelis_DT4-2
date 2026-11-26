"""Datu sagatavošana: nolasa dati/CICIDS2017.csv un saglabā sakārtotu failu tirs.csv.
Oriģinālo failu nemaina - tas tiek tikai nolasīts."""

from pathlib import Path

import numpy as np
import pandas as pd

MAPE = Path(__file__).parent
SAKUMA_FAILS = MAPE / "dati" / "CICIDS2017.csv"
REZULTATA_FAILS = MAPE / "tirs.csv"

dati = pd.read_csv(SAKUMA_FAILS, low_memory=False)
rindas_sakuma = len(dati)
print(f"Rindu skaits sākumā: {rindas_sakuma}")

# 1. solis: izmetam kolonnu 'Fwd Header Length.1', jo tā ir precīza kolonnas 'Fwd Header Length' kopija
#    (šajā failā abas kolonnas ir identiskas, tāpēc otra neko jaunu modelim nedod).
assert dati["Fwd Header Length"].equals(dati["Fwd Header Length.1"])
dati = dati.drop(columns=["Fwd Header Length.1"])

# 2. solis: izmetam kolonnas, kurās visās rindās ir viena un tā pati vērtība (piem., 'Bwd PSH Flags'),
#    jo šajos tīkla datos tās vienmēr ir 0 un modelis no tām neko nevar iemācīties.
konstantas = [k for k in dati.columns if dati[k].nunique() <= 1]
print(f"Izmestas konstantās kolonnas: {konstantas}")
dati = dati.drop(columns=konstantas)

# 3. solis: bezgalīgās vērtības (inf) pārvēršam par trūkstošām, jo 'Flow Bytes/s' un 'Flow Packets/s'
#    ir dalījums ar plūsmas ilgumu, un plūsmām ar ilgumu 0 sanāk dalīšana ar nulli.
skaitliskas = dati.select_dtypes(include="number").columns
dati[skaitliskas] = dati[skaitliskas].replace([np.inf, -np.inf], np.nan)

# 4. solis: izmetam rindas ar trūkstošām vērtībām (kopā mazāk nekā 0,2 % datu),
#    jo tās ir mērījumu kļūdas un tik maz rindu nav vērts aizpildīt ar izdomātām vērtībām.
dati = dati.dropna()

# 5. solis: izmetam rindas ar negatīviem laika/skaita rādītājiem (piem., 'Flow IAT Min'),
#    jo laika starpība starp paketēm nevar būt negatīva - tā ir kļūda plūsmu uzskaitē.
#    Init_Win_bytes_* atstājam: tur -1 ir apzīmējums "loga izmērs nav zināms", nevis kļūda.
parbaudamas = [k for k in dati.select_dtypes(include="number").columns if not k.startswith("Init_Win_bytes")]
dati = dati[(dati[parbaudamas] >= 0).all(axis=1)]

# 6. solis: izmetam dublikātus (6806 rindas sākumā), jo identiskas plūsmas treniņa un testa daļā
#    ļautu modelim "atcerēties" atbildi un uzpūstu precizitāti.
dati = dati.drop_duplicates()

# 7. solis: pievienojam mērķa kolonnu 'Uzbrukums' (0 = normāla plūsma, 1 = jebkurš uzbrukums),
#    jo 15 klases ar dažām klasēm pa 11-36 rindām nav pamatoti prognozēt, bet "uzbrukums vai nē" ir jautājums,
#    uz kuru tīkla administratoram vajag atbildi.
dati["Uzbrukums"] = (dati["Label"] != "BENIGN").astype(int)

# 8. solis: atiestatām rindu numurus, jo pēc rindu izmešanas numerācija ir ar caurumiem.
dati = dati.reset_index(drop=True)

dati.to_csv(REZULTATA_FAILS, index=False)

print(f"Rindu skaits beigās: {len(dati)} (izmestas {rindas_sakuma - len(dati)})")
print(f"Kolonnu skaits beigās: {dati.shape[1]}")
print("Normālas (0) un uzbrukuma (1) plūsmas:")
print(dati["Uzbrukums"].value_counts().to_string())
print(f"Saglabāts: {REZULTATA_FAILS.name}")
