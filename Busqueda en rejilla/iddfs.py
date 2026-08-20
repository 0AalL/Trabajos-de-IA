from pila import Pila
from nodo import Nodo


def dfs_limitado(problema, limite):

    raiz = Nodo(problema.inicial)

    pila = Pila()
    pila.apilar((raiz, 0))

    # Estado -> menor profundidad conocida
    visitados = {
        problema.inicial: 0
    }

    nodos_expandidos = 0

    while not pila.esta_vacia():

        nodo, profundidad = pila.desapilar()

        if problema.es_objetivo(nodo.estado):
            return nodo, nodos_expandidos, raiz

        if profundidad == limite:
            continue

        nodos_expandidos += 1

        acciones = problema.acciones(nodo.estado)

        acciones.reverse()

        for accion in acciones:

            nuevo_estado = problema.resultado(
                nodo.estado,
                accion
            )

            nueva_profundidad = profundidad + 1

            # Si ya llegamos a este estado a una profundidad
            # menor o igual, no necesitamos volver a explorarlo.
            if (nuevo_estado in visitados and
                    visitados[nuevo_estado] <= nueva_profundidad):
                continue

            visitados[nuevo_estado] = nueva_profundidad

            hijo = Nodo(
                nuevo_estado,
                nodo,
                accion
            )

            nodo.agregar_hijo(hijo)

            pila.apilar(
                (hijo, nueva_profundidad)
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