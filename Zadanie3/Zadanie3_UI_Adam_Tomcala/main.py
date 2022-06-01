import random
import time


def nacitaj_zahradu(vstupny_subor):
    """
    Funkcia nacita zahradu zo suboru ulozi ju do 2D listu.
    :param vstupny_subor:   Subor, z ktoreho citam.
    :return:                Vratim zahradu v 2D liste.
    """
    z = []
    for riadok in vstupny_subor:
        z.append(list(riadok[:len(riadok) - 1]))
    return z


def vytvor_vstupy_mnicha(sirka, vyska):
    """
    Funkcia vytvori list, ktory obsahuje vstupy do zahrady. Pocita sa to na zaklade obvodu zahrady.
    :param sirka:   Sirka zahrady.
    :param vyska:   Vyska zahrady.
    :return:        Vstupy do zahrady.
    """
    return [x for x in range(2*(sirka+vyska))]


def random_vstupy(vstupne_policka):
    """
    Funckia, ktora nahodne poprehadzuje vstupy mnicha do zahrady.
    :param vstupne_policka:     Vstupy do zahrady.
    :return:                    Poprehadzovane vstupy do zahrady.
    """
    velkost = len(vstupne_policka)
    for ii in range(velkost):                            # Cyklus na vytvorenie random poradia
        index = random.randrange(0, velkost)
        index2 = random.randrange(0, velkost)
        if index == index2:
            ii -= 1
            continue
        vstupne_policka[index], vstupne_policka[index2] = vstupne_policka[index2], vstupne_policka[index]

    return vstupne_policka


def vytvor_rozhodnutie():
    """
    Funkcia vytvori 1 rozhodnutie mnicha.
    :return:    1 bit, ktory symbolizuje pohyb mnicha (jeho rozhodnutie).
    """
    bit = random.getrandbits(1)
    if bit:
        return bit
    return -1


def vytvor_rozhodnutia(z):
    """
    Funkcia vytvara list rozhodnuti mnicha, vytvorim tolko rozhodnuti, kolko je prekazok v zahrade na zaciatku.
    :param z:   Vstupna zahrada.
    :return:    List rozhodnuti mnicha.
    """
    rozhodnutia = []
    for riadok in z:
        for policka in riadok:
            if policka == 'X':
                rozhodnutia.append(vytvor_rozhodnutie())

    if not rozhodnutia:
        rozhodnutia.append(1)
        rozhodnutia.append(-1)

    return rozhodnutia


def vytvor_mnicha(z):
    """
    Funkcia vytvara mnicha.
    ->  fitness mnicha na zaciatku. 0
    ->  vstupy mnicha do zahrady.   list[0, .. , MxN zahrady]
    ->  rozhodnutia mnicha.         list[1, -1, -1, 1, 1, ...]

    :param z:   Vstupna zahrada.
    :return:    Mnich.       -->    list[fitness, rozhodnutia, vstupy do zahrady]
    """
    vstupy = vytvor_vstupy_mnicha(len(z[0]), len(z))         # vytvorenie vstupov do zahrady a nahodne preusporiadanie
    vstupy = random_vstupy(vstupy)

    rozhodnutia = vytvor_rozhodnutia(z)                     # vytvorenie rozhodnuti mnicha

    return [0, rozhodnutia, vstupy]


def max_fitness_zahrady(z):
    """
    Funkcia vrati pocet upravitelnych policok v zahrade.
    :param z:   Vstupna zahrada.
    :return:    Fitness zahrady. -> maximalny pocet policok, ktory sa da upravit.
    """
    fitness = 0
    for riadok in z:
        for policka in riadok:
            if policka == '0':
                fitness += 1
    return fitness


# smer 1/-1 -> hore,vpravo/dole,vlavo

def urci_smer(vstup, sirka, vyska):
    """
    Funkcia urci smer mnicha na zaklade vstupu do zahradky.
    :param vstup:   Vstup do zahradky.  Int
    :param sirka:   Sirka zahrady.      Int
    :param vyska:   Vyska zahrady.      Int
    :return:        Smer mnicha         Char
    """
    if vstup < sirka:
        return 'D'
    elif vstup < sirka + vyska:
        return 'L'
    elif vstup < 2*sirka + vyska:
        return 'U'
    elif vstup < 2*sirka + 2*vyska:
        return 'R'


