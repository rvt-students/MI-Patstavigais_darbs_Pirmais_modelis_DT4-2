# Rezultāti: uzbrukumu atpazīšana tīkla plūsmās

---

## 1. Kas ir šie dati un no kurienes tie nāk?

Dati ir CIC-IDS2017 kopa, ko izveidojusi Kanādas Kiberdrošības institūts (Ņūbransvikas Universitāte). Tīkla trafiks tika ierakstīts 2017. gada jūlijā laboratorijas tīklā, kur normālu lietotāju darbību imitēja speciāls skripts, bet uzbrukumus veica paši pētnieki (DDoS, PortScan, brute-force paroļu minēšana, Bot, tīmekļa uzbrukumi u. c.). 

Katra rinda ir viena tīkla plūsma (savienojums starp diviem datoriem), aprakstīta ar 78 skaitliskiem rādītājiem: ilgums, paketes un to izmēri, laiki starp paketēm, karodziņi u. c. Pēdējā kolonna `Label` norāda, vai plūsma ir `BENIGN` (normāla) vai kāda uzbrukuma veids. 

Mans fails ir samazināta versija (61 381 rinda; pilnā kopa ir vairākas reizes lielāka). Lejupielādes vieta norādīta `dati/AVOTS.txt`.

---

## 2. Kas ar datiem bija nepareizi un ko es ar tiem izdarīju?

* Duplikātus izmetu, lai treniņa un testa daļā nebūtu vienādu rindu.
* Bezgalīgas vērtības pārvērtu par trūkstošām (rodas, dalot ar plūsmas ilgumu 0).
* Izmetu rindas ar trūkstošām vērtībām.
* Izmetu negatīvus laika rādītājus, jo laika starpība nevar būt negatīva.
* Izmetu kolonnas ar vienādiem vērtībām, jo no tām nevar neko iemācīties.

> Pēc tīrīšanas palika **54 531 rinda** (izmestas 6 850) un **71 kolonna**. Izmestas konstantās kolonnas: ['Bwd PSH Flags', 'Bwd URG Flags', 'Fwd Avg Bytes/Bulk', 'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate', 'Bwd Avg Bytes/Bulk', 'Bwd Avg Packets/Bulk', 'Bwd Avg Bulk Rate']

---

## 3. Ko modelis prognozē un cik labi?

Modelis (lēmumu koks, `max_depth=10`) prognozē, vai plūsma ir uzbrukums. Dati sadalīti 75 % treniņam (40 898 rindas) un 25 % testam (13 633 rindas).

### Precizitāte testā
* **Modelis:** 99,14 %
* **Bāzes līnija (vienmēr atbildēt "uzbrukums"):** 87,90 %

Modelis bāzes līniju pārspēj par aptuveni 11 procentpunktiem. Bāzes līnija ir ļoti augsta, jo šajā izlasē 88 % plūsmu ir uzbrukumi. Reālā tīklā ir otrādi: gandrīz viss trafiks ir normāls. Tāpēc 99,14 % nav tik iespaidīgi, kā izklausās. 

### Kādas kļūdas modelis pieļauj (testa dati)
* **Patiesībā normāla -> Prognoze: normāla:** 1 547
* **Patiesībā normāla -> Prognoze: uzbrukums:** 103 (nepamatota trauksme)
* **Patiesībā uzbrukums -> Prognoze: normāla:** 14 (nepamanīts uzbrukums)
* **Patiesībā uzbrukums -> Prognoze: uzbrukums:** 11 969

* No normālajām plūsmām kļūdaini par uzbrukumu atzīti **6,2 %** (103 no 1 650).
* No uzbrukumiem nepamanīti **0,1 %** (14 no 11 983). Sliktāk atpazīts uzbrukuma veids "Infiltration": noķerti tikai 5 no 9 testa rindām, bet šīs klases pēc tīrīšanas ir tikai 35 rindas, tāpēc secinājums nav drošs.

