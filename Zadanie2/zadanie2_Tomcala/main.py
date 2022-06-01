from queue import PriorityQueue
from queue import Queue
import time


class Uzol:
    """
    Trieda uzol sluzi na vytvaranie novych stavov pri rieseni hlavolamu.
    Obsahuje tabulku (aktualny stav hlavolamu), rodica a smer pohybu
    """
    def __init__(self, pole, sirka, vyska, rodic=None, smer=""):
        self.tabulka = []
        self.sirka = sirka
        self.vyska = vyska
        for i in range(0, len(pole)):
            self.tabulka.append(pole[i])
        self.heuristika = 0
        self.rodic = rodic
        self.pohyb = smer

    def vypis_hlavolam(self):
        """
        Funkcia vypisuje dany stav. (tabulku)
        :return: None.
        """
        for i in range(0, self.vyska):
            for j in range(0, self.sirka):
                print(self.tabulka[i * self.sirka + j], end=" ")
            print()
        print()

    def vytvor_novy_vstup(self, vysledok, hodnota, index_nuly, index_cisla):
        """
        Funkcia vytvara novu tabulku pre zvoleny smer.
        :param vysledok:    Novy stav.
        :param hodnota:     Hodnota cisla, s ktorym sa vymenila 0.
        :param index_nuly:  Index, na ktorom sa nachadzala 0.
        :param index_cisla: Index, na ktorom sa nachadzala hodnota.
        :return:            Pole (novovytvorenu tabulku).
        """
        for i in range(0, len(self.tabulka)):
            if i == index_nuly:
                vysledok.append(hodnota)
            elif i == index_cisla:
                vysledok.append(0)
            else:
                vysledok.append(self.tabulka[i])
        return vysledok

    def hore(self):
        """
        Funkcia overuje ci sa moze uskutocnit pohyb hore.
        :return:  Tabulku (ak sa moze pohnut hore), inak None.
        """
        index = self.tabulka.index(0)
        if (index // self.sirka) - 1 < 0:
            return None
        return self.vytvor_novy_vstup([], self.tabulka[index - self.sirka], index, index - self.sirka)

    def dole(self):
        """
        Funkcia overuje ci sa moze uskutocnit pohyb dole.
        :return:  Tabulku (ak sa moze pohnut dole), inak None.
        """
        index = self.tabulka.index(0)
        if (index // self.sirka) + 1 >= self.vyska:
            return None
        return self.vytvor_novy_vstup([], self.tabulka[index + self.sirka], index, index + self.sirka)

    def vpravo(self):
        """
        Funkcia overuje ci sa moze uskutocnit pohyb vpravo.
        :return:  Tabulku (ak sa moze pohnut vpravo), inak None.
        """
        index = self.tabulka.index(0)
        if (index % self.sirka) + 1 >= self.sirka:
            return None
        return self.vytvor_novy_vstup([], self.tabulka[index + 1], index, index + 1)

    def vlavo(self):
        """
        Funkcia overuje ci sa moze uskutocnit pohyb vlavo.
        :return:  Tabulku (ak sa moze pohnut vlavo), inak None.
        """
        index = self.tabulka.index(0)
        if (index % self.sirka) - 1 < 0:
            return None
        return self.vytvor_novy_vstup([], self.tabulka[index - 1], index, index - 1)

    def pohyby(self, smer):
        """
        Funkcia zavola funkcia na konkretny pohyb.
        :param smer:    Smer, ktory sa chceme skusit pohnut.
        :return:        Vystupnu tabulku
        """
        if smer == 'H':
            return self.hore()
        elif smer == 'D':
            return self.dole()
        elif smer == 'L':
            return self.vlavo()
        elif smer == 'R':
            return self.vpravo()

    def pocet_zlych(self, konecny):
        """
        Funkcia zisti, kolko policok v danom stave nie je na rovnakych miestach ako v koncovom stave.
        Heuristika 1.
        :param konecny:     Uzol, s ktorym porovnavam.
        :return:            Nic.
        """
        for i in range(0, len(konecny.tabulka)):
            if self.tabulka[i] != konecny.tabulka[i]:
                self.heuristika += 1

    def manhattan(self, konecny):
        """
        Funckia zisti manhattansku vzdialenost kazdeho policka s polickom v koncovom stave.
        Heuristika 2.
        :param konecny:      Uzol, s ktorym porovnavam.
        :return:             Nic.
        """
        for i in range(0, len(konecny.tabulka)):
            if konecny.tabulka[i] == 0:
                continue
            index = self.tabulka.index(konecny.tabulka[i])
            self.heuristika += (abs(i // konecny.sirka - index // konecny.sirka)) + (
             abs(i % konecny.sirka - index % konecny.sirka))


def ries(vstup, vystup, sirka, vyska):
    """
    Funkcia riesi vstupne a vystupne stavy.
    Zistuje pocet vytvorenych uzlov pri heuristike 1 a 2.
    Zistuje pocet vsetkych iteracii pri heuristike 1 a 2.
    Zistuje pocet dlzky celkovej cesty pri heuristike 1 a 2.
    Casy jednotlivych heuristik.
    :param vstup:      Vstupny uzol.
    :param vystup:     Vystupny uzol.
    :param sirka:      Sirka hlavolamu.
    :param vyska:      Vyska hlavolamu.
    :return:           Nic.
    """
    print("Zaciatocny stav:")
    vstup.vypis_hlavolam()
    print("Konecny stav:")
    vystup.vypis_hlavolam()
    casy = []
    uzly = []
    pocty_iteracii = []
    cesty = []
    aktualny = None
    for heuristika in ["1", "2"]:
        pocet_iteracii = 0
        zac = vstup
        priorita = PriorityQueue()      # vytvorenie priority queue
        vytvorene_tabulky = []          # list, kde si uchovavam uz vygenerovane stavy
        pocet_uzlov = 1
        if heuristika == "1":
            zac.pocet_zlych(vystup)
        elif heuristika == "2":
            zac.manhattan(vystup)
        priorita.put((zac.heuristika, pocet_uzlov, zac))
        pocet_uzlov += 1
        start_cas = time.time()
        smery = ["Hore", "Dole", "Vpravo", "Vlavo"]
        while True:
            potomkovia = Queue()
            if priorita.empty():                # ak je priority queue prazdna nema riesenie
                break
            aktualny = priorita.get()
            str_ints = [str(ints) for ints in aktualny[2].tabulka]      # prevod tabulky do stringu
            if aktualny[2].tabulka == vystup.tabulka:                   # ak sa bude aktualny vstup rovnat
                break                                                   # koncovemu, naslo sa risenie
            elif str_ints not in vytvorene_tabulky:                     # ak dany uzol, nie je v prehladanych
                vytvorene_tabulky.append(str_ints)                    # vlozim ho tam a skusam mozne pohyby (potomkovia)
                pomocna = 0
                for smer in ['H', 'D', 'R', 'L']:
                    if aktualny[2].pohyby(smer) is not None:            # ak dany smer sa moze uskutocnit, vytvori sa
                        string_ints = [str(ints) for ints in aktualny[2].pohyby(smer)]
                        pomocna += 1
                    else:
                        pomocna += 1
                        continue
                    if string_ints not in vytvorene_tabulky:            # ak sa dany smer nenachadza v prehladanych,
                        potomkovia.put((aktualny[2].pohyby(smer), smery[pomocna - 1]))  # bude to potomok
                while not potomkovia.empty():                           # vkladanie potomkov do priority queue
                    pole = potomkovia.get()
                    novy_uzol = Uzol(pole[0], sirka, vyska, aktualny[2], pole[1])
                    if heuristika == "1":
                        novy_uzol.pocet_zlych(vystup)
                    else:
                        novy_uzol.manhattan(vystup)
                    pocet_uzlov += 1
                    priorita.put((novy_uzol.heuristika, pocet_uzlov, novy_uzol))
            pocet_iteracii += 1

        casy.append(time.time() - start_cas)
        pocty_iteracii.append(pocet_iteracii)
        uzly.append(pocet_uzlov)
        uzol = aktualny[2]
        cesta = []
        y = 0

        while uzol.rodic is not None:
            print("Smer pohybu: " + uzol.pohyb)
            uzol.vypis_hlavolam()
            cesta.append(uzol.pohyb)
            y += 1
            uzol = uzol.rodic
        print("Zaciatok: ")
        uzol.vypis_hlavolam()
        cesty.append(y)
    print(7*"-" + " Heuristika 1: " + 7*"-" + "  " + 7*"-" + " Heuristika 2: " + 7*"-")
    print(" Cas riesenia: %.4f           Cas riesenia: %.4f" % (casy[0], casy[1]))
    print(" Pocet uzlov: %d               Pocet uzlov: %d" % (uzly[0], uzly[1]))
    print(" Pocet iteracii: %d            Pocet iteracii: %d" % (pocty_iteracii[0], pocty_iteracii[1]))
    print(" Cena cesty: %d                 Cena cesty: %d" % (cesty[0], cesty[1]))
    print()


if __name__ == '__main__':
    print(10*"-" + " TESTY " + 10*"-")
    print("TEST 1: Hlavolam s rozmermi 3x2.")
    print("TEST 2: Hlavolam s rozmermi 4x2.")
    print("TEST 3: Hlavolam s rozmermi 3x3.")
    print("TEST 4: Hlavolam s rozmermi 5x2.")
    print("TEST 5: Hlavolam s rozmermi 4x3.")
    print("TEST 6: Hlavolam s rozmermi 6x2.")
    cislo_testu = input("Zadajte cislo TESTU: ")
    if cislo_testu == "1":
        zac_vstup = [1, 2, 0, 3, 4, 5]
        kon_vystup = [3, 4, 5, 0, 1, 2]
        zaciatok = Uzol(zac_vstup, 3, 2)
        koniec = Uzol(kon_vystup, 3, 2)
        ries(zaciatok, koniec, 3, 2)
    elif cislo_testu == "2":
        zac_vstup = [0, 1, 2, 3, 4, 5, 6, 7]
        kon_vystup = [3, 2, 5, 4, 7, 6, 1, 0]
        zaciatok = Uzol(zac_vstup, 4, 2)
        koniec = Uzol(kon_vystup, 4, 2)
        ries(zaciatok, koniec, 4, 2)
    elif cislo_testu == "3":
        zac_vstup = [1, 0, 2, 3, 4, 5, 6, 7, 8]
        kon_vystup = [8, 0, 6, 5, 4, 7, 2, 3, 1]
        zaciatok = Uzol(zac_vstup, 3, 3)
        koniec = Uzol(kon_vystup, 3, 3)
        ries(zaciatok, koniec, 3, 3)
    elif cislo_testu == "4":
        zac_vstup = [1, 2, 3, 4, 9, 5, 6, 0, 7, 8]
        kon_vystup = [5, 1, 9, 8, 7, 2, 4, 3, 6, 0]
        zaciatok = Uzol(zac_vstup, 5, 2)
        koniec = Uzol(kon_vystup, 5, 2)
        ries(zaciatok, koniec, 5, 2)
    elif cislo_testu == "5":
        zac_vstup = [1, 2, 0, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        kon_vystup = [2, 7, 4, 6, 1, 9, 3, 11, 10, 8, 0, 5]
        zaciatok = Uzol(zac_vstup, 4, 3)
        koniec = Uzol(kon_vystup, 4, 3)
        ries(zaciatok, koniec, 4, 3)
    elif cislo_testu == "6":
        zac_vstup = [1, 2, 3, 4, 5, 0, 6, 7, 8, 9, 10, 11]
        kon_vystup = [4, 5, 9, 11, 10, 8, 3, 2, 1, 6, 7, 0]
        zaciatok = Uzol(zac_vstup, 6, 2)
        koniec = Uzol(kon_vystup, 6, 2)
        ries(zaciatok, koniec, 6, 2)
    else:
        print("Zadali ste nespravny vstup.")
