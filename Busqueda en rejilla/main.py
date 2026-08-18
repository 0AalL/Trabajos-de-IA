import time
import random

from problema import ProblemaRejilla
from bfs import bfs
from dfs import dfs
from iddfs import iddfs
from bidireccional import bidireccional
from imprimir_arbol import imprimir_arbol


FILAS = 10
COLUMNAS = 20

factor_ramificacion = 3


def introducir_coordenada(nombre):

    while True:

        try:

            fila = int(input(
                f"Introduce la fila de {nombre} (0-{FILAS - 1}): "
            ))

            columna = int(input(
                f"Introduce la columna de {nombre} (0-{COLUMNAS - 1}): "
            ))

            if not (0 <= fila < FILAS):

                print("La fila está fuera de rango.")
                continue

            if not (0 <= columna < COLUMNAS):

                print("La columna está fuera de rango.")
                continue

            return (fila, columna)

        except ValueError:

            print("Introduce números enteros.")


def generar_coordenadas_aleatorias():

    inicial = (
        random.randint(0, FILAS - 1),
        random.randint(0, COLUMNAS - 1)
    )

    objetivo = (
        random.randint(0, FILAS - 1),
        random.randint(0, COLUMNAS - 1)
    )

    while objetivo == inicial:

        objetivo = (
            random.randint(0, FILAS - 1),
            random.randint(0, COLUMNAS - 1)
        )

    return inicial, objetivo


def mostrar_resultado(
    nombre,
    resultado,
    es_bidireccional=False,
    profundidad_consola=15,
    mostrar_arbol=True
):

    salida = ""
    salida_consola = ""

    if es_bidireccional:

        solucion, nodos_expandidos, raiz_inicio, raiz_objetivo = resultado

    else:

        solucion, nodos_expandidos, raiz = resultado

    # ==========================================
    # CABECERA
    # ==========================================

    cabecera = (
        "\n==============================\n"
        + nombre
        + "\n==============================\n"
    )

    salida += cabecera
    salida_consola += cabecera

    # ==========================================
    # SI NO HAY SOLUCIÓN
    # ==========================================

    if solucion is None:

        salida += "No se encontró solución.\n"
        salida_consola += "No se encontró solución.\n"

        if not mostrar_arbol:

            return salida, salida_consola

        if es_bidireccional:

            salida += "\nÁRBOL DE BÚSQUEDA DESDE EL INICIO:\n"
            salida += imprimir_arbol(raiz_inicio)

            salida += "\n\nÁRBOL DE BÚSQUEDA DESDE EL OBJETIVO:\n"
            salida += imprimir_arbol(raiz_objetivo)

            salida_consola += (
                "\nÁRBOL DE BÚSQUEDA DESDE EL INICIO "
                f"(primeros {profundidad_consola} niveles):\n"
            )

            salida_consola += imprimir_arbol(
                raiz_inicio,
                profundidad_maxima=profundidad_consola
            )

            salida_consola += (
                "\n\nÁRBOL DE BÚSQUEDA DESDE EL OBJETIVO "
                f"(primeros {profundidad_consola} niveles):\n"
            )

            salida_consola += imprimir_arbol(
                raiz_objetivo,
                profundidad_maxima=profundidad_consola
            )

        else:

            salida += "\n"
            salida += imprimir_arbol(raiz)

            salida_consola += (
                "\nÁRBOL DE BÚSQUEDA "
                f"(primeros {profundidad_consola} niveles):\n"
            )

            salida_consola += imprimir_arbol(
                raiz,
                profundidad_maxima=profundidad_consola
            )

        return salida, salida_consola

    # ==========================================
    # CAMINO
    # ==========================================

    if isinstance(solucion, list):

        camino = solucion

    else:

        camino = solucion.obtener_camino()

    datos = ""

    datos += "Camino:\n"
    datos += str(camino) + "\n"

    datos += "Longitud:\n"
    datos += str(len(camino) - 1) + "\n"

    datos += "Nodos expandidos:\n"
    datos += str(nodos_expandidos) + "\n"

    salida += datos
    salida_consola += datos

    # ==========================================
    # NO MOSTRAR ÁRBOL
    # ==========================================

    if not mostrar_arbol:

        return salida, salida_consola

    # ==========================================
    # ÁRBOLES
    # ==========================================

    if es_bidireccional:

        salida += "\nÁRBOL DE BÚSQUEDA DESDE EL INICIO:\n"
        salida += imprimir_arbol(raiz_inicio)

        salida += "\n\nÁRBOL DE BÚSQUEDA DESDE EL OBJETIVO:\n"
        salida += imprimir_arbol(raiz_objetivo)

        salida_consola += (
            "\nÁRBOL DE BÚSQUEDA DESDE EL INICIO "
            f"(primeros {profundidad_consola} niveles):\n"
        )

        salida_consola += imprimir_arbol(
            raiz_inicio,
            profundidad_maxima=profundidad_consola
        )

        salida_consola += (
            "\n\nÁRBOL DE BÚSQUEDA DESDE EL OBJETIVO "
            f"(primeros {profundidad_consola} niveles):\n"
        )

        salida_consola += imprimir_arbol(
            raiz_objetivo,
            profundidad_maxima=profundidad_consola
        )

    else:

        salida += "\n"
        salida += imprimir_arbol(raiz)

        salida_consola += (
            "\nÁRBOL DE BÚSQUEDA "
            f"(primeros {profundidad_consola} niveles):\n"
        )

        salida_consola += imprimir_arbol(
            raiz,
            profundidad_maxima=profundidad_consola
        )

    return salida, salida_consola


