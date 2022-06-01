import random
import math
import matplotlib.pyplot as plot
import time

hranice = [-5000, 5000]
offset = [-100, 100]
max_iteracii = 10000

farby = ["blue", "brown", "salmon", "orangered", "gold", "olive", "yellow", "tan", "green", "lime",
         "turquoise", "cyan", "blue", "indigo", "violet", "magenta", "pink", "gray", "red", "forestgreen"
         ]


def prve_body(pocet):
    """
    Funkcia vytvara random body na ploche
    :param pocet:   Pocet, kolko bodov treba vytvorit.
    :return:        Body
    """
    body = []
    for i in range(pocet):

        while True:
            x = random.randrange(hranice[0], hranice[1] + 1)
            y = random.randrange(hranice[0], hranice[1] + 1)

            if [x, y] not in body:
                body.append([x, y])
                break

    return body


def vygeneruj_body(pocet, body):
    """
    Funkcia vybera jeden z uz vytvorenych bodov a vytvara pomocou nahodneho offsetu dalsi bod.
    :param pocet:   Pocet bodov, ktory treba vyrobit
    :param body:    Pociatocne body.
    :return:        k bodov.
    """
    for i in range(pocet):
        random_bod = body[random.randrange(0, len(body))]
        offsetx1, offsetx2 = offset[0], offset[1]
        offsety1, offsety2 = offset[0], offset[1]

        # prepocitanie offsetu, ak je bod za hranicou
        if offsetx1 + random_bod[0] < hranice[0]:
            offsetx1 += abs(offsetx1 + random_bod[0]) % hranice[1]

        if offsetx2 + random_bod[0] > hranice[1]:
            offsetx2 -= (offsetx2 + random_bod[0]) % hranice[1]

        if offsety1 + random_bod[1] < hranice[0]:
            offsety1 += abs(offsety1 + random_bod[1]) % hranice[1]

        if offsety2 + random_bod[1] > hranice[1]:
            offsety2 -= (offsety2 + random_bod[1]) % hranice[1]

        # Overovanie ci bod uz existuje
        while True:
            novy_bod = [0, 0]
            novy_bod[0] = random_bod[0] + random.randrange(offsetx1, offsetx2 + 1)
            novy_bod[1] = random_bod[1] + random.randrange(offsety1, offsety2 + 1)
            if novy_bod not in body:
                body.append(novy_bod)
                break

    return body


def vytvor_pociatocne_body(body, k):
    """
    Funkcia vyberie k nahodnych bodov zo vsetkych bodov ako centra zhlukov.
    :param body:    Body, z ktorych vyberam.
    :param k:       Pocet centier.
    :return:        Centra zhlukov. list [[x,y], ..]
    """
    centra = []
    while True:
        if len(centra) == k:
            break
        random_bod = random.choice(body)
        novy_centroid = [random_bod[0], random_bod[1]]

        if novy_centroid not in centra:
            centra.append(novy_centroid)

    return centra


def zisti_vzdialenost(bod1, bod2):
    """
    Funkcia zisti eulerovsku vzdialenost medzi bodmi.
    :param bod1:    Bod 1
    :param bod2:    Bod 2
    :return:        Vzdialenost (float)
    """
    x = abs(bod1[0] - bod2[0])
    y = abs(bod1[1] - bod2[1])

    return math.sqrt(math.pow(x, 2) + math.pow(y, 2))


def zafarbi_body(centra, body):
    """
    Funkcia priradi body do jednotlivuych zhlukov podla centier.
    :param centra:  List centier.
    :param body:    List vsetkych bodov, ktore chceme zaradit.
    :return:        Zhluky (clasters).
    """
    zhluky = [[] for i in range(len(centra))]

    for bod in body:

        najmensia_vzd = zisti_vzdialenost(bod, centra[0])
        index = 0

        for i in range(1, len(centra)):
            nova_vzd = zisti_vzdialenost(bod, centra[i])
            if nova_vzd < najmensia_vzd:
                najmensia_vzd = nova_vzd
                index = i

        zhluky[index].append(bod)

    return zhluky


