from pila import Pila
from nodo import Nodo


def dfs(problema):

    raiz = Nodo(problema.inicial)

    pila = Pila()
    pila.apilar(raiz)

    visitados = {problema.inicial}

    nodos_expandidos = 0

    while not pila.esta_vacia():

        nodo = pila.desapilar()

        if problema.es_objetivo(nodo.estado):
            return nodo, nodos_expandidos, raiz

        nodos_expandidos += 1

        acciones = problema.acciones(nodo.estado)

        # Invertimos para mantener el orden de expansión
        acciones.reverse()

        for accion in acciones:

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

                pila.apilar(hijo)

    return None, nodos_expandidos, raiz