def ejecutar(
    nombre,
    funcion,
    problema,
    complejidad_tiempo,
    complejidad_espacio,
    es_bidireccional=False,
    mostrar_arbol=True
):

    inicio_tiempo = time.perf_counter()

    resultado = funcion(problema)

    fin_tiempo = time.perf_counter()

    salida, salida_consola = mostrar_resultado(
        nombre,
        resultado,
        es_bidireccional,
        mostrar_arbol=mostrar_arbol
    )

    tiempo = fin_tiempo - inicio_tiempo

    # ==========================================
    # INFORMACIÓN ADICIONAL
    # ==========================================

    informacion = ""

    informacion += "\nTiempo:\n"
    informacion += str(tiempo) + " segundos\n"

    informacion += "\nComplejidad temporal:\n"
    informacion += complejidad_tiempo + "\n"

    informacion += "\nComplejidad espacial:\n"
    informacion += complejidad_espacio + "\n"

    salida += informacion
    salida_consola += informacion

    print(salida_consola)

    return salida, resultado, tiempo


def main():

    print("==============================")
    print("     BÚSQUEDA EN UNA REJILLA")
    print("==============================")

    print(f"\nRejilla: {FILAS} x {COLUMNAS}")

    print("\n¿Cómo quieres elegir las posiciones?")
    print("1. Introducir inicio y objetivo manualmente")
    print("2. Generarlos aleatoriamente")
    print("3. Configuración por defecto: (0,0) -> (9,19)")

    while True:

        opcion = input("\nElige una opción (1/2/3): ")

        if opcion == "1":

            print("\n--- POSICIÓN INICIAL ---")
            inicial = introducir_coordenada("inicio")

            print("\n--- POSICIÓN OBJETIVO ---")
            objetivo = introducir_coordenada("objetivo")

            if inicial == objetivo:

                print("\nEl inicio y el objetivo no pueden ser iguales.")
                print("Vuelve a introducir las posiciones.\n")

                continue

            break

        elif opcion == "2":

            inicial, objetivo = generar_coordenadas_aleatorias()

            break

        elif opcion == "3":

            inicial = (0, 0)
            objetivo = (FILAS - 1, COLUMNAS - 1)

            break

        else:

            print("Opción no válida. Introduce 1, 2 o 3.")

    problema = ProblemaRejilla(
        FILAS,
        COLUMNAS,
        inicial,
        objetivo
    )

    # ==========================================
    # CONFIGURACIÓN
    # ==========================================

    print("\n==============================")
    print("CONFIGURACIÓN")
    print("==============================")

    print("Tamaño:", f"{FILAS} x {COLUMNAS}")
    print("Inicio:", problema.inicial)
    print("Objetivo:", problema.objetivo)
    print("Factor de ramificación máximo: b = 4")
    print("d = profundidad de la solución")
    print("m = profundidad máxima del árbol de búsqueda")

    # ==========================================
    # SALIDA TOTAL
    # ==========================================

    salida_total = ""

    salida_total += "==============================\n"
    salida_total += "     BÚSQUEDA EN UNA REJILLA\n"
    salida_total += "==============================\n\n"

    salida_total += f"Rejilla: {FILAS} x {COLUMNAS}\n"
    salida_total += f"Inicio: {problema.inicial}\n"
    salida_total += f"Objetivo: {problema.objetivo}\n"
    salida_total += f"Factor de ramificación: b = {factor_ramificacion}\n"
    salida_total += "d = profundidad de la solución\n"
    salida_total += "m = profundidad máxima del árbol de búsqueda\n"

    # ==========================================
    # BFS
    # ==========================================

    salida_bfs, resultado_bfs, tiempo_bfs = ejecutar(
        "BÚSQUEDA EN ANCHURA (BFS)",
        bfs,
        problema,
        f"O({factor_ramificacion}^d)",
        f"O({factor_ramificacion}^d)"
    )

    salida_total += salida_bfs

    # ==========================================
    # DFS
    # ==========================================

    salida_dfs, resultado_dfs, tiempo_dfs = ejecutar(
        "BÚSQUEDA EN PROFUNDIDAD (DFS)",
        dfs,
        problema,
        f"O({factor_ramificacion}^m)",
        f"O({factor_ramificacion}m)"
    )

    salida_total += salida_dfs

    # ==========================================
    # IDDFS
    # ==========================================

    salida_iddfs, resultado_iddfs, tiempo_iddfs = ejecutar(
        "PROFUNDIDAD ITERATIVA (IDDFS)",
        iddfs,
        problema,
        f"O({factor_ramificacion}^d)",
        f"O({factor_ramificacion}d)",
        mostrar_arbol=False
    )

    salida_total += salida_iddfs

    # ==========================================
    # BÚSQUEDA BIDIRECCIONAL
    # ==========================================

    salida_bidir, resultado_bidir, tiempo_bidir = ejecutar(
        "BÚSQUEDA BIDIRECCIONAL",
        bidireccional,
        problema,
        f"O({factor_ramificacion}^(d/2))",
        f"O({factor_ramificacion}^(d/2))",
        es_bidireccional=True
    )

    salida_total += salida_bidir

    # ==========================================
    # BUSCAR EL CAMINO MÁS CORTO
    # ==========================================

    resultados = [
        ("BFS", resultado_bfs, tiempo_bfs),
        ("DFS", resultado_dfs, tiempo_dfs),
        ("IDDFS", resultado_iddfs, tiempo_iddfs),
        ("Bidireccional", resultado_bidir, tiempo_bidir)
    ]

    soluciones = []

    for nombre, resultado, tiempo in resultados:

        solucion = resultado[0]
        nodos_expandidos = resultado[1]

        if solucion is None:
            continue

        if isinstance(solucion, list):

            camino = solucion

        else:

            camino = solucion.obtener_camino()

        longitud = len(camino) - 1

        soluciones.append(
            (
                longitud,
                nombre,
                camino,
                tiempo,
                nodos_expandidos
            )
        )

    # ==========================================
    # RESULTADO DEL CAMINO MÁS CORTO
    # ==========================================

    if soluciones:

        mejor_longitud = min(
            solucion[0]
            for solucion in soluciones
        )

        mejores = [
            solucion
            for solucion in soluciones
            if solucion[0] == mejor_longitud
        ]

        # Si hay empate en longitud, elegimos el que
        # haya tardado menos.
        mejor = min(
            mejores,
            key=lambda x: x[3]
        )

        longitud, nombre, camino, tiempo, nodos_expandidos = mejor

        resumen = (
            "\n======================================\n"
            "          CAMINO MÁS CORTO\n"
            "======================================\n"
            f"Método de búsqueda: {nombre}\n"
            f"Camino: {camino}\n"
            f"Longitud: {longitud}\n"
            f"Tiempo: {tiempo} segundos\n"
            f"Nodos expandidos: {nodos_expandidos}\n"
            "======================================\n"
        )

        print(resumen)

        salida_total += resumen

    else:

        resumen = (
            "\n======================================\n"
            "       NO SE ENCONTRÓ SOLUCIÓN\n"
            "======================================\n"
        )

        print(resumen)

        salida_total += resumen

    # ==========================================
    # GUARDAR RESULTADOS
    # ==========================================

    with open(
        "resultados.txt",
        "w",
        encoding="utf-8"
    ) as archivo:

        archivo.write(salida_total)

    print("\n======================================")
    print("Los resultados se han guardado en:")
    print("resultados.txt")
    print("======================================")


if __name__ == "__main__":
    main()