def prepocitaj_centroidy(zhluky):
    """
    Funkcia prepocita centra zhlukov ako centroidy.
    :param zhluky:  Klastre.
    :return:        Nove centroidy.
    """
    nove_centroidy = []

    for zhluk in zhluky:
        x, y = 0, 0
        for bod in zhluk:
            x += bod[0]
            y += bod[1]
        if len(zhluk) == 0:
            x, y = 0, 0
        else:
            x = round(x/len(zhluk))
            y = round(y/len(zhluk))
        nove_centroidy.append([x, y])

    return nove_centroidy


def vypocitaj_celkovu_vzd(aktualny_bod, zhluk):
    celkova_vzdialenost = 0

    for bod in zhluk:
        celkova_vzdialenost += zisti_vzdialenost(aktualny_bod, bod)

    return celkova_vzdialenost


def prepocitaj_medoidy(zhluky):
    """
    Funkcia prepocita centra zhlukov ako medoidy.
    :param zhluky:  Klastre.
    :return:        Nove medoidy.
    """
    nove_medoidy = []
    index = 0
    for zhluk in zhluky:
        najmensia_vzd = vypocitaj_celkovu_vzd(zhluk[0], zhluk)

        for i in range(1, len(zhluk)):
            vzdialenost = vypocitaj_celkovu_vzd(zhluk[i], zhluk)

            if vzdialenost < najmensia_vzd:
                najmensia_vzd, index = vzdialenost, i

        nove_medoidy.append(zhluk[index])

    return nove_medoidy


def vykresli(zhluky, centra, typ, iteracia):
    index = 0
    for z in zhluky:
        plot.scatter([b[0] for b in z], [b[1] for b in z], c=farby[index], s=1)
        index += 1
    plot.scatter([b[0] for b in centra], [b[1] for b in centra], c="black", s=3)
    plot.xlabel(str(typ) + " " + str(iteracia))
    plot.show()


def najdi_najvzdialenejsi(body, prvy_bod):
    najvacsia_vzdialenost = zisti_vzdialenost(body[0], prvy_bod)
    index = 0
    for i in range(1, len(body)):
        vzdialenost = zisti_vzdialenost(body[i], prvy_bod)

        if vzdialenost > najvacsia_vzdialenost:
            najvacsia_vzdialenost = vzdialenost
            index = i

    return [body[index]]


def k_means(body, pociatocne_body, typ):
    # Vytvorenie pociatocnych centier podla toho aky algo spustam.
    if typ == "D":
        centra = vytvor_pociatocne_body(body, 1)
        centra += najdi_najvzdialenejsi(body, centra[0])
    else:
        centra = [bod for bod in pociatocne_body]

    # Zaciatocne ofarbenie bodov
    zhluky = zafarbi_body(centra, body)

    if typ != "D":
        vykresli(zhluky, centra, typ, 0)

    i = 0
    for i in range(max_iteracii):
        # Vypocet novy centier
        if typ == "M":
            nove_centra = prepocitaj_medoidy(zhluky)
        else:
            nove_centra = prepocitaj_centroidy(zhluky)

        # Rozdelenie bodov podla novych centier
        zhluky = zafarbi_body(nove_centra, body)

        # Centra sa uz nezmenili
        if centra == nove_centra:
            break
        centra = nove_centra

    if typ != "D":
        vykresli(zhluky, centra, typ, i + 1)

    return zhluky, centra


def najdi_najhorsi_klaster(klastre, centra):
    """
    Funkcia vypocita celkovu priemernu vzdialenost bodov od jeho centra a zisti najhorsi klaster.
    :param klastre:     List vsetkych klastrov.
    :param centra:      List centier pre klastre.
    :return:            Najhorsia vzdialenost.
    """
    index = 0
    najhorsia_vzdialenost = vypocitaj_celkovu_vzd(centra[index], klastre[index]) / len(klastre[index])

    for i in range(1, len(klastre)):
        vzdialenost = vypocitaj_celkovu_vzd(centra[i], klastre[i]) / len(klastre[i])
        if vzdialenost > najhorsia_vzdialenost:
            najhorsia_vzdialenost = vzdialenost
            index = i
    return index


