import sys

class Graf:
    def __init__(self):
        """
        inicializacija grafa z vozlisci in oznakami
        """
        self.vozlisca = []
        self.oznake = []


    # doda vozlisce v seznam vozlisc
    def dodaj_vozlisce(self, vozlisce):
        """
        Doda vozlišče v seznam vozlisc
        """
        if vozlisce not in self.vozlisca:
            self.vozlisca.append(vozlisce)


    def dobi_vozlisce(self, oznaka):
        """
        Vrne vozlisce z doloceno oznako ali None, ce ne obstaja.
        """
        for v in self.vozlisca:
            if v.oznaka == oznaka:
                return v
        return None
    
    


class Vozlisce:
    def __init__(self, oznaka):
        """
        inicializacija vozlisca z oznako, seznamom sosedov in pre/post vrednostmi
        """
        self.oznaka = oznaka
        self.sosedi = []
        self.stars = -1
        self.obiskano = False
        # zacetni vrednosti pre in post bosta -1, da algoritem lepo deluje
        self.pre = 0 
        self.post = 0
        self.low = float('inf')
        self.prerezno = False


    def dodaj_soseda(self, sosed):
        if sosed not in self.sosedi:
            self.sosedi.append(sosed)



import sys

class Graf:
    def __init__(self):
        """
        Initialize the graph with vertices and labels.
        """
        self.vozlisca = []
        self.oznake = []

    def dodaj_vozlisce(self, vozlisce):
        """
        Add a vertex to the list of vertices.
        """
        if vozlisce not in self.vozlisca:
            self.vozlisca.append(vozlisce)

    def dobi_vozlisce(self, oznaka):
        """
        Return the vertex with a given label or None if it doesn't exist.
        """
        for v in self.vozlisca:
            if v.oznaka == oznaka:
                return v
        return None


class Vozlisce:
    def __init__(self, oznaka):
        """
        Initialize a vertex with a label, neighbors, and pre/post values.
        """
        self.oznaka = oznaka
        self.sosedi = []
        self.stars = None  # Parent node in DFS
        self.obiskano = False
        self.pre = 0  # Discovery time
        self.low = float('inf')  # Low value
        self.prerezno = False  # Whether the node is an articulation point

    def dodaj_soseda(self, sosed):
        if sosed not in self.sosedi:
            self.sosedi.append(sosed)


# def prerezna_vozisca(vozlisce, ura):
#     """
#     DFS-based function to calculate low and pre values and identify articulation points.
#     """
#     # Mark the current node as visited
#     vozlisce.obiskano = True

#     # Initialize discovery and low values
#     vozlisce.pre = ura[0]
#     vozlisce.low = ura[0]
#     ura[0] += 1

#     children = 0  # Count of children in DFS tree

#     for sosed in vozlisce.sosedi:
#         if not sosed.obiskano:
#             # Set parent and increase the child count
#             sosed.stars = vozlisce
#             children += 1

#             # Recur for the child node
#             prerezna_vozisca(sosed, ura)

#             # Update the low value of the current node
#             vozlisce.low = min(vozlisce.low, sosed.low)

#             # Articulation point check
#             # Case 1: Root node with more than one child
#             if vozlisce.stars is None and children > 1:
#                 vozlisce.prerezno = True

#             # Case 2: Non-root node where a child's low value is greater or equal to the node's pre value
#             if vozlisce.stars is not None and sosed.low >= vozlisce.pre:
#                 vozlisce.prerezno = True

#         elif sosed != vozlisce.stars:
#             # Update low value for a back edge
#             vozlisce.low = min(vozlisce.low, sosed.pre)

def dfs_prerezna_vozlisca(G):
    """
    Inicializira DFS za celoten graf in izračuna pre in low vrednosti.
    """
    ura = [0]  # Začetna ura za previsit in low
    for vozlisce in G.vozlisca:
        if not vozlisce.obiskano:  # Če vozlišče še ni obiskano, zaženi DFS
            dfs_prerezna(G, vozlisce, ura)


def dfs_prerezna_vozlisca(G):
    """
    Inicializira DFS za celoten graf in izračuna pre, low ter post vrednosti.
    """
    ura = [0]  # Začetna ura za previsit in low
    for vozlisce in G.vozlisca:
        if not vozlisce.obiskano:  # Če vozlišče še ni obiskano, zaženi DFS
            dfs_prerezna(G, vozlisce, ura)


def dfs_prerezna(G, vozlisce, ura, parent=None):
    """
    Rekurzivna DFS funkcija za nastavitev pre, low in post vrednosti ter preverjanje prereznih vozlišč.
    """
    # Nastavi pre in low za trenutno vozlišče
    vozlisce.obiskano = True
    vozlisce.pre = ura[0]
    vozlisce.low = ura[0]
    ura[0] += 1

    children = 0  # Število otrok v DFS drevesu

    for sosed in vozlisce.sosedi:
        if not sosed.obiskano:  # Če sosed še ni obiskan
            sosed.stars = vozlisce
            children += 1

            # Rekurzivno pokliči DFS za soseda
            dfs_prerezna(G, sosed, ura, vozlisce)

            # Posodobi low za trenutno vozlišče
            vozlisce.low = min(vozlisce.low, sosed.low)

            # Preveri, če je vozlišče prerezno
            if parent is None and children > 1:
                vozlisce.prerezno = True
            if parent is not None and sosed.low >= vozlisce.pre:
                vozlisce.prerezno = True

        elif sosed != parent:  # Povratna povezava
            vozlisce.low = min(vozlisce.low, sosed.pre)

    # Po koncu obiskovanja sosedov nastavi post vrednost
    vozlisce.post = ura[0]
    ura[0] += 1




def graf():
    """
    Reads input, constructs the graph, and initializes discovery.
    """
    input = sys.stdin.read
    data = input().strip().split("\n")

    # Number of vertices (n) and edges (m)
    n, m = map(int, data[0].split())

    G = Graf()

    # Read edges and add vertices and neighbors
    for i in range(1, m + 1):
        u, v = map(int, data[i].split())

        # Get or create vertices
        prvo = G.dobi_vozlisce(u)
        drugo = G.dobi_vozlisce(v)

        if prvo is None:
            prvo = Vozlisce(u)
            G.dodaj_vozlisce(prvo)
        
        if drugo is None:
            drugo = Vozlisce(v)
            G.dodaj_vozlisce(drugo)

        # Add neighbors
        prvo.dodaj_soseda(drugo)
        drugo.dodaj_soseda(prvo)

    # Find articulation points
    dfs_prerezna_vozlisca(G)

    return G


if __name__ == "__main__":
    G = graf()

    resitev = []
    for v in G.vozlisca:
        if v.prerezno:
            resitev.append(v.oznaka)
    
    if len(resitev) == 0:
        print(-1)

    else:
        koncno = " ".join(str(i) for i in resitev)
        print(koncno)

    # Print results
    # for v in G.vozlisca:
    #     print(f"vozlisce: {v.oznaka}, low: {v.low}, pre: {v.pre}, prerezno: {v.prerezno}")
