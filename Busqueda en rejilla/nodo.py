class Nodo:
    def __init__(self, estado, padre=None, accion=None, profundidad=0):
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def obtener_camino(self):
        camino = []
        nodo = self

        while nodo is not None:
            camino.append(nodo.estado)
            nodo = nodo.padre

        camino.reverse()
        return camino

    def obtener_acciones(self):
        acciones = []
        nodo = self

        while nodo.padre is not None:
            acciones.append(nodo.accion)
            nodo = nodo.padre

        acciones.reverse()
        return acciones