# pozicia -> [x, y], okrajoveho policka, podla rozmeru zahrady
def najdi_vstupnu_poziciu(vstup, sirka, vyska):
    """
    Funkcia urci suradnice vstupneho policka mnicha na zaklade sirky a vysky zahrady.

        0 1 2
      9       3       --> Vstupy do zahrady
      8       4
        7 6 5

    Vyberiem napr. vstup 1 -> jeho suradnice:   [0,1]

    :param vstup:   Konkretny vstup do zahradky.    Int
    :param sirka:   Sirka zahrady.                  Int
    :param vyska:   Vyska zahrady.                  Int
    :return:        Suradnice vstupneho policka.    [riadok - 1, stlpec - 1]
    """
    if vstup < sirka:
        return [0, vstup % sirka]
    elif vstup < sirka + vyska:
        return [abs(vstup - sirka) % vyska, sirka - 1]
    elif vstup < 2*sirka + vyska:
        return [vyska - 1, sirka - (abs(vstup - sirka - vyska) % sirka) - 1]
    else:
        return [vyska - (abs(vstup - 2*sirka - vyska) % vyska) - 1, 0]


def skontroluj_policko(policko, z):
    """
    Funkcia skontroluje ci sa dane policko uz nenachadza mimo zahradu.
    Ak je v zahrade, kontroluje sa ci sa da upravit.
    :param policko:     Policko, ktore sa kontroluje.
    :param z:
    :return:
    """
    if policko[0] < 0 or policko[1] < 0 or policko[0] >= len(z) or policko[1] >= len(z[0]):
        return "Koniec tahu"

    return z[policko[0]][policko[1]] == '0'


def urob_pohyb(pozicia, smer, cislo_tahu, z):
    """
    Funkcia pohne mnicha danym smerom a zapise do zahrady prechod mnnicha (cislo aktualneho tahu).
    :param pozicia:     Pozicia, z ktorej sa chceme pohnut.
    :param smer:        Smer, akym sa chceme pohnut.
    :param cislo_tahu:  Cislo tahu mnicha.
    :param z:           Zahrada.
    :return:            Vrati poziciu po vykonani pohybu. [x,y]
    """
    z[pozicia[0]][pozicia[1]] = str(cislo_tahu)

    if smer == 'L':
        pozicia[1] -= 1

    elif smer == 'R':
        pozicia[1] += 1

    elif smer == 'U':
        pozicia[0] -= 1

    elif smer == 'D':
        pozicia[0] += 1

    return pozicia


