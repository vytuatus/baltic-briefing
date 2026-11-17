import json, sys, copy
T = "2026-11-17"
R = sys.argv[1]
SUB = "migration"

ED = {
 "headline": "Pirmasis migracijos skilties leidimas. Baltarusijos spaudimas sutelktas į Latviją, kur bandymų neteisėtai kirsti sieną 2026 m. jau daugiau nei per visus 2025 m., o Latvija nori išlaikyti specialų pasienio režimą iki 2027 m. vidurio. ES lygmeniu Baltijos šalys oficialiai priskirtos rizikos grupei ir negali būti priverstos priimti perkeliamų migrantų; apie migrantų perdavimą Baltijos šalims iš kitų ES valstybių nepranešta.",
 "pressure_note": "Latvijos pasieniečių duomenimis, iki lapkričio 10 d. sustabdyti 12 857 bandymai kirsti sieną iš Baltarusijos – daugiau nei 12 046 per visus 2025 m.; pastarųjų dienų skaičiai siekia kelias dešimtis per parą. Kontrabandininkai, tuneliai ir pasienio įrangos gadinimas tęsiasi. Lietuvoje ir Lenkijoje bandymų gerokai mažiau, o Estija gruodžio 1 d. uždaro kelių pasienio punktus su Rusija.",
 "eu_note": "Pagal ES migracijos paktą kiekviena šalis pati renkasi, ar priimti žmones, mokėti, ar teikti kitą paramą; Latvija ir Lietuva sako, kad perkeliamų migrantų nepriims, o Estija gali prašyti sumažinti savo dalį. Po lapkričio 6 d. Komisijos ataskaitos deramasi dėl 2027 m. Vokietija pagal ES taisykles atnaujina grąžinimą į Italiją ir Graikiją, o ne į Baltijos šalis.",
 "changed": "Pirmasis leidimas, todėl ankstesnės dienos palyginimui nėra. Skaičiai apima tai, apie ką pranešta lapkričio 10–17 d.; nuo rytojaus jie apims tik tai, kas nauja nuo ankstesnio leidimo.",
 "bottom_line": "Įrodymai rodo dvi skirtingas rizikas. Artimiausia – Baltarusijos organizuojamas spaudimas: Latvijos prokurorai aprašo kontrabandininkų tinklus, maždaug 5 000 dolerių mokestį už sienos kirtimą, migrantus, verčiamus gadinti pasienio įrangą, ir įtariamą Baltarusijos pasieniečių dalyvavimą – tai atitinka Lietuvos 2026 m. grėsmių vertinime aprašytą hibridinį spaudimą. Antroji, kurios baiminasi daugelis, – kad kitos ES šalys perkels savo migrantus į Baltijos šalis. Pagal dabartines taisykles tokia galimybė ribota: perkėlimas praktiškai yra savanoriškas, 2026 m. visoje ES tikimasi fiziškai perkelti mažiau nei 1 000 žmonių, o Baltijos šalys atsisakė jų priimti. Galintis augti teisėtas kanalas – grąžinimas žmonių, kurie į ES pirmą kartą pateko per Latviją ar Lietuvą ir keliavo toliau į vakarus; Lenkija jau tikrina savo sieną su Lietuva iki 2027 m. kovo ir grąžina žmones atgal. Teiginių, kad ES verčia Baltijos šalis priimti tūkstančius migrantų, nepagrindžia nei taisyklės, nei skaičiai. Kasdieniai sienos kirtimo skaičiai labai svyruoja ir skelbiami netolygiai, todėl pavienės dienos mažai ką pasako.",
}

