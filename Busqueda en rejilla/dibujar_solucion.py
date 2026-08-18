def dibujar_camino(filas, columnas, camino):

    if camino is None or len(camino) == 0:
        return "No hay camino que dibujar.\n"

    posiciones = {}

    for i, posicion in enumerate(camino):

        # Inicio
        if i == 0:

            posiciones[posicion] = "S"

        # Objetivo
        elif i == len(camino) - 1:

            posiciones[posicion] = "G"

        else:

            fila_actual, columna_actual = camino[i]
            fila_siguiente, columna_siguiente = camino[i + 1]

            # Movimiento hacia arriba
            if fila_siguiente < fila_actual:

                posiciones[posicion] = "↑"

            # Movimiento hacia abajo
            elif fila_siguiente > fila_actual:

                posiciones[posicion] = "↓"

            # Movimiento hacia la izquierda
            elif columna_siguiente < columna_actual:

                posiciones[posicion] = "←"

            # Movimiento hacia la derecha
            elif columna_siguiente > columna_actual:

                posiciones[posicion] = "→"

    lineas = []

    lineas.append("\n")
    lineas.append("DIBUJO DEL CAMINO\n")
    lineas.append("==============================\n")

    for fila in range(filas):

        linea = ""

        for columna in range(columnas):

            posicion = (fila, columna)

            if posicion in posiciones:

                linea += f" {posiciones[posicion]} "

            else:

                linea += " . "

        lineas.append(linea + "\n")

    lineas.append("\n")
    lineas.append("S = Inicio\n")
    lineas.append("G = Objetivo\n")
    lineas.append("Flechas = dirección del camino\n")

    return "".join(lineas)