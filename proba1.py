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


# def dfs_prerezna_vozlisca(G):
#     """
#     Inicializira DFS za celoten graf in izračuna pre, low ter post vrednosti iterativno.
#     """
#     ura = [0]  # Števec za čas odkritja in zaključka
#     for vozlisce in G.vozlisca:
#         if vozlisce.obiskano:
#             continue
#         prerezna_vozisca(G, vozlisce, ura)


def prerezna_vozlisca_iterativno(vozlisce, ura):
    """
    Iterativna funkcija DFS za iskanje prereznih vozlišč.
    """
    sklad = [(vozlisce, None)]  # (trenutno_vozlisce, starš)
    vozlisce.obiskano = True

    # Inicializacija dodatnih struktur
    vozlisce.pre = vozlisce.low = ura[0]
    ura[0] += 1
    children_map = {vozlisce: 0}  # Beleži število otrok za vsako vozlišče

    while sklad:
        trenutno, stars = sklad[-1]  # Pogledamo vozlišče na vrhu sklada, brez odstranitve

        child_processed = True  # Označuje, če so vsi sosedje obdelani
        for sosed in trenutno.sosedi:
            if sosed == stars:  # Ignoriraj povezavo nazaj k staršu
                continue
            if not sosed.obiskano:
                # Če sosed še ni obiskan, ga dodamo na sklad
                sklad.append((sosed, trenutno))
                sosed.obiskano = True
                sosed.pre = sosed.low = ura[0]
                ura[0] += 1

                children_map[trenutno] += 1  # Povečaj število otrok
                child_processed = False  # Še imamo soseda za obdelavo
                break  # Nadaljujemo z novim sosedom

            else:  # Back edge: posodobi low vrednost trenutnega vozlišča
                trenutno.low = min(trenutno.low, sosed.pre)

        if child_processed:  # Če so vsi sosedje obdelani, izvedemo "povratek"
            sklad.pop()  # Odstranimo trenutno vozlišče s sklada

            # Posodobi low starševskega vozlišča, če obstaja
            if stars:
                stars.low = min(stars.low, trenutno.low)

                # Preverjanje prereznih vozlišč:
                # Primer 2: Non-root vozlišče
                if stars.stars is not None and trenutno.low >= stars.pre:
                    stars.prerezno = True

            # Primer 1: Root vozlišče
            if stars is None and children_map[trenutno] > 1:
                trenutno.prerezno = True


def dfs_prerezna_vozlisca(G):
    """
    Inicializira DFS za celoten graf in iterativno izračuna pre, low in zazna prerezna vozlišča.
    """
    ura = [0]  # Števec za čas odkritja
    for vozlisce in G.vozlisca:
        if not vozlisce.obiskano:
            prerezna_vozlisca_iterativno(vozlisce, ura)



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