IND = {
 "belarus-crossings": ("Bandymai kirsti sieną iš Baltarusijos", "Latvija: iki 2026 m. lapkričio 10 d. sustabdyti 12 857 bandymai kirsti sieną – jau daugiau nei 12 046 per visus 2025 m. (5 388 – 2024 m.); lapkričio pradžioje – maždaug 20–40 per parą. Lietuva grąžina gerokai mažiau žmonių, o bandymų Lenkijos pasienyje nuo 2025 m. smarkiai sumažėjo. Spaudimas sutelktas į 173 km Latvijos sieną.", "Oficialus pareiškimas"),
 "smuggling": ("Kontrabandininkų tinklai ir organizuotas sienos kirtimas", "Lapkričio 10 d. Latvijos pasieniečiai rado septynis iš Baltarusijos atvykusius žmones, sugrūstus į mažą automobilį, kurį vairavo Baltarusijos pilietis. Šiemet Latvija pradėjo 179 baudžiamąsias bylas dėl neteisėto žmonių gabenimo ir padidino didžiausią bausmę iki 12 metų. Prokurorai teigia, kad migrantai verčiami gadinti pasienio įrangą, ir įtaria Baltarusijos pasieniečių dalyvavimą; naudoti ir tuneliai.", "Oficialus pareiškimas"),
 "russia-border": ("Siena su Rusija: Estija, Latvija, Suomija", "Estija gruodžio 1 d. uždarys Narvos, Luhamaa ir Koidulos kelių pasienio punktus po sabotažo bandymo, kurį priskiria Rusijai; jos premjeras sako, kad pasieniečiai pasirengę galimam migraciniam spaudimui. Suomijos sausumos siena su Rusija uždaryta nuo 2023 m. Apie migrantų antplūdį prie Rusijos sienos nepranešta.", "Oficialus pareiškimas"),
 "eu-solidarity": ("ES solidarumo ir perkėlimo sprendimai", "Lapkričio 6 d. Komisijos ataskaitoje Estija, Latvija, Lietuva, Lenkija ir Suomija priskirtos migracinio spaudimo rizikos grupei, todėl joms pirmenybė teikiant ES paramą; Estija ir dar penkios šalys gali prašyti sumažinti 2027 m. įnašą. 2027 m. fondo dydis ir kiekvienos šalies dalis dabar derinami Taryboje. Kiekviena šalis renkasi: priimti žmones, mokėti ar teikti kitą paramą.", "Oficialus pareiškimas"),
 "transfers": ("Perdavimai atgal į Baltijos šalis", "Nepranešta, kad kitos ES šalys didesniais mastais siųstų migrantus į Baltijos šalis. Vokietija pagal naujas taisykles atnaujina grąžinimą į Italiją ir Graikiją. Baltijos regione žmonės, atvykę per Latviją ir keliavę toliau per Lietuvą, pagal trišalį susitarimą grąžinami į Latviją maždaug per 30 dienų.", "Analizė"),
 "schengen-checks": ("Patikros Šengeno erdvės viduje", "Lenkija pratęsė patikras pasienyje su Lietuva ir Vokietija iki 2027 m. kovo 30 d.; nuo 2025 m. liepos Lietuvos pasienyje atsisakyta įleisti beveik 1 300 žmonių. Šios patikros lėtina keliones ir dalį grąžinamų žmonių nukreipia atgal Lietuvos link.", "Oficialus pareiškimas"),
 "onward-routes": ("Tranzito maršrutai per Baltijos šalis", "Pagrindinis maršrutas eina iš Baltarusijos į Latviją, toliau per Lietuvą ir Lenkiją Vokietijos link. Lietuvos pasieniečių teigimu, neteisėta migracija per Latviją 2025 m. išaugo daugiau nei dvigubai, o Lenkijos patikros sulaikė žmonių, atvykusių iš Lietuvos. Šią savaitę apie naujus maršrutus nepranešta.", "Oficialus pareiškimas"),
 "asylum-capacity": ("Prieglobsčio prašymai ir priėmimo pajėgumai", "ES prieglobsčio agentūros duomenimis, Lietuvos prieglobsčio prašymų 2025 m. sumažėjo, palyginti su 2024 m. Lietuva rengia papildomas apgyvendinimo vietas, o ekspertai įspėja, kad Latvijai būtų sunku žiemą priimti ir apdoroti staiga atvykusią didelę grupę. Apie pajėgumų krizę nepranešta.", "Oficialus pareiškimas"),
 "law-rights": ("Apgręžimo įstatymas, teismai ir teisės", "Lietuva sako, kad, nepaisant ES pakto, toliau apgręš žmones Baltarusijos pasienyje pagal ekstremaliąją padėtį, o Latvija siūlo pratęsti sustiprintą pasienio režimą iki 2027 m. birželio 30 d. Žmogaus teisių organizacijos Lietuvoje, Latvijoje ir Lenkijoje ragina peržiūrėti apgręžimo praktiką, o migrantams padėję Lenkijos aktyvistai vis dar persekiojami teisme.", "Oficialus pareiškimas"),
 "narratives": ("Dezinformacija ir retorika apie migraciją", "Faktų tikrintojai ne kartą paneigė teiginius, kad ES paktas verčia Baltijos šalis priimti daug migrantų. Maskva Estijos sienos uždarymą pateikia kaip priešiškumą rusams. Šią savaitę naujos didelės kampanijos apie migraciją Baltijos šalyse nerasta.", "Analizė"),
}

