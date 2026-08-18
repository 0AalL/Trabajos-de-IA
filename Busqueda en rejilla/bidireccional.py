from cola import Cola
from nodo import Nodo


def bidireccional(problema):

    nodo_inicial = Nodo(problema.inicial)
    nodo_objetivo = Nodo(problema.objetivo)

    cola_inicial = Cola()
    cola_inicial.encolar(nodo_inicial)

    cola_objetivo = Cola()
    cola_objetivo.encolar(nodo_objetivo)

    visitados_inicial = {
        problema.inicial: nodo_inicial
    }

    visitados_objetivo = {
        problema.objetivo: nodo_objetivo
    }

    nodos_expandidos = 0

    while (
        not cola_inicial.esta_vacia()
        and not cola_objetivo.esta_vacia()
    ):

        # Expandimos un nodo desde el inicio
        resultado = expandir(
            problema,
            cola_inicial,
            visitados_inicial,
            visitados_objetivo
        )

        nodos_expandidos += 1

        if resultado is not None:

            nodo_inicio, nodo_fin = resultado

            camino_inicio = nodo_inicio.obtener_camino()

            camino_fin = nodo_fin.obtener_camino()
            camino_fin.reverse()

            camino = camino_inicio + camino_fin[1:]

            return (
                camino,
                nodos_expandidos,
                nodo_inicial,
                nodo_objetivo
            )

        # Expandimos un nodo desde el objetivo
        resultado = expandir(
            problema,
            cola_objetivo,
            visitados_objetivo,
            visitados_inicial
        )

        nodos_expandidos += 1

        if resultado is not None:

            nodo_fin, nodo_inicio = resultado

            camino_inicio = nodo_inicio.obtener_camino()

            camino_fin = nodo_fin.obtener_camino()
            camino_fin.reverse()

            camino = camino_inicio + camino_fin[1:]

            return (
                camino,
                nodos_expandidos,
                nodo_inicial,
                nodo_objetivo
            )

    return (
        None,
        nodos_expandidos,
        nodo_inicial,
        nodo_objetivo
    )


def expandir(
    problema,
    cola,
    visitados_actual,
    visitados_otro
):

    if cola.esta_vacia():
        return None

    # Sacamos el primero de la cola → BFS
    nodo = cola.desencolar()

    for accion in problema.acciones(nodo.estado):

        nuevo_estado = problema.resultado(
            nodo.estado,
            accion
        )

        # ¿El otro árbol ya llegó a este estado?
        if nuevo_estado in visitados_otro:

            nodo_otro = visitados_otro[nuevo_estado]

            hijo = Nodo(
                nuevo_estado,
                nodo,
                accion
            )

            nodo.agregar_hijo(hijo)

            return hijo, nodo_otro

        # Si este árbol todavía no ha visitado el estado
        if nuevo_estado not in visitados_actual:

            hijo = Nodo(
                nuevo_estado,
                nodo,
                accion
            )

            nodo.agregar_hijo(hijo)

            visitados_actual[nuevo_estado] = hijo

            # Se añade al final → mantiene BFS
            cola.encolar(hijo)

    return None