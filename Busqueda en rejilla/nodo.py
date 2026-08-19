class Nodo:

    _ACCIONES_OPUESTAS = {
        "ARRIBA": "ABAJO",
        "ABAJO": "ARRIBA",
        "IZQUIERDA": "DERECHA",
        "DERECHA": "IZQUIERDA",
    }

    def __init__(
        self,
        estado,
        padre=None,
        accion=None,
        profundidad=0
    ):
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.hijos = []
        self.profundidad = profundidad

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def obtener_camino(self):

        camino = []
        nodo = self

        while nodo is not None:
            camino.append(nodo.estado)
            nodo = nodo.padre

        camino.reverse()

        return camino

    def obtener_acciones(self):

        acciones = []
        nodo = self

        while nodo.padre is not None:

            acciones.append(nodo.accion)
            nodo = nodo.padre

        acciones.reverse()

        return acciones

    @staticmethod
    def _accion_contraria_de(accion):

        """
        Devuelve la acción opuesta a la recibida,
        sin depender de ningún nodo en particular.
        Se usa para poder invertir la acción de UN
        nodo y asignarla a OTRO nodo distinto
        (necesario al invertir un camino).
        """

        if accion is None:
            return None

        if accion not in Nodo._ACCIONES_OPUESTAS:
            raise ValueError(
                f"Acción desconocida: {accion}"
            )

        return Nodo._ACCIONES_OPUESTAS[accion]

    def accion_contraria(self):
        return Nodo._accion_contraria_de(self.accion)

    def revertir_camino_desde_nodo(self):

        """
        Invierte el camino desde este nodo
        hasta la raíz, invirtiendo también
        las acciones.

        IMPORTANTE: al invertir un tramo padre -> hijo
        en hijo -> padre, la acción que queda en el
        nuevo hijo (el antiguo padre) es la contraria
        de la acción que TENÍA el antiguo hijo, no la
        contraria de su propia acción original. Por
        eso se arrastra 'accion_pendiente' de una
        iteración a la siguiente, en vez de invertir
        cada nodo con su propia acción.

        Devuelve la antigua raíz (ahora en el otro
        extremo del camino invertido).
        """

        nodo = self
        anterior = None
        accion_pendiente = None

        while nodo is not None:

            # Guardamos el padre y la acción originales
            # antes de modificar el nodo.
            siguiente = nodo.padre
            accion_original = nodo.accion

            # Invertimos el enlace padre.
            nodo.padre = anterior

            # La acción de este nodo pasa a ser la
            # contraria de la acción que tenía el nodo
            # anterior (su nuevo hijo en el camino
            # invertido), no la suya propia.
            nodo.accion = Nodo._accion_contraria_de(
                accion_pendiente
            )

            # Lo que este nodo tenía como acción
            # original queda pendiente para el
            # próximo nodo del recorrido.
            accion_pendiente = accion_original

            # Avanzamos.
            anterior = nodo
            nodo = siguiente

        # 'anterior' es ahora la antigua raíz.
        return anterior