ST = {
 "latvia-record": ("Latvija: bandymų kirsti sieną iš Baltarusijos jau daugiau nei per visus 2025 m.",
   "Latvijos pasieniečių teigimu, nuo 2026 m. sausio 1 d. iki lapkričio 10 d. sustabdyti 12 857 bandymai kirsti sieną iš Baltarusijos, palyginti su 12 046 per visus 2025 m., 5 388 – 2024 m. ir 13 863 – 2023 m. Lapkričio 12 d. Vidaus reikalų ministerija pasiūlė iki 2027 m. birželio 30 d. pratęsti sustiprintą pasienio režimą Ludzos, Krāslavos, Augšdaugavos ir Daugpilio apylinkėse, nurodydama besitęsiantį spaudimą, tunelius ir pasienio įrangos gadinimą.",
   "Oficialus pareiškimas", "LETA duomenys per UA.NEWS ir BNN; kasdieniai skaičiai – iš LSM.",
   "Metų skaičius rodo sustabdytus bandymus, o ne žmones, todėl tas pats žmogus gali būti suskaičiuotas kelis kartus. Vis dėlto tendencija aiški ir atitinka Komisijos vertinimą, kad spaudimas iš Lenkijos persikėlė į Latviją."),
 "organised-pressure": ("Latvijos prokurorai: migrantai verčiami gadinti pasienio įrangą",
   "Latvijos prokurorų teigimu, Baltarusijos pusėje laukiantiems migrantams, negalintiems sumokėti maždaug 5 000 dolerių už sienos kirtimą, liepiama gadinti Latvijos pasienio infrastruktūrą arba grasinama smurtu, ir yra pagrįstų įtarimų dėl Baltarusijos pasieniečių dalyvavimo. Šiemet užfiksuota daugiau nei 60 gadinimo atvejų, pernai – 23. Lapkričio 10 d. pasieniečiai sulaikė Baltarusijos pilietį vairuotoją, vežusį septynis neteisėtai sieną kirtusius žmones; Latvija padidino didžiausią bausmę už neteisėtos migracijos organizavimą iki 12 metų.",
   "Oficialus pareiškimas", "LSM ir LTV „De facto“, per UA.NEWS; lapkričio 11 d. LSM pranešimas.",
   "Tai aiškiausias ženklas, kad spaudimas Latvijai yra organizuotas, o ne savaiminis. Teiginiai apie Baltarusijos pareigūnus kyla iš vykstančio tyrimo ir teisme dar nepatikrinti."),
 "eu-2027": ("ES solidarumas: Baltijos šalys – rizikos grupėje, ir niekas negali būti priverstas priimti žmonių",
   "Lapkričio 6 d. metinėje Komisijos ataskaitoje Estija, Latvija, Lietuva, Lenkija ir Suomija priskirtos migracinio spaudimo rizikos grupei, todėl joms pirmenybė teikiant ES paramą, o Estija ir dar penkios šalys gali prašyti sumažinti 2027 m. įnašą. Graikija, Kipras, Italija ir Ispanija – spaudimą patiriančios šalys, gaunančios pagalbą. 2026 m. ES sutarė dėl 21 000 perkėlimų ar lygiavertės paramos ir 420 mln. eurų, o kiekviena šalis pati renkasi, kaip prisidėti. Dabar Taryboje derinamas 2027 m. fondas.",
   "Oficialus pareiškimas", "Europos Komisijos ataskaita; ES Taryba; Euronews; Bytes Europe.",
   "Taisyklės veikia prieš priverstinį perskirstymą į Baltijos šalis. Euronews praneša, kad 2026 m. visoje ES iš tikrųjų bus perkelta mažiau nei 1 000 žmonių, nes dauguma šalių vietoj to moka."),
 "poland-checks": ("Lenkija patikras pasienyje su Lietuva išlaiko iki 2027 m. kovo",
   "Spalio 1 d. Lenkija šešiems mėnesiams, iki 2027 m. kovo 30 d., pratęsė patikras pasienyje su Lietuva ir Vokietija. Jos teigimu, nuo 2025 m. liepos Lietuvos pasienyje atsisakyta įleisti beveik 1 300 žmonių, o daugiau nei 130 sulaikyta už pagalbą neteisėtai kertant sieną.",
   "Oficialus pareiškimas", "Lenkijos vidaus reikalų ministerija; „Anadolu“ pagrįstas pranešimas.",
   "Tai pagrindinis būdas, kuriuo kaimyninės ES šalys stumia spaudimą atgal Lietuvos link. Pagal Šengeno taisykles tai teisėta ribotą laiką, tačiau patikros pratęstos jau ne kartą."),
 "estonia-closure": ("Estija nuo gruodžio 1 d. uždaro kelių pasienio punktus su Rusija",
   "Estija uždarys Narvos, Luhamaa ir Koidulos kelių pasienio punktus po sabotažo bandymo, kurį priskiria Rusijai. Jos premjeras sako, kad pasieniečiai pasirengę galimam bandymui permesti migrantus per sieną, kaip 2023 m. nutiko Suomijos pasienyje.",
   "Oficialus pareiškimas", "ERR, Al Jazeera ir kiti.",
   "Uždarymas yra saugumo atsakas, tačiau jis didina riziką, kad Rusija bandys nukreipti migrantus į žaliąją sieną, kaip darė su Suomija. Apie tokį judėjimą kol kas nepranešta."),
 "eu-returns": ("Grąžinimas pagal ES taisykles nukreiptas į Italiją ir Graikiją, o ne į Baltijos šalis",
   "Vokietija sako, kad grąžinimas į Italiją ir Graikiją pagal ES taisykles turėtų būti atnaujintas žmonėms, atvykusiems po to, kai 2026 m. birželio 12 d. įsigaliojo paktas. Nerasta pranešimų, kad Vokietija ar kitos Vakarų šalys planuotų grąžinimą į Baltijos šalis. Regione Lietuva pagal trišalį susitarimą grąžina per Latviją atvykusius žmones.",
   "Oficialus pareiškimas", "Il Sole 24 Ore; LRT.",
   "Žmonės, kurie į ES pirmą kartą pateko per Baltijos šalis, gali būti teisėtai grąžinti ten. Šis rodiklis parodys, jei toks grąžinimas ims augti."),
}

