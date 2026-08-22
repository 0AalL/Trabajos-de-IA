from nodo import Nodo
from lista_prioridad import listaPrioridad, listaPrioridad
from heuristica import HeuristicaManhattan


class PrimeroElMejor:

    def __init__(self, problema):

        self.problema = problema
        self.heuristica = HeuristicaManhattan()

        self.nodos_expandidos = 0
        self.arbol = []

    def resolver(self):

        self.nodos_expandidos = 0
        self.arbol = []

        nodo_inicial = Nodo(
            self.problema.inicial
        )

        frontera = listaPrioridad()

        h = self.heuristica.calcular(
            nodo_inicial.estado,
            self.problema.meta
        )

        frontera.insertar(
            h,
            nodo_inicial
        )

        visitados = set()

        while not frontera.esta_vacia():

            nodo = frontera.extraer()

            if nodo.estado in visitados:
                continue

            visitados.add(nodo.estado)

            

            # Guardamos el nodo expandido
            self.arbol.append(nodo)

            # Comprobar si es la meta
            if nodo.estado.es_meta(
                self.problema.meta
            ):
                return nodo

            # Generar sucesores
            for movimiento, estado in self.problema.sucesores(
                nodo.estado
            ):
                self.nodos_expandidos += 1
                if estado not in visitados:

                    nuevo_nodo = Nodo(
                        estado=estado,
                        padre=nodo,
                        movimiento=movimiento,
                        costo=nodo.costo + 1
                    )

                    h = self.heuristica.calcular(
                        estado,
                        self.problema.meta
                    )

                    frontera.insertar(
                        h,
                        nuevo_nodo
                    )

        return None