def divisive(body, k, pocet_b):

    pocet_klastrov = 2
    # rozdelenie vsetkych bodov do 2 klastrov
    klastre, centra = k_means(body, [], "D")
    vykresli(klastre, centra, "D", 0)

    iteracia = 1
    while True:
        if pocet_klastrov == k:
            break

        # Najdem si klaster s najhorsou celkovou vzdialenostou a idem ho delit
        najhorsi_index = najdi_najhorsi_klaster(klastre, centra)
        najhorsi_klaster = [bod for bod in klastre[najhorsi_index]]
        del klastre[najhorsi_index]
        del centra[najhorsi_index]

        nove_klastre, nove_centra = k_means(najhorsi_klaster, [], "D")

        # Pridanie novych klastrov do listu vsetkych klastrov
        klastre += nove_klastre

        centra += nove_centra

        vykresli(klastre, centra, "D", iteracia)

        iteracia += 1
        pocet_klastrov += 1
    uspesnost(klastre, centra, pocet_b)


def najdi_najmensiu_cestu(matica):
    velkost = len(matica)
    minimum = min(matica[1])

    index1, index2 = 1, matica[1].index(minimum)

    for i in range(2, velkost):
        aktualne_min = min(matica[i])
        if aktualne_min < minimum:
            minimum = aktualne_min
            index1, index2 = i, matica[i].index(aktualne_min)

    return index1, index2


def aglomerative(body, k, pocet_b):
    # kazdy bod je ako samostatny klaster
    klastre = []
    for i in range(len(body)):
        klastre.append([])
        klastre[i].append(body[i])

    # kazdy bod je svojim centrom
    centra = [bod for bod in body]

    pocet_klastrov = len(klastre)

    # vytvorenie trojuholnikovej matice vzdialenosti
    matica_vzdialenosti = [[0] * i for i in range(pocet_klastrov)]

    # Zistenie vzdialenosti medzi centrami
    for riadok in range(len(matica_vzdialenosti)):
        for stlpec in range(len(matica_vzdialenosti[riadok])):
            matica_vzdialenosti[riadok][stlpec] = zisti_vzdialenost(centra[riadok], centra[stlpec])

    # vykresli(klastre, centra, "D", -1)

    iteracie = 1
    while pocet_klastrov != k:
        # najdem indexi centier, ktore su pri sebe najblizsie
        index1, index2 = najdi_najmensiu_cestu(matica_vzdialenosti)

        # vytvorim z tychto dvoch klastrov novy
        novy_klaster = klastre[index1] + klastre[index2]

        # precitam nove centrum pre tento zhluk
        nove_centra = prepocitaj_centroidy([novy_klaster])

        # odstranim uz neexistujuce klastre a centra
        del klastre[index1]
        del klastre[index2]
        del centra[index1]
        del centra[index2]

        # pridam novy klaster a jeho cetrum do listov
        centra.append(nove_centra[0])
        klastre.append(novy_klaster)

        mensie = min(index1, index2)
        vacsie = max(index1, index2)

        # vymazanie neexistujucich vzdialenosti v matici
        for i in range(mensie + 1, len(matica_vzdialenosti)):
            del matica_vzdialenosti[i][mensie]
        del matica_vzdialenosti[mensie]
        vacsie -= 1
        for i in range(vacsie + 1, len(matica_vzdialenosti)):
            del matica_vzdialenosti[i][vacsie]
        del matica_vzdialenosti[vacsie]

        # pridanie noveho riadka pre novovzniknuty zhluk
        matica_vzdialenosti.append([0 for i in range(len(matica_vzdialenosti))])

        # vypocitanie vzdialenosti od noveho centra
        for i in range(len(matica_vzdialenosti) - 1):
            matica_vzdialenosti[-1][i] = zisti_vzdialenost(centra[i], centra[-1])

        pocet_klastrov -= 1

        if pocet_klastrov == k:
            vykresli(klastre, centra, "A", iteracie)

        iteracie += 1
    uspesnost(klastre, centra, pocet_b)


