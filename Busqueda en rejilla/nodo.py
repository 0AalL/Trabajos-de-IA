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
