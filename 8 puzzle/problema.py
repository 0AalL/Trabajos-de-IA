from estado import Estado


class Problema8Puzzle:

    def __init__(self, inicial, meta):

        self.inicial = Estado(inicial)
        self.meta = Estado(meta)

    def posicion_vacio(self, estado):

        return estado.tablero.index(0)

    def sucesores(self, estado):

        sucesores = []

        posicion = self.posicion_vacio(estado)

        fila = posicion // 3
        columna = posicion % 3

        movimientos = {
            "ARRIBA": (-1, 0),
            "ABAJO": (1, 0),
            "IZQUIERDA": (0, -1),
            "DERECHA": (0, 1)
        }

        for movimiento, (df, dc) in movimientos.items():

            nueva_fila = fila + df
            nueva_columna = columna + dc

            # Comprobar que el movimiento es válido
            if 0 <= nueva_fila < 3 and 0 <= nueva_columna < 3:

                nueva_posicion = (
                    nueva_fila * 3 + nueva_columna
                )

                nuevo_tablero = list(estado.tablero)

                # Intercambiar el vacío con la ficha
                nuevo_tablero[posicion], nuevo_tablero[nueva_posicion] = (
                    nuevo_tablero[nueva_posicion],
                    nuevo_tablero[posicion]
                )

                nuevo_estado = Estado(nuevo_tablero)

                sucesores.append(
                    (movimiento, nuevo_estado)
                )

        return sucesores