def uspesnost(zhluky, centra, pocet_bodov):
    pocet_zly = 0
    for i in range(len(zhluky)):
        for bod in zhluky[i]:
            vzdialenost = zisti_vzdialenost(centra[i], bod)
            if vzdialenost > 500:
                pocet_zly += 1
    uspech = 100 - round(pocet_zly / pocet_bodov, 2) * 100
    print("Uspesnost zhlukovaca bola: " + str(uspech) + "%.")


def testovac(pocet_b, pocet_k):
    print("\nGenerovanie %d bodov + 20 inicializacnych.." % pocet_b)
    points = prve_body(20)

    points = vygeneruj_body(pocet_b, points)

    pociatocne_body = vytvor_pociatocne_body(points, pocet_k)

    print("Body boli vygenerovane.")
    print()

    print("Algoritmus 1, K-means (centroid).")
    print("Algoritmus 2, K-means (medoid).")
    print("Algoritmus 3, Divizivne zhlukovanie (centroid).")
    print("Algoritmus 4, Aglomerativne zhlukovanie (centroid).")
    print("Ukoncenie 0.")
    while True:
        z = []
        c = []
        while True:
            alg = int(input("Zadajte cislo testu: "))
            if 0 <= alg <= 4:
                break
            print("Nespravne cislo alg.")

        if alg == 1:
            start_cas = time.time()
            z, c = k_means(points, pociatocne_body, "C")
            uspesnost(z, c, pocet_b + 20)
            end_cas = time.time()
            print("Celkovy cas " + str(round(end_cas - start_cas, 4)) + " s. (K-means, centroid)")
            z.clear()
            c.clear()
        elif alg == 2:

            start_cas = time.time()
            z, c = k_means(points, pociatocne_body, "M")
            uspesnost(z, c, pocet_b + 20)
            end_cas = time.time()
            print("Celkovy cas " + str(round(end_cas - start_cas, 4)) + " s. (K-means, medoid)")
            z.clear()
            c.clear()

        elif alg == 3:

            start_cas = time.time()
            divisive(points, pocet_k, pocet_b + 20)
            end_cas = time.time()
            print("Celkovy cas " + str(round(end_cas - start_cas, 4)) + " s. (Divisive, centroid)")

        elif alg == 4:

            start_cas = time.time()
            aglomerative(points, pocet_k, pocet_b + 20)
            end_cas = time.time()
            print("Celkovy cas " + str(round(end_cas - start_cas, 4)) + " s. (Aglomerative, centroid)")

        else:
            break


if __name__ == "__main__":
    print("Test 1: pocet bodov 1 000, pocet klastrov 5.")
    print("Test 2: pocet bodov 2 500, pocet klastrov 10.")
    print("Test 3: pocet bodov 10 000, pocet klastrov 15.")
    print("Test 4: pocet bodov 20 000, pocet klastrov 20.")
    print("Test 5: Zadajte lubovolny pocet.")

    while True:
        cislo_testu = int(input("Zadajte cislo testu: "))
        if 1 <= cislo_testu <= 5:
            break
        print("Nespravne cislo testu.")

    if cislo_testu == 1:
        testovac(1000, 5)
    elif cislo_testu == 2:
        testovac(2500, 10)
    elif cislo_testu == 3:
        testovac(10000, 15)
    elif cislo_testu == 4:
        testovac(20000, 20)
    else:
        while True:
            pocet_bodov = int(input("Zadajte pocet bodov (1 000 - 20 000): "))
            if 1000 <= pocet_bodov <= 20000:
                break
            print("Nespravny rozsah.")
        while True:
            pocet_klastrov = int(input("Zadajte pocet klastrov (5 - 20): "))
            if 5 <= pocet_klastrov <= 20:
                break
            print("Nespravny pocet klastrov.")

        testovac(pocet_bodov, pocet_klastrov)
