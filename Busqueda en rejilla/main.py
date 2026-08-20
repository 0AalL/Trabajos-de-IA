from problema import ProblemaRejilla

from bfs import bfs
from dfs import dfs
from iddfs import iddfs
from bidireccional import bidireccional

from interfaz import seleccionar_posiciones
from ejecucion import ejecutar
from resultados import obtener_datos_solucion
from dibujar_solucion import dibujar_camino


FILAS = 10
COLUMNAS = 20

factor_ramificacion = 3


def main():

    # ==========================================
    # CONFIGURACIÓN INICIAL
    # ==========================================

    print("==============================")
    print("     BÚSQUEDA EN UNA REJILLA")
    print("==============================")

    print(f"\nRejilla: {FILAS} x {COLUMNAS}")

    inicial, objetivo = seleccionar_posiciones(
        FILAS,
        COLUMNAS
    )

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
    print("Factor de ramificación máximo: b = ", factor_ramificacion)
    print("d = profundidad de la solución")
    print("m = profundidad máxima del árbol de búsqueda")

    # ==========================================
    # CABECERA DEL ARCHIVO
    # ==========================================

    salida_total = ""

    salida_total += "==============================\n"
    salida_total += "     BÚSQUEDA EN UNA REJILLA\n"
    salida_total += "==============================\n\n"

    salida_total += f"Rejilla: {FILAS} x {COLUMNAS}\n"
    salida_total += f"Inicio: {problema.inicial}\n"
    salida_total += f"Objetivo: {problema.objetivo}\n"
    salida_total += (
        f"Factor de ramificación: "
        f"b = {factor_ramificacion}\n"
    )

    salida_total += "d = profundidad de la solución\n"
    salida_total += (
        "m = profundidad máxima del árbol de búsqueda\n"
    )

    # ==========================================
    # BFS
    # ==========================================

    salida, resultado_bfs, tiempo_bfs = ejecutar(
        "BÚSQUEDA EN ANCHURA (BFS)",
        bfs,
        problema,
        f"O({factor_ramificacion}^d)",
        f"O({factor_ramificacion}^d)"
    )

    salida_total += salida

    # ==========================================
    # DIBUJO BFS
    # ==========================================

    solucion_bfs = resultado_bfs[0]

    if solucion_bfs is not None:

        camino_bfs, acciones_bfs = obtener_datos_solucion(
            solucion_bfs
        )

        dibujo_bfs = dibujar_camino(
            FILAS,
            COLUMNAS,
            camino_bfs
        )

        print("\nBFS - SOLUCIÓN")
        print(dibujo_bfs)

        salida_total += (
            "\nBFS - SOLUCIÓN\n"
            + dibujo_bfs
        )

    # ==========================================
    # DFS
    # ==========================================

    salida, resultado_dfs, tiempo_dfs = ejecutar(
        "BÚSQUEDA EN PROFUNDIDAD (DFS)",
        dfs,
        problema,
        f"O({factor_ramificacion}^m)",
        f"O({factor_ramificacion}m)"
    )

    salida_total += salida

    # ==========================================
    # DIBUJO DFS
    # ==========================================

    solucion_dfs = resultado_dfs[0]

    if solucion_dfs is not None:

        camino_dfs, acciones_dfs = obtener_datos_solucion(
            solucion_dfs
        )

        dibujo_dfs = dibujar_camino(
            FILAS,
            COLUMNAS,
            camino_dfs
        )

        print("\nDFS - SOLUCIÓN")
        print(dibujo_dfs)

        salida_total += (
            "\nDFS - SOLUCIÓN\n"
            + dibujo_dfs
        )

    # ==========================================
    # IDDFS
    # ==========================================

    salida, resultado_iddfs, tiempo_iddfs = ejecutar(
        "PROFUNDIDAD ITERATIVA (IDDFS)",
        iddfs,
        problema,
        f"O({factor_ramificacion}^d)",
        f"O({factor_ramificacion}d)",
        mostrar_arbol=True
    )

    salida_total += salida

    # ==========================================
    # DIBUJO IDDFS
    # ==========================================

    solucion_iddfs = resultado_iddfs[0]

    if solucion_iddfs is not None:

        camino_iddfs, acciones_iddfs = obtener_datos_solucion(
            solucion_iddfs
        )

        dibujo_iddfs = dibujar_camino(
            FILAS,
            COLUMNAS,
            camino_iddfs
        )

        print("\nIDDFS - SOLUCIÓN")
        print(dibujo_iddfs)

        salida_total += (
            "\nIDDFS - SOLUCIÓN\n"
            + dibujo_iddfs
        )

    # ==========================================
    # BIDIRECCIONAL
    # ==========================================

    salida, resultado_bidir, tiempo_bidir = ejecutar(
        "BÚSQUEDA BIDIRECCIONAL",
        bidireccional,
        problema,
        f"O({factor_ramificacion}^(d/2))",
        f"O({factor_ramificacion}^(d/2))",
        es_bidireccional=True
    )

    salida_total += salida

    # ==========================================
    # DIBUJO BIDIRECCIONAL
    # ==========================================

    solucion_bidir = resultado_bidir[0]

    if solucion_bidir is not None:

        camino_bidir, acciones_bidir = obtener_datos_solucion(
            solucion_bidir
        )

        dibujo_bidir = dibujar_camino(
            FILAS,
            COLUMNAS,
            camino_bidir
        )

        print("\nBIDIRECCIONAL - SOLUCIÓN")
        print(dibujo_bidir)

        salida_total += (
            "\nBIDIRECCIONAL - SOLUCIÓN\n"
            + dibujo_bidir
        )

    # ==========================================
    # COMPARAR CAMINOS
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

        if solucion is None:
            continue

        nodos_expandidos = resultado[1]

        camino, acciones = obtener_datos_solucion(
            solucion
        )

        longitud = len(camino) - 1

        soluciones.append(
            (
                longitud,
                nombre,
                camino,
                acciones,
                tiempo,
                nodos_expandidos
            )
        )

    # ==========================================
    # CAMINO MÁS CORTO
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

        # Si hay empate en longitud,
        # elegimos el que tarda menos.

        mejor = min(
            mejores,
            key=lambda x: x[4]
        )

        (
            longitud,
            nombre,
            camino,
            acciones,
            tiempo,
            nodos_expandidos
        ) = mejor

        resumen = (
            "\n======================================\n"
            "          CAMINO MÁS CORTO\n"
            "======================================\n"
            f"Método de búsqueda: {nombre}\n"
            f"Camino: {camino}\n"
            f"Acciones: {acciones}\n"
            f"Longitud: {longitud}\n"
            f"Tiempo: {tiempo} segundos\n"
            f"Nodos expandidos: {nodos_expandidos}\n"
            "======================================\n"
        )

        print(resumen)

        salida_total += resumen

        # ======================================
        # DIBUJO DEL MEJOR CAMINO
        # ======================================

        dibujo_mejor = dibujar_camino(
            FILAS,
            COLUMNAS,
            camino
        )

        print("DIBUJO DEL CAMINO MÁS CORTO")
        print(dibujo_mejor)

        salida_total += (
            "\nDIBUJO DEL CAMINO MÁS CORTO\n"
            + dibujo_mejor
        )

    else:

        resumen = (
            "\n======================================\n"
            "       NO SE ENCONTRÓ SOLUCIÓN\n"
            "======================================\n"
        )

        print(resumen)

        salida_total += resumen

    # ==========================================
    # GUARDAR TODO
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