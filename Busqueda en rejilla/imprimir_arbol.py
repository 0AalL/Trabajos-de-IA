def imprimir_arbol(raiz, profundidad_maxima=15):

    lineas = []

    lineas.append("")
    lineas.append("ÁRBOL DE BÚSQUEDA:")
    lineas.append("")

    lineas.append(str(raiz.estado))

    hijos = raiz.hijos

    for i, hijo in enumerate(hijos):

        es_ultimo = (i == len(hijos) - 1)

        agregar_subarbol(
            hijo,
            "",
            es_ultimo,
            lineas,
            1,
            profundidad_maxima
        )

    return "\n".join(lineas)


def agregar_subarbol(
    nodo,
    prefijo,
    es_ultimo,
    lineas,
    profundidad,
    profundidad_maxima
):

    if profundidad_maxima is not None:
        if profundidad > profundidad_maxima:
            return

    if es_ultimo:

        conector = "└── "
        nuevo_prefijo = prefijo + "    "

    else:

        conector = "├── "
        nuevo_prefijo = prefijo + "│   "

    lineas.append(
        prefijo + conector + str(nodo.estado)
    )

    hijos = nodo.hijos

    for i, hijo in enumerate(hijos):

        es_ultimo_hijo = (i == len(hijos) - 1)

        agregar_subarbol(
            hijo,
            nuevo_prefijo,
            es_ultimo_hijo,
            lineas,
            profundidad + 1,
            profundidad_maxima
        )