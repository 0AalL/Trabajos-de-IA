import time

from comprobar_solubilidad import puede_transformarse
from problema import Problema8Puzzle
from primero_mejor import PrimeroElMejor
from a_estrella import AEstrella


def estado_a_texto(estado):

    texto = ""

    for i in range(0, 9, 3):

        fila = estado.tablero[i:i + 3]

        texto += " ".join(
            "_" if x == 0 else str(x)
            for x in fila
        )

        texto += "\n"

    return texto

def mostrar_solucion(nodo):

    if nodo is None:

        print("No se encontró solución.")

        return

    camino = nodo.obtener_camino()

    print(
        "Número de movimientos:",
        len(camino) - 1
    )

    print()

    # ==============================
    # ESTADO INICIAL Y FINAL
    # ==============================

    

    # ==============================
    # ACCIONES DE LA SOLUCIÓN
    # ==============================

    acciones = [
        nodo_actual.movimiento
        for nodo_actual in camino
        if nodo_actual.movimiento
    ]

    print("ACCIONES:")
    print(" → ".join(acciones))

    print()
    print()

    # ==============================
    # CAMINO COMPLETO
    # ==============================

    for i, nodo_actual in enumerate(camino):

        print("------------------------")
        print("Paso:", i)

        if nodo_actual.movimiento:

            print(
                "Movimiento:",
                nodo_actual.movimiento
            )

        print(
            nodo_actual.estado
        )
def guardar_resultados(
    archivo,
    nombre,
    algoritmo,
    solucion,
    tiempo
):

    with open(
        archivo,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("=" * 70 + "\n")
        f.write(f"ALGORITMO: {nombre}\n")
        f.write("=" * 70 + "\n\n")

        if solucion is None:

            f.write(
                "NO SE ENCONTRÓ SOLUCIÓN.\n"
            )

            return

        # RESULTADOS

        f.write("RESULTADOS\n")
        f.write("-" * 70 + "\n")

        f.write(
            f"Número de movimientos: "
            f"{solucion.costo}\n"
        )

        f.write(
            f"Nodos expandidos: "
            f"{algoritmo.nodos_expandidos}\n"
        )

        f.write(
            f"Tiempo de ejecución: "
            f"{tiempo:.8f} segundos\n"
        )

        f.write("\n")

        # COMPLEJIDAD

        f.write("COMPLEJIDAD ASINTÓTICA\n")
        f.write("-" * 70 + "\n")

        if nombre == "PRIMERO EL MEJOR":

            f.write(
                "f(n) = h(n)\n\n"
            )

            f.write(
                "Tiempo:  O(b^m)\n"
            )

            f.write(
                "Espacio: O(b^m)\n\n"
            )

            f.write(
                "b = factor de ramificación\n"
            )

            f.write(
                "m = profundidad máxima\n"
            )

        else:

            f.write(
                "f(n) = g(n) + h(n)\n\n"
            )

            f.write(
                "Tiempo:  O(b^d)\n"
            )

            f.write(
                "Espacio: O(b^d)\n\n"
            )

            f.write(
                "b = factor de ramificación\n"
            )

            f.write(
                "d = profundidad de la solución\n"
            )

        # CAMINO

        f.write("\n")
        f.write("=" * 70 + "\n")
        f.write("CAMINO DE LA SOLUCIÓN\n")
        f.write("=" * 70 + "\n\n")

        camino = solucion.obtener_camino()

        for i, nodo in enumerate(camino):

            f.write(
                f"Paso {i}\n"
            )

            if nodo.movimiento:

                f.write(
                    f"Movimiento: "
                    f"{nodo.movimiento}\n"
                )

            f.write(
                estado_a_texto(nodo.estado)
            )

            h = algoritmo.heuristica.calcular(
                nodo.estado,
                algoritmo.problema.meta
            )

            f.write(
                f"g(n) = {nodo.costo}\n"
            )

            f.write(
                f"h(n) = {h}\n"
            )

            f.write(
                f"f(n) = "
                f"{nodo.costo + h}\n"
            )

            f.write("\n")



def ejecutar_algoritmo(
    nombre,
    algoritmo,
    archivo
):

    print("\n")
    print("=" * 60)
    print(nombre)
    print("=" * 60)

    inicio = time.perf_counter()

    solucion = algoritmo.resolver()

    fin = time.perf_counter()

    tiempo = fin - inicio

    if solucion is None:

        print("No se encontró solución.")

        return

    print(
        "Movimientos:",
        solucion.costo
    )

    print(
        "Nodos expandidos:",
        algoritmo.nodos_expandidos
    )

    print(
        "Tiempo:",
        f"{tiempo:.8f} segundos"
    )

    guardar_resultados(
        archivo,
        nombre,
        algoritmo,
        solucion,
        tiempo
    )

    print(
        f"\nResultados guardados en: "
        f"{archivo}"
    )

    mostrar_solucion(solucion)


def main():

    inicial = [
    7, 2, 4,
    5, 0, 6,
    8, 3, 1
]


    meta = [
        1, 2, 3,
        4, 5, 6,
        7, 8, 0
    ]
    problema = Problema8Puzzle(
            inicial,
            meta
        )
    print("ESTADO INICIAL:")
        #imprimir el estado inicial en formato de tablero como matriz
    print(estado_a_texto(problema.inicial))
        
    print()
        
    print("ESTADO FINAL:")
    print(estado_a_texto(problema.meta))
    if not puede_transformarse(inicial, meta):

        print("NO existe un camino del estado inicial al estado final.")
        return
   

    # ==========================================
    # PRIMERO EL MEJOR
    # ==========================================

    algoritmo = PrimeroElMejor(
        problema
    )
    print("ESTADO INICIAL:")
    #imprimir el estado inicial en formato de tablero como matriz
    print(estado_a_texto(problema.inicial))
    
    print()
    
    print("ESTADO FINAL:")
    print(estado_a_texto(problema.meta))
    ejecutar_algoritmo(
        "PRIMERO EL MEJOR",
        algoritmo,
        "resultados_primero_mejor.txt"
    )

    # ==========================================
    # A*
    # ==========================================

    algoritmo = AEstrella(
        problema
    )

    ejecutar_algoritmo(
        "A*",
        algoritmo,
        "resultados_a_estrella.txt"
    )


if __name__ == "__main__":
    main()