CL = {
 "forced-relocation": ("ES migracijos paktas verčia Baltijos šalis priimti migrantus iš kitų ES šalių", "Populistiniai politikai ir įrašai socialiniuose tinkluose Baltijos šalyse", "Nepatikrintas teiginys",
   "Paktas leidžia kiekvienai šaliai rinktis – priimti žmones, mokėti ar teikti kitą paramą; Latvija ir Lietuva pareiškė, kad perkeliamų migrantų nepriims, o 2026 m. visoje ES tikimasi perkelti mažiau nei 1 000 žmonių.",
   "Taisyklės ir paskelbti įsipareigojimai tam prieštarauja."),
 "latvia-10000": ("Latvija turės kasmet priimti 10 000 migrantų arba mokėti 200 mln. eurų", "Latvijos populistiniai politikai prieš 2024 m. Europos Parlamento rinkimus (patikrino Re:Baltica)", "Nepatikrintas teiginys",
   "Re:Baltica nustatė, kad tuo metu Latvijai skaičiuota 99 žmonės arba 2 mln. eurų; sutartas 2026 m. fondas visai ES – 21 000 perkėlimų ar lygiavertė parama.",
   "Senesnis teiginys, kuris vis dar sklando; skaičiai buvo išpūsti maždaug šimtą kartų."),
 "belarus-officials": ("Baltarusijos pasieniečiai padeda organizuoti neteisėtą migraciją į Latviją", "Latvijos prokurorai", "Oficialus pareiškimas",
   "Baltarusija į šią konkrečią bylą neatsakė; įrodymai gauti vykstant baudžiamajam tyrimui.",
   "Atitinka nuo 2021 m. dokumentuotą valstybės organizuojamą migraciją iš Baltarusijos, tačiau teisme dar nepatikrinta."),
 "forced-sabotage": ("Migrantai, negalintys sumokėti kontrabandininkams, verčiami gadinti Latvijos pasienio įrangą", "Latvijos prokurorai; LTV „De facto“", "Oficialus pareiškimas",
   "Remiamasi vykstančio tyrimo metu surinktais parodymais; nepriklausomo patvirtinimo kol kas nėra.",
   "Patikima ir konkretu, tačiau dar tiriama."),
}

CN = {
 "organised": "Vienas: lapkričio 10 d. netoli Baltarusijos sienos Ludzos apylinkėse sustabdytas automobilis su septyniais neteisėtai sieną kirtusiais žmonėmis, kurį vairavo Baltarusijos pilietis.",
 "measures": "Dvi: lapkričio 12 d. Latvijos pasiūlymas pratęsti sustiprintą pasienio režimą iki 2027 m. birželio ir lapkričio 15 d. Estijos sprendimas nuo gruodžio 1 d. uždaryti kelių pasienio punktus su Rusija.",
 "eu": "Šiuo laikotarpiu nėra; Komisijos ataskaita ir 2027 m. fondo pasiūlymas paskelbti lapkričio 6 d., anksčiau.",
 "transfers": "Nepranešta.",
 "claims": "Du šiandienos teiginiai įvertinti kaip melagingi: kad ES paktas verčia Baltijos šalis priimti migrantus ir ankstesnis teiginys apie „10 000 per metus“ Latvijai.",
}

TOPICS = {
 "Crossings from Belarus": "Sienos kirtimas iš Baltarusijos",
 "Smuggling": "Kontrabanda",
 "EU solidarity": "ES solidarumas",
 "Schengen checks": "Patikros Šengeno erdvėje",
 "Russia border": "Siena su Rusija",
 "Returns and pushbacks": "Grąžinimas ir apgręžimas",
 "Asylum and capacity": "Prieglobstis ir pajėgumai",
 "Onward routes": "Tranzito maršrutai",
 "Migration claims": "Teiginiai apie migraciją",
}
