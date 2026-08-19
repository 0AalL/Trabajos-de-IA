from imprimir_arbol import imprimir_arbol


def obtener_camino(nodo):

    return nodo.obtener_camino()


def obtener_acciones_camino(nodo):

    acciones = []

    while nodo.padre is not None:

        acciones.append(nodo.accion)
        nodo = nodo.padre

    acciones.reverse()

    return acciones


def obtener_datos_solucion(solucion):

    if isinstance(solucion, list):

        camino = solucion
        acciones = []

    else:

        camino = obtener_camino(solucion)
        acciones = obtener_acciones_camino(solucion)

    return camino, acciones


def mostrar_resultado(
    nombre,
    resultado,
    es_bidireccional=False,
    profundidad_consola=15,
    mostrar_arbol=True
):

    salida = ""
    salida_consola = ""

    # ==========================================
    # DATOS DEL RESULTADO
    # ==========================================

    if es_bidireccional:

        # Búsqueda bidireccional:
        #
        # 4 elementos:
        # solucion, nodos_expandidos, raiz_inicio, raiz_objetivo
        #
        # 3 elementos:
        # solucion, nodos_expandidos, raiz

        if len(resultado) == 4:

            solucion, nodos_expandidos, raiz_inicio, raiz_objetivo = resultado

            tipo_arbol = "dos"

        else:

            solucion, nodos_expandidos, raiz = resultado

            tipo_arbol = "uno"

    else:

        solucion, nodos_expandidos, raiz = resultado

        tipo_arbol = "uno"

    cabecera = (
        "\n==============================\n"
        + nombre
        + "\n==============================\n"
    )

    salida += cabecera
    salida_consola += cabecera

    # ==========================================
    # SIN SOLUCIÓN
    # ==========================================

    if solucion is None:

        salida += "No se encontró solución.\n"
        salida_consola += "No se encontró solución.\n"

        if not mostrar_arbol:
            return salida, salida_consola

        # ==========================================
        # BIDIRECCIONAL CON DOS ÁRBOLES
        # ==========================================

        if es_bidireccional and tipo_arbol == "dos":

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

        # ==========================================
        # BIDIRECCIONAL CON UN SOLO ÁRBOL
        # ==========================================

        elif es_bidireccional and tipo_arbol == "uno":

            salida += "\nÁRBOL DE BÚSQUEDA:\n"
            salida += imprimir_arbol(raiz)

            salida_consola += (
                "\nÁRBOL DE BÚSQUEDA "
                f"(primeros {profundidad_consola} niveles):\n"
            )

            salida_consola += imprimir_arbol(
                raiz,
                profundidad_maxima=profundidad_consola
            )

        # ==========================================
        # BÚSQUEDA NORMAL
        # ==========================================

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
    # SOLUCIÓN
    # ==========================================

    camino, acciones = obtener_datos_solucion(solucion)

    datos = ""

    datos += "Camino:\n"
    datos += str(camino) + "\n"

    datos += "Acciones:\n"
    datos += str(acciones) + "\n"

    datos += "Longitud:\n"
    datos += str(len(camino) - 1) + "\n"

    datos += "Nodos expandidos:\n"
    datos += str(nodos_expandidos) + "\n"

    salida += datos
    salida_consola += datos

    # ==========================================
    # SIN ÁRBOL
    # ==========================================

    if not mostrar_arbol:

        return salida, salida_consola

    # ==========================================
    # BIDIRECCIONAL CON DOS ÁRBOLES
    # ==========================================

    if es_bidireccional and tipo_arbol == "dos":

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

    # ==========================================
    # BIDIRECCIONAL CON UN SOLO ÁRBOL
    # ==========================================

    elif es_bidireccional and tipo_arbol == "uno":

        salida += "\nÁRBOL DE BÚSQUEDA:\n"
        salida += imprimir_arbol(raiz)

        salida_consola += (
            "\nÁRBOL DE BÚSQUEDA "
            f"(primeros {profundidad_consola} niveles):\n"
        )

        salida_consola += imprimir_arbol(
            raiz,
            profundidad_maxima=profundidad_consola
        )

    # ==========================================
    # BÚSQUEDA NORMAL
    # ==========================================

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