Svarīgākā pazīme ir `Bwd Packet Length Min` (65 % no koka svarīguma), tad `Destination Port` (10 %).

> Jāņem vērā arī tas, ka tests ir tā pati laboratorijas ierakstu sesija, tikai nejauši sadalīta. Viena uzbrukuma plūsmas ir ļoti līdzīgas viena otrai, tāpēc rezultāts, iespējams, ir optimistiskāks nekā jaunā tīklā.

---

## 4. Ko es darītu ar prognozi reālā sistēmā?

Ja modelis plūsmu atzīst par uzbrukumu, sistēma automātiski izveido paziņojumu tīkla administratoram ar šīs plūsmas datiem (avota adrese, ports, laiks, svarīgākās pazīmes). 

Tehniķis pārbauda, vai tas ir īsts uzbrukums, un tikai tad nobloķē avotu ugunsmūrī. Plūsmu automātiski nebloķē, jo modeļa nepamatotu trauksmju daļa ir pārāk liela (skat. nākamo punktu).

---

## 5. Kas notiek, ja modelis kļūdās?

* Ja tas ir Nepamatota trauksme (normāla plūsma atzīta par uzbrukumu), tehniķis velta laiku, pārbaudot nevainīgu trafiku. Ja trauksmes ir bieži, cilvēki sāk tās ignorēt. Šajā modelī tā ir 6,2 % normālo plūsmu. Ja reālā tīklā ir miljons normālu plūsmu dienā, tās būtu ap 62 000 nepamatotu trauksmju dienā, ko neviens nevar pārbaudīt.
* Ja ir Nepamanīts uzbrukums (uzbrukums atzīts par normālu). Uzbrukums turpinās nepamanīts: var tikt nozagti dati, serveris var kļūt nepieejams vai uzbrucējs var iekļūt tīklā un palikt tajā ilgi. Šajā modelī tādu ir ļoti maz (0,1 %), bet reti uzbrukumu veidi (Infiltration) tiek nokavēti biežāk.

> **Kurš ir sliktāks?** Vienam atsevišķam gadījumam sliktāks ir nepamanīts uzbrukums, jo tā cena ir datu noplūde vai dīkstāve, nevis dažas zaudētas minūtes. Taču šim modelim praktiskā problēma ir nepamatotās trauksmes: tā kā reālā tīklā normāla trafika ir daudz vairāk nekā uzbrukumu, 6 % kļūdu tur pārplūdinātu tehniķus ar viltus trauksmēm, un tad arī īstie uzbrukumi tiktu pamanīti pārāk vēlu. Tāpēc šim modelim jāpalīdz tehniķim, nevis jāvietojas.

---

## 6. Ko ar šo modeli NEDRĪKST darīt

Nedrīkst to izmantot, lai **automātiski bloķētu lietotājus vai ierīces** reālā uzņēmuma tīklā. 

Tas kļūdaini atzīst 6 no 100 normālām plūsmām par uzbrukumu, tātad pārtrauktu parastu darbinieku darbu, un modelis ir apmācīts tikai uz 2017. gada laboratorijas datiem, kur normāla trafika bija tikai 12 %, tāpēc nav zināms, kā tas uzvestos mūsdienu tīklā.

---

## 7. Pašvērtējums

Izdevās izveidot pilnu ķēdi no neapstrādātiem datiem līdz modelim, un lielāko daļu darba (datu problēmas, to labošanu, rezultātus un secinājumus) es saprotu. 

Neizdevās līdz galam saprast dažus programmēšanas terminus kodā (kā arī bibliotēkas lietošanu), jo esmu tehniķis, nevis programmētājs. Tāpēc, protams, kā palīgu izmantoju mākslīgo intelektu. 

Nākamreiz es droši vien izvēlētos kādu vieglāku projektu, jo veidot lēmumu koku ar niecīgām programmēšanas zināšanām nav viegls darbs.