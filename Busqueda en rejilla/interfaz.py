import random


def introducir_coordenada(nombre, filas, columnas):

    while True:

        try:

            fila = int(input(
                f"Introduce la fila de {nombre} (0-{filas - 1}): "
            ))

            columna = int(input(
                f"Introduce la columna de {nombre} (0-{columnas - 1}): "
            ))

            if not (0 <= fila < filas):

                print("La fila está fuera de rango.")
                continue

            if not (0 <= columna < columnas):

                print("La columna está fuera de rango.")
                continue

            return (fila, columna)

        except ValueError:

            print("Introduce números enteros.")


def generar_coordenadas_aleatorias(filas, columnas):

    inicial = (
        random.randint(0, filas - 1),
        random.randint(0, columnas - 1)
    )

    objetivo = (
        random.randint(0, filas - 1),
        random.randint(0, columnas - 1)
    )

    while objetivo == inicial:

        objetivo = (
            random.randint(0, filas - 1),
            random.randint(0, columnas - 1)
        )

    return inicial, objetivo


def seleccionar_posiciones(filas, columnas):

    print("\n¿Cómo quieres elegir las posiciones?")
    print("1. Introducir inicio y objetivo manualmente")
    print("2. Generarlos aleatoriamente")
    print(
        f"3. Configuración por defecto: "
        f"(0,0) -> ({filas - 1},{columnas - 1})"
    )

    while True:

        opcion = input("\nElige una opción (1/2/3): ")

        if opcion == "1":

            print("\n--- POSICIÓN INICIAL ---")

            inicial = introducir_coordenada(
                "inicio",
                filas,
                columnas
            )

            print("\n--- POSICIÓN OBJETIVO ---")

            objetivo = introducir_coordenada(
                "objetivo",
                filas,
                columnas
            )

            if inicial == objetivo:

                print(
                    "\nEl inicio y el objetivo no pueden ser iguales."
                )

                continue

            return inicial, objetivo

        elif opcion == "2":

            return generar_coordenadas_aleatorias(
                filas,
                columnas
            )

        elif opcion == "3":

            return (
                (0, 0),
                (filas - 1, columnas - 1)
            )

        else:

            print(
                "Opción no válida. "
                "Introduce 1, 2 o 3."
            )