import sys

class Graf:
    def __init__(self):
        """
        Inicializacija grafa s slovarjem za vozlisca
        """
        self.vozlisca = {}

    def dodaj_vozlisce(self, oznaka):
        """
        Dodajanje vozlisca in vracanje njegove oznake
        """
        if oznaka not in self.vozlisca:
            self.vozlisca[oznaka] = Vozlisce(oznaka)
        return self.vozlisca[oznaka]


class Vozlisce:
    def __init__(self, oznaka):
        """
        Inicializacija vozlisca z oznako, sosedi in atributi za izracun prereznosti
        """
        self.oznaka = oznaka
        self.sosedi = []
        self.stars = None 
        self.obiskano = False
        self.pre = 0 
        self.low = sys.maxsize
        self.prerezno = False 
        self.otroci = 0

    def dodaj_soseda(self, sosed):
        """
        Dodajanje soseda v seznam sosedov
        """
        self.sosedi.append(sosed)


def iterativen_dfs(graf, zacetna_oznaka):
    """
    Izvede iterativen DFS na grafu, kjer se izracuna se vrednosti "pre", "low" in doloci prerezna vozlisca
    """
    # stevec za cas, da se pre/low vrednosti zacnejo z 0
    cas = -1

    zacetek = graf.vozlisca[zacetna_oznaka]

    # stack za izvjaanje iterativnega dfs; rekurzija je prepocasna :|
    stack = [(zacetek, "vstop")]

    while stack:
        vozlisce, stanje = stack.pop()

        # vstop v vozlisce
        if stanje == "vstop":
            #ce vozlisce se ni obiskano, ga obisci in doloci pre, low
            if not vozlisce.obiskano:
                vozlisce.obiskano = True
                cas += 1
                vozlisce.pre = vozlisce.low = cas

                # dodajanje izstopa za vozlisce na sklad
                stack.append((vozlisce, "izstop"))

                # dodajanje vstopa v vse sosede
                for sosed in vozlisce.sosedi:
                    if not sosed.obiskano:
                        # dolocimo se starsa vozlisca za kasnejse racunanje low
                        sosed.stars = vozlisce
                        stack.append((sosed, "vstop"))
                    elif sosed != vozlisce.stars:
                        # ce je povratna povezava, updejtamo low
                        vozlisce.low = min(vozlisce.low, sosed.pre)

        # izstop iz vozlisca
        elif stanje == "izstop":
            cas += 1
            
            # updejtanje low za starsa
            if vozlisce.stars:
                vozlisce.stars.low = min(vozlisce.stars.low, vozlisce.low)
                vozlisce.stars.otroci += 1 

                # preverjanje prereznosti starsa; vozlisce.low >= stars.pre in se ne sme biti koren (drugi pogoj je nujen pri CIKLIH)
                if vozlisce.low >= vozlisce.stars.pre and vozlisce.stars.stars is not None:
                    vozlisce.stars.prerezno = True

            # robni primer: vozlisce je koren
            if vozlisce.stars is None and vozlisce.otroci > 1:
                vozlisce.prerezno = True

def resevanje():
    """
    Prebere vhodne podatke, zgradi graf in izvede iterativen dfs
    Vrne graf z izracunanimi prereznimi vozisci
    """

    data = sys.stdin.read().strip().split("\n")

    # stevilo vozlis (n) in povezav (m)
    n, m = map(int, data[0].split())

    G = Graf()

    # dodajanje vozlisc v graf
    for i in range(n):
        G.dodaj_vozlisce(i)

    # dodajanje povezav med vozlisci
    for i in range(1, m + 1):
        u, v = map(int, data[i].split())
        G.vozlisca[u].dodaj_soseda(G.vozlisca[v])
        G.vozlisca[v].dodaj_soseda(G.vozlisca[u])

    # poisce prerezna vozlisca
    iterativen_dfs(G, 0)

    return G


if __name__ == "__main__":
    G = resevanje()

    # zbere resitve v seznam in ga sortira 
    resitev = [v.oznaka for v in G.vozlisca.values() if v.prerezno]    
    resitev.sort()

    if resitev:
        print(" ".join(map(str, resitev)))
    else:
        print(-1)
