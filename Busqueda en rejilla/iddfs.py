from pila import Pila
from nodo import Nodo


def dfs_limitado(problema, limite):

    raiz = Nodo(problema.inicial)

    pila = Pila()
    pila.apilar((raiz, 0))

    visitados = {problema.inicial}

    nodos_expandidos = 0

    while not pila.esta_vacia():

        nodo, profundidad = pila.desapilar()

        if problema.es_objetivo(nodo.estado):
            return nodo, nodos_expandidos, raiz

        if profundidad == limite:
            continue

        nodos_expandidos += 1

        acciones = problema.acciones(nodo.estado)

        # Mantener el orden original de DFS
        acciones.reverse()

        for accion in acciones:

            nuevo_estado = problema.resultado(
                nodo.estado,
                accion
            )

            if nuevo_estado in visitados:
                continue

            visitados.add(nuevo_estado)

            hijo = Nodo(
                nuevo_estado,
                nodo,
                accion
            )

            nodo.agregar_hijo(hijo)

            pila.apilar(
                (hijo, profundidad + 1)
            )

    return None, nodos_expandidos, raiz


def iddfs(problema):

    nodos_expandidos = 0
    limite = 0

    while True:

        solucion, expandidos, raiz = dfs_limitado(
            problema,
            limite
        )

        nodos_expandidos += expandidos

        if solucion is not None:
            return solucion, nodos_expandidos, raiz

        limite += 1