def urob_tah(z, vstup, cislo_tahu, r_index):
    """
    Funkcia urobi pohyb na zaklade vstupnej pozicie. Ak sa na danom policku nachadza prekazka, kontroluju sa 2 nove
    policka (na zaklade jeho pohybu). Ak sa moze pohnut do oboch, mnich si vyberie policko na zaklade jeho rozhodnuti.
    Ak je volne iba jedno policko, ide do neho.
    Ak nie je ani jedno volne, mnich sa zasekol, koniec.
    :param z:           Aktualna zahradka.
    :param vstup:       Vstup do zahradky.
    :param cislo_tahu:  Cislo, ktore zapisem do zahradky.
    :param r_index:     Index, ktory urcuje, ktore rozhodnutie si mnich vyberie.
    :return:            Int, Int (Ukoncenie alebo pokracovanie, r_index)
    """
    smer = urci_smer(vstup, len(z[0]), len(z))                              # Urcenie smeru na zaklade vstupu.
    vstupna_pozcia = najdi_vstupnu_poziciu(vstup, len(z[0]), len(z))        # Prepocitanie vstupu na [x,y].
    pozicia = vstupna_pozcia
    if not skontroluj_policko(pozicia, z):                                  # Na vstupnu poziciu sa neda vstupit.
        return 2, r_index

    while True:
        kontrola = skontroluj_policko(pozicia, z)
        if kontrola == "Koniec tahu":                               # koniec tahu
            return 1, r_index
        elif kontrola:                                              # mozem sa presunut na dane policko
            pozicia = urob_pohyb(pozicia, smer, cislo_tahu, z)
        elif not kontrola:                                          # nemozem sa presunut na dane policko
            if smer == 'L':                                         # Testovanie dvoch policok.
                kontrola1 = skontroluj_policko([pozicia[0] - 1, pozicia[1] + 1], z)     # jedno spat a hore
                kontrola2 = skontroluj_policko([pozicia[0] + 1, pozicia[1] + 1], z)     # jedno spat a dole
            elif smer == 'R':
                kontrola1 = skontroluj_policko([pozicia[0] - 1, pozicia[1] - 1], z)     # jedno spat a hore
                kontrola2 = skontroluj_policko([pozicia[0] + 1, pozicia[1] - 1], z)     # jedno spat a dole
            elif smer == 'U':
                kontrola1 = skontroluj_policko([pozicia[0] + 1, pozicia[1] + 1], z)     # jedno spat a vpravo
                kontrola2 = skontroluj_policko([pozicia[0] + 1, pozicia[1] - 1], z)     # jedno spat a vlavo
            else:
                kontrola1 = skontroluj_policko([pozicia[0] - 1, pozicia[1] + 1], z)     # jedno spat a vpravo
                kontrola2 = skontroluj_policko([pozicia[0] - 1, pozicia[1] - 1], z)     # jedno spat a vlavo

            if smer == 'U' or smer == 'D':
                smer1 = 'R'
                smer2 = 'L'
            else:
                smer1 = 'U'
                smer2 = 'D'

            if (kontrola1 and kontrola2) or (kontrola1 and kontrola2 == "Koniec tahu") or (kontrola1 == "Koniec tahu"
                and kontrola2):
                # Mnich si moze vybrat, na ktore policko vstupi.
                rozhodnutie = mnich[1][r_index % len(mnich[1])]
                if rozhodnutie == 1 and (smer == 'U' or smer == 'D'):
                    novy_smer = 'R'
                    if kontrola1 == "Koniec tahu":              # Ak si vyberie take, ze sa dostane za okraj, ukonci sa
                        return 1, r_index + 1                   # tah. (Plati pre kazde)
                elif rozhodnutie == -1 and (smer == 'U' or smer == 'D'):
                    novy_smer = 'L'
                    if kontrola2 == "Koniec tahu":
                        return 1, r_index + 1
                elif rozhodnutie == 1 and (smer == 'R' or smer == 'L'):
                    novy_smer = 'D'
                    if kontrola2 == "Koniec tahu":
                        return 1, r_index + 1
                elif rozhodnutie == -1 and (smer == 'R' or smer == 'L'):
                    novy_smer = 'U'
                    if kontrola1 == "Koniec tahu":
                        return 1, r_index + 1

                # Pohyby danym smerom, ktory si vybral mnich, na zaklade rozhodnuti.
                if smer == 'U':
                    smer = novy_smer
                    pozicia = urob_pohyb([pozicia[0] + 1, pozicia[1]], smer, cislo_tahu, z)
                elif smer == 'D':
                    smer = novy_smer
                    pozicia = urob_pohyb([pozicia[0] - 1, pozicia[1]], smer, cislo_tahu, z)
                elif smer == 'L':
                    smer = novy_smer
                    pozicia = urob_pohyb([pozicia[0], pozicia[1] + 1], smer, cislo_tahu, z)
                elif smer == 'R':
                    smer = novy_smer
                    pozicia = urob_pohyb([pozicia[0], pozicia[1] - 1], smer, cislo_tahu, z)

                r_index = r_index + 1
                continue

            # Iba jeden smer je dostupny, ak bude pohyb viest mimo zahradku -> Ukoncim tah.
            elif kontrola1 or kontrola1 == "Koniec tahu":
                if kontrola1 == "Koniec tahu" and not kontrola2:
                    return 1, r_index

                if smer == 'U':
                    smer = smer1
                    pozicia = urob_pohyb([pozicia[0] + 1, pozicia[1]], smer, cislo_tahu, z)

                elif smer == 'D':
                    smer = smer1
                    pozicia = urob_pohyb([pozicia[0] - 1, pozicia[1]], smer, cislo_tahu, z)

                elif smer == 'R':
                    smer = smer1
                    pozicia = urob_pohyb([pozicia[0], pozicia[1] - 1], smer, cislo_tahu, z)

                elif smer == 'L':
                    smer = smer1
                    pozicia = urob_pohyb([pozicia[0], pozicia[1] + 1], smer, cislo_tahu, z)

                continue

            # Iba jeden smer je dostupny, ak bude pohyb viest mimo zahradku -> Ukoncim tah.
            elif kontrola2 or kontrola2 == "Koniec tahu":
                if kontrola2 == "Koniec tahu":
                    return 1, r_index

                if smer == 'U':
                    smer = smer2
                    pozicia = urob_pohyb([pozicia[0] + 1, pozicia[1]], smer, cislo_tahu, z)

                elif smer == 'D':
                    smer = smer2
                    pozicia = urob_pohyb([pozicia[0] - 1, pozicia[1]], smer, cislo_tahu, z)

                elif smer == 'R':
                    smer = smer2
                    pozicia = urob_pohyb([pozicia[0], pozicia[1] - 1], smer, cislo_tahu, z)

                elif smer == 'L':
                    smer = smer2
                    pozicia = urob_pohyb([pozicia[0], pozicia[1] + 1], smer, cislo_tahu, z)

                continue

            # Mnich sa zasekol.
            return -1, 0


