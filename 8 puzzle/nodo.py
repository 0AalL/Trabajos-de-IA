class Nodo:

    contador_nodos = 0

    def __init__(
        self,
        estado,
        padre=None,
        movimiento=None,
        costo=0
    ):

        self.id = Nodo.contador_nodos
        Nodo.contador_nodos += 1

        self.estado = estado
        self.padre = padre
        self.movimiento = movimiento
        self.costo = costo

    def obtener_camino(self):

        camino = []
        nodo = self

        while nodo is not None:

            camino.append(nodo)
            nodo = nodo.padre

        camino.reverse()

        return camino