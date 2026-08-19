from cola import Cola
from nodo import Nodo


def bidireccional(problema):

    # ==========================================
    # RAÍCES
    # ==========================================

    raiz_inicial = Nodo(problema.inicial)
    raiz_objetivo = Nodo(problema.objetivo)

    # ==========================================
    # COLAS
    # ==========================================

    cola_inicial = Cola()
    cola_inicial.encolar(raiz_inicial)

    cola_objetivo = Cola()
    cola_objetivo.encolar(raiz_objetivo)

    # ==========================================
    # VISITADOS
    # ==========================================

    visitados_inicial = {problema.inicial}
    visitados_objetivo = {problema.objetivo}

    # ==========================================
    # NODOS VISITADOS
    # ==========================================

    nodos_inicial = {
        problema.inicial: raiz_inicial
    }

    nodos_objetivo = {
        problema.objetivo: raiz_objetivo
    }

    nodos_expandidos = 0

    # ==========================================
    # BÚSQUEDA
    # ==========================================

    while (
        not cola_inicial.esta_vacia()
        and not cola_objetivo.esta_vacia()
    ):

        # ==========================================
        # EXPANDIR DESDE EL INICIO
        # ==========================================

        resultado = expandir(
            problema,
            cola_inicial,
            visitados_inicial,
            nodos_inicial,
            visitados_objetivo,
            nodos_objetivo
        )

        nodos_expandidos += 1

        if resultado is not None:

            nodo_inicio, nodo_objetivo = resultado

            solucion = construir_solucion(
                nodo_inicio,
                nodo_objetivo
            )

            return (
                solucion,
                nodos_expandidos,
                raiz_inicial,
                raiz_objetivo
            )

        # ==========================================
        # EXPANDIR DESDE EL OBJETIVO
        # ==========================================

        resultado = expandir(
            problema,
            cola_objetivo,
            visitados_objetivo,
            nodos_objetivo,
            visitados_inicial,
            nodos_inicial
        )

        nodos_expandidos += 1

        if resultado is not None:

            nodo_objetivo, nodo_inicio = resultado

            solucion = construir_solucion(
                nodo_inicio,
                nodo_objetivo
            )

            return (
                solucion,
                nodos_expandidos,
                raiz_inicial,
                raiz_objetivo
            )

    # ==========================================
    # NO HAY SOLUCIÓN
    # ==========================================

    return (
        None,
        nodos_expandidos,
        raiz_inicial,
        raiz_objetivo
    )


def expandir(
    problema,
    cola,
    visitados_actual,
    nodos_actual,
    visitados_otro,
    nodos_otro
):

    if cola.esta_vacia():
        return None

    nodo = cola.desencolar()

    # ==========================================
    # GENERAR SUCESORES
    # ==========================================

    for accion in problema.acciones(
        nodo.estado
    ):

        nuevo_estado = problema.resultado(
            nodo.estado,
            accion
        )

        # ==========================================
        # ENCUENTRO DE LOS DOS ÁRBOLES
        # ==========================================

        if nuevo_estado in visitados_otro:

            hijo = Nodo(
                nuevo_estado,
                nodo,
                accion
            )

            nodo.agregar_hijo(hijo)

            nodos_actual[nuevo_estado] = hijo

            return (
                hijo,
                nodos_otro[nuevo_estado]
            )

        # ==========================================
        # ESTADO NUEVO
        # ==========================================

        if nuevo_estado not in visitados_actual:

            visitados_actual.add(nuevo_estado)

            hijo = Nodo(
                nuevo_estado,
                nodo,
                accion
            )

            nodo.agregar_hijo(hijo)

            nodos_actual[nuevo_estado] = hijo

            cola.encolar(hijo)

    return None


def construir_solucion(
    nodo_inicio,
    nodo_objetivo
):

    # ==========================================
    # RECORRER EL ÁRBOL DEL OBJETIVO
    # DESDE EL ENCUENTRO HASTA EL OBJETIVO
    # ==========================================

    nodo = nodo_objetivo

    padre = nodo_inicio

    while nodo.padre is not None:

        # La acción almacenada en 'nodo' corresponde
        # al movimiento:
        #
        # nodo.padre -> nodo
        #
        # Pero nosotros necesitamos recorrer:
        #
        # nodo -> nodo.padre
        #
        # Por eso usamos la acción contraria.

        accion = Nodo._accion_contraria_de(
            nodo.accion
        )

        hijo = Nodo(
            nodo.padre.estado,
            padre,
            accion
        )

        padre.agregar_hijo(hijo)

        padre = hijo
        nodo = nodo.padre

    return padre