def uprav_zahradu(z, m, vypis):
    """
    Funkcia, ktora upravuje zahradu.
    :param z:   Vstupna zahrada.
    :param m:   Vstupny mnich.
    :return:    Nic.
    """
    cislo_tahu = 1
    rozhodnutie = 0

    for vstupne_policko in m[2]:

        flag, rozhodnutie = urob_tah(z, vstupne_policko, cislo_tahu, rozhodnutie)

        if flag == 1:
            cislo_tahu += 1
        if flag == 1 and vypis:
            print(najdi_vstupnu_poziciu(vstupne_policko, len(z[0]), len(z)))
            vypis_zahradu(z)
            print()
        elif flag == -1:
            break


def vypis_zahradu(z):
    """
    Funkcia, ktora vypise zahradu.
    :param z:   Vstupna zahrada.
    :return:    Nic.
    """
    for riadok in z:
        for policko in riadok:
            if len(policko) == 1:
                print(policko, end='  ')
            else:
                print(policko, end=' ')
        print()


def fitness_mnicha(z):
    """
    Funckia zistuje kolko policok dany mnich upravil.
    :param z:   Zahradka upravena mnichom.
    :return:    Int, pocet upravenych policok.
    """
    fitness = 0
    for riadok in z:
        for policko in riadok:
            if policko != "0" and policko != "X":
                fitness += 1
    return fitness


def vytvor_susedov(m, vst_subor):
    """
    Funkcia vytvara novych mnichov (susedov) od najlepsieho mnicha z predchadzajucej genereacie (susedstva)/
    :param m:               Najlepsi mnich z predchadzajucej popluacie (susedstva).
    :param vst_subor:       Subor, z ktoreho nacitavam zaciatocnu zahradku.
    :return:                List, ktory obsahuje susedov (mnichov).
    """
    s = []
    for index in range(10):
        novy_sused = [0, [y for y in m[1]], [z for z in m[2]]]
        novy_sused[1][index % len(m[1])] *= -1
        for j in range(10):
            r_num1 = random.randint(0, len(m[2]) - 1)
            r_num2 = random.randint(0, len(m[2]) - 1)
            if r_num1 == r_num2:
                j -= 1
                continue
            novy_sused[2][r_num1], novy_sused[2][r_num2] = novy_sused[2][r_num2], novy_sused[2][r_num1]

        s.append(novy_sused)

    for novy_sused in s:
        z = nacitaj_zahradu(vst_subor)
        vst_subor.seek(0)
        uprav_zahradu(z, novy_sused, False)
        novy_sused[0] = fitness_mnicha(z)

    return s


