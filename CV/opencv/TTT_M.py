
# Trumpesnis variantas

lentele = ["–", "–", "–", "–", "–", "–", "–", "–", "–"]
#globals
zaidimas_tesiasi = True
laimetojas = None
dabartinis_zaidejas = "X"

def lenteles_isdestymas():
    print (lentele[0], "|", lentele[1], "|", lentele[2])
    print (lentele[3], "|", lentele[4], "|", lentele[5])
    print (lentele[6], "|", lentele[7], "|", lentele[8])

def zaidimas():
    lenteles_isdestymas()
    while zaidimas_tesiasi:
        ejimas(dabartinis_zaidejas)
        ar_zaidimas_baigesi()
        zaidejo_pakeitimas()
    if laimetojas == "X" or laimetojas == "O":
        print (laimetojas, " - laimejo")
    elif laimetojas == None:
        print ("Lygiosios")

def ejimas(zaidejas):
    print (zaidejas, "-o eile")
    salyga = input("Irasykite skaiciu nuo 1 iki 9 ejimui atlikti: ")
    veikiantis = False
    while not veikiantis:
        while salyga not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            salyga = input("Tokio ejimo atlikti negalima. Irasykite skaiciu nuo 1 iki 9 ejimui atlikti:")
            salyga = int(salyga) - 1
        if lentele[salyga] == "–":
            veikiantis = True
        else:
            print ("Sis laukelis jau uzimtas. Eikite dar karta")
            lentele[salyga] = zaidejas
            lenteles_isdestymas()

def ar_zaidimas_baigesi():
    ar_laimejo()
    ar_lygiosios()

def ar_laimejo():
    global laimetojas
    laimejimas = laimejo()
    if laimejimas:
        laimetojas = laimejimas
    else:
        laimetojas == None
    return

def laimejo():
    global zaidimas_tesiasi
    eilute1 = lentele[0] == lentele[1] == lentele[2] != "–"
    eilute2 = lentele[3] == lentele[4] == lentele[5] != "–"
    eilute3 = lentele[6] == lentele[7] == lentele[8] != "–"
    stulpelis1 = lentele[0] == lentele[3] == lentele[6] != "–"
    stulpelis2 = lentele[1] == lentele[4] == lentele[7] != "–"
    stulpelis3 = lentele[2] == lentele[5] == lentele[8] != "–"
    istrizaine1 = lentele[2] == lentele[4] == lentele[6] != "–"
    istrizaine2 = lentele[8] == lentele[4] == lentele[0] != "–"
    if eilute1 or eilute2 or eilute3 or stulpelis1 or stulpelis2 or stulpelis3 or istrizaine1 or istrizaine2:
        zaidimas_tesiasi = False
    if eilute1 or stulpelis1:
        return lentele[0]
    elif eilute2 or stulpelis2 or istrizaine1:
        return lentele[4]
    elif stulpelis3 or eilute3 or istrizaine2:
        return lentele[8]
    return

def ar_lygiosios(statusas):
    global zaidimas_tesiasi
    if "–" not in lentele:
        zaidimas_tesiasi = False
    return

def zaidejo_pakeitimas():
    global dabartinis_zaidejas
    if dabartinis_zaidejas == "X":
        dabartinis_zaidejas = "O"
    elif dabartinis_zaidejas == "O":
        dabartinis_zaidejas = "X"
    return

zaidimas()
