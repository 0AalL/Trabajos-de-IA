class HeuristicaManhattan:

    def calcular(self, estado, meta):

        distancia = 0

        for numero in range(1, 9):

            posicion_actual = estado.tablero.index(numero)
            posicion_meta = meta.tablero.index(numero)

            fila_actual = posicion_actual // 3
            columna_actual = posicion_actual % 3

            fila_meta = posicion_meta // 3
            columna_meta = posicion_meta % 3

            distancia += (
                abs(fila_actual - fila_meta)
                +
                abs(columna_actual - columna_meta)
            )

        return distancia