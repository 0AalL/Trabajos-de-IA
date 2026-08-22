from nodo import Nodo
from lista_prioridad import listaPrioridad
from heuristica import HeuristicaManhattan


class AEstrella:

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

        f = nodo_inicial.costo + h

        frontera.insertar(
            f,
            nodo_inicial
        )

        costos = {
            nodo_inicial.estado: 0
        }

        while not frontera.esta_vacia():

            nodo = frontera.extraer()


            # Guardamos el nodo expandido
            self.arbol.append(nodo)

            # Comprobar si llegamos a la meta
            if nodo.estado.es_meta(
                self.problema.meta
            ):
                return nodo

            # Generar sucesores
            for movimiento, estado in self.problema.sucesores(
                nodo.estado
            ):
                self.nodos_expandidos += 1

                nuevo_costo = nodo.costo + 1

                if (
                    estado not in costos
                    or nuevo_costo < costos[estado]
                ):

                    costos[estado] = nuevo_costo

                    nuevo_nodo = Nodo(
                        estado=estado,
                        padre=nodo,
                        movimiento=movimiento,
                        costo=nuevo_costo
                    )

                    h = self.heuristica.calcular(
                        estado,
                        self.problema.meta
                    )

                    f = nuevo_costo + h

                    frontera.insertar(
                        f,
                        nuevo_nodo
                    )

        return None