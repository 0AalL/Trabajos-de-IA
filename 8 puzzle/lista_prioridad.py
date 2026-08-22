from heapq import heappush, heappop


class listaPrioridad:

    def __init__(self):
        self.elementos = []
        self.contador = 0

    def insertar(self, prioridad, nodo):

        heappush(
            self.elementos,
            (prioridad, self.contador, nodo)
        )

        self.contador += 1

    def extraer(self):

        return heappop(self.elementos)[2]

    def esta_vacia(self):

        return len(self.elementos) == 0