def vymaz_prveho(tabu):
    """
    Funkcia vymazuje prveho mnicha z tabu listu.
    :param tabu:    Tabu list.
    :return:        Update-nuty tabu list.
    """
    for index in range(0, len(tabu) - 1):
        tabu[index] = tabu[index+1]
    tabu.pop()
    return tabu


if __name__ == '__main__':

    mena_suborov = ["input.txt", "input2.txt"]
    print("Zadajte cislo mapy, ktoru chcete spustit: ")
    print(" 1, mapa 12x10 (lahsia mapa)")
    print(" 2, mapa 8x8   (tazsia mapa)")
    cislo_mapy = int(input("Cislo mapy: ")) - 1

    if cislo_mapy not in [0, 1]:
        print("Nespravne cislo mapy")
        exit(1)

    tabu_list_size = int(input("Zadajte velkost tabu listu "))

    pocet_opakovani = 10

    zaciatocny_cas = time.time()

    pocet_iteracii = 0

    for opakovanie in range(pocet_opakovani):

        subor = open(mena_suborov[cislo_mapy], "r")              # Otvorenie suboru, z ktoreho citam

        zahrada = nacitaj_zahradu(subor)            # nacitanie zahrady do 2D listu

        subor.seek(0)                               # Posuniem subor na zaciatok.

        max_fitness = max_fitness_zahrady(zahrada)  # Najdem kolko policok sa da poorat.

        mnich = vytvor_mnicha(zahrada)              # vytvorenie mnicha

        uprav_zahradu(zahrada, mnich, False)        # Upravim zahradu s danym mnichom.

        mnich[0] = fitness_mnicha(zahrada)

        najlepsi = mnich

        najlepsi_kanditat = mnich

        i = 1

        tabu_list = [najlepsi]

        najlepsii = []
        while najlepsi[0] != max_fitness:                           # Cyklus iteruje, kym sa nenajde vysledok
            susedia = vytvor_susedov(najlepsi_kanditat, subor)      # Vytvorenie susedov
            susedia.sort(key=lambda x: x[0], reverse=True)          # Usporiadanie podla fitness

            for sused in susedia:                                   # Odstranenie susedov
                if sused in tabu_list:                              # ktori sa nachadzaju v tabu liste
                    susedia.remove(sused)

            najlepsi_kanditat = susedia[0]                          # najlepsi kanditat je najlepsi
                                                                    # z danych susedov
            # print(susedia[0][0])

            if najlepsi_kanditat[0] > najlepsi[0]:                  # Ak je novonajdeny kandidat lepsi
                najlepsi = najlepsi_kanditat                        # ako celkovo najlepsi, prepisem ho

            najlepsii.append(najlepsi_kanditat[0])
            tabu_list.append(najlepsi_kanditat)                     # Pridam najlepsieho suseda do tabu listu

            if len(tabu_list) > tabu_list_size:                     # Ak sa v tabu liste nachadza viac mnichov
                vymaz_prveho(tabu_list)                             # ako je dovolene odstranim prveho

            i += 1
            if i > 5000:                                            # Ak cyklus prekroci 5000 iteracii,
                i -= 1
                break                                               # zastavim hladanie

        pocet_iteracii += i
        zahrada = nacitaj_zahradu(subor)
        if opakovanie == pocet_opakovani - 1:
            uprav_zahradu(zahrada, najlepsi, True)
            vypis_zahradu(zahrada)
        else:
            uprav_zahradu(zahrada, najlepsi, False)
            # vypis_zahradu(zahrada)

        # print(najlepsii)
        # print("Opakovanie " + str(opakovanie) + " " + str(i))

    koncovy_cas = time.time()

    print()
    print("Vykonalo sa %s opakovani." % pocet_opakovani)
    print("Celkovy cas trvania: %s s." % (koncovy_cas - zaciatocny_cas))
    print("Primerny cas: %s s." % ((koncovy_cas - zaciatocny_cas)/pocet_opakovani))
    print("Priemerny pocet iteracii: %s" % (pocet_iteracii // pocet_opakovani))
