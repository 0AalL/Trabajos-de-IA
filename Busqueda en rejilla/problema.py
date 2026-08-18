class ProblemaRejilla:

    def __init__(self, filas, columnas, inicial=None, objetivo=None):
        self.filas = filas
        self.columnas = columnas

        # Primera casilla
        self.inicial = inicial if inicial is not None else (0, 0)

        # Última casilla
        self.objetivo = objetivo if objetivo is not None else (filas - 1, columnas - 1)

    def es_objetivo(self, estado):
        return estado == self.objetivo

    def acciones(self, estado):
        fila, columna = estado

        acciones = []

        if fila > 0:
            acciones.append("ARRIBA")

        if fila < self.filas - 1:
            acciones.append("ABAJO")

        if columna > 0:
            acciones.append("IZQUIERDA")

        if columna < self.columnas - 1:
            acciones.append("DERECHA")

        return acciones

    def resultado(self, estado, accion):
        fila, columna = estado

        if accion == "ARRIBA":
            return (fila - 1, columna)

        elif accion == "ABAJO":
            return (fila + 1, columna)

        elif accion == "IZQUIERDA":
            return (fila, columna - 1)

        elif accion == "DERECHA":
            return (fila, columna + 1)

        return None