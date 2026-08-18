from cola import Cola
from nodo import Nodo


def bfs(problema):

    raiz = Nodo(problema.inicial)

    cola = Cola()
    cola.encolar(raiz)

    visitados = {problema.inicial}

    nodos_expandidos = 0

    while not cola.esta_vacia():

        nodo = cola.desencolar()

        if problema.es_objetivo(nodo.estado):
            return nodo, nodos_expandidos, raiz

        nodos_expandidos += 1

        for accion in problema.acciones(nodo.estado):

            nuevo_estado = problema.resultado(
                nodo.estado,
                accion
            )

            if nuevo_estado not in visitados:

                visitados.add(nuevo_estado)

                hijo = Nodo(
                    nuevo_estado,
                    nodo,
                    accion
                )

                nodo.agregar_hijo(hijo)

                cola.encolar(hijo)

    return None, nodos_expandidos, raiz