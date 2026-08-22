class Estado:

    def __init__(self, tablero):
        self.tablero = tuple(tablero)

    def __eq__(self, otro):
        return self.tablero == otro.tablero

    def __hash__(self):
        return hash(self.tablero)

    def __str__(self):
        resultado = ""

        for i in range(0, 9, 3):
            fila = self.tablero[i:i + 3]

            resultado += " ".join(
                "_" if x == 0 else str(x)
                for x in fila
            )

            resultado += "\n"

        return resultado

    def es_meta(self, meta):
        return self.tablero == meta.tablero