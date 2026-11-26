# bibliotēkas ielāde
from pathlib import Path  # Importē rīku darbam ar failu ceļiem (lai skripts atrastu tirs.csv pēc savas atrašanās vietas)
import pandas as pd  # Importē bibliotēku darbam ar tabulām.
from sklearn.metrics import accuracy_score, confusion_matrix  # Importē precizitātes un kļūdu matricas rīkus.
from sklearn.model_selection import train_test_split  # Importē datu sadalīšanas rīku.
from sklearn.tree import DecisionTreeClassifier  # Importē lēmumu koka algoritmu.

# Ielādē datus.
dati = pd.read_csv(Path(__file__).parent / "tirs.csv")  # Nolasa CSV datu failu no skripta mapes.

# 'Label' (uzbrukuma nosaukums) jāizmet no pazīmēm, jo tas tieši atklāj atbildi.
pazimes = dati.drop(columns=["Label", "Uzbrukums"])  # Atlasa pazīmes, izmetot atbilžu kolonnas.
atbilde = dati["Uzbrukums"]  # Saglabā mērķa kolonnu (pareizās atbildes).

# 75 % datu treniņam, 25 % testam; stratify nodrošina, ka abās daļās ir vienāda normālo/uzbrukumu proporcija.
pazimes_train, pazimes_test, atbilde_train, atbilde_test, label_train, label_test = train_test_split(  # Sadala datus treniņa un testa kopās.
    pazimes, atbilde, dati["Label"], test_size=0.25, random_state=42, stratify=atbilde  # Norāda 25 % testa apjomu un saglabā klašu proporciju.
)

modelis = DecisionTreeClassifier(max_depth=10, random_state=42)  # Izveido lēmumu koka modeli ar maksimālo dziļumu 10.
modelis.fit(pazimes_train, atbilde_train)  # Apmāca modeli uz treniņa datiem.
prognoze = modelis.predict(pazimes_test)  # Prognozē atbildes testa datiem.

# Bāzes līnija: vienmēr nosaucam biežāko klasi, kāda bija treniņa datos.
biezakais = atbilde_train.mode()[0]  # Atrod biežāk sastopamo klasi treniņa datos.
baze = accuracy_score(atbilde_test, [biezakais] * len(atbilde_test))  # Aprēķina bāzes precizitāti, vienmēr minot biežāko klasi.
precizitate = accuracy_score(atbilde_test, prognoze)  # Aprēķina izveidotā modeļa precizitāti.

print(f"Treniņa rindas: {len(pazimes_train)}, testa rindas: {len(pazimes_test)}")  # Izdrukā treniņa un testa rindu skaitu.
print(f"Modeļa precizitāte testā: {precizitate:.4f} | Bāzes līnija (vienmēr '{biezakais}'): {baze:.4f}")  # Izdrukā modeļa un bāzes precizitātes salīdzinājumu.

if precizitate > baze:  # Pārbauda, vai modelis ir labāks par bāzes līniju.
    print("Modelis bāzes līniju pārspēj.")  # Paziņo, ka modelis ir veiksmīgs.
else:  # Pretējā gadījumā (ja modelis nav labāks).
    print("Modelis bāzes līniju NEPĀRSPĒJ.")  # Paziņo, ka modelis ir vājāks par minēšanu.

# Kļūdu sadalījums: kuras plūsmas modelis sajauca un kādā virzienā.
pareizi_normala, nepamatota_trauksme, nepamanits_uzbrukums, pareizi_uzbrukums = confusion_matrix(atbilde_test, prognoze).ravel()  # Sadala kļūdu matricu četros pamata rādītājos.
print("\nKļūdu matrica (testa dati):")  # Izdrukā kļūdu matricas virsrakstu.
print(f"  Normāla plūsma atpazīta pareizi: {pareizi_normala}")  # Izdrukā pareizi noteikto normālo plūsmu skaitu (TN).
print(f"  Nepamatota trauksme (normāla -> uzbrukums): {nepamatota_trauksme}")  # Izdrukā viltus trauksmju skaitu (FP).
print(f"  Nepamanīts uzbrukums (uzbrukums -> normāla): {nepamanits_uzbrukums}")  # Izdrukā palaisto uzbrukumu skaitu (FN).
print(f"  Uzbrukums atpazīts pareizi: {pareizi_uzbrukums}")  # Izdrukā pareizi noteikto uzbrukumu skaitu (TP).

# Cik no katra uzbrukuma veida modelis noķēra.
rezultati = pd.DataFrame({"Label": label_test.values, "pareizi": (prognoze == atbilde_test.values)})  # Izveido tabulu ar uzbrukumu veidiem un prognozes pareizību.
print("\nPareizi atpazītu plūsmu daļa pa veidiem (testa dati):")  # Izdrukā detalizēto rezultātu virsrakstu.
print(rezultati.groupby("Label")["pareizi"].agg(["mean", "count"]).rename(columns={"mean": "daļa", "count": "rindas"}).round(3).sort_values("daļa").to_string())  # Grupē pēc uzbrukuma veida un izdrukā precizitāti un skaitu.

# Svarīgākās pazīmes - lai redzētu, uz ko modelis balstās.
svarigakas = pd.Series(modelis.feature_importances_, index=pazimes.columns).sort_values(ascending=False).head(5)  # Atlasa 5 modelim svarīgākās pazīmes.
print("\n5 svarīgākās pazīmes:")  # Izdrukā svarīgāko pazīmju virsrakstu.
print(svarigakas.round(3).to_string())  # Izdrukā šīs 5 pazīmes un to svarīgumu.