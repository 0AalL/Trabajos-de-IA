# crossover.py

import random

from configuracion import (
    ANCHO,
    LARGO,
    POTENCIAS
)


def experimento_100():

    vector = list(range(1, 101))

    numero = random.randint(1, 100)

    return vector[numero - 1]


def crossover(padre1, padre2):

    hijo1 = []
    hijo2 = []

    for i in range(0, len(padre1), 3):

        # ==================================
        # PORCENTAJE ALEATORIO
        # ==================================

        numero = experimento_100()

        p = numero / 100.0

        # ==================================
        # COORDENADA X
        # ==================================

        x1 = (
            p * padre1[i]
            +
            (1 - p) * padre2[i]
        )

        x2 = (
            (1 - p) * padre1[i]
            +
            p * padre2[i]
        )

        # ==================================
        # COORDENADA Y
        # ==================================

        y1 = (
            p * padre1[i + 1]
            +
            (1 - p) * padre2[i + 1]
        )

        y2 = (
            (1 - p) * padre1[i + 1]
            +
            p * padre2[i + 1]
        )

        # ==================================
        # LIMITAR AL ESPACIO
        # ==================================

        x1 = max(0, min(ANCHO, x1))
        x2 = max(0, min(ANCHO, x2))

        y1 = max(0, min(LARGO, y1))
        y2 = max(0, min(LARGO, y2))

        # ==================================
        # POTENCIA
        # ==================================
        # Se selecciona una potencia válida.
        # Puede ser 0 = foco apagado.

        potencia_padre1 = padre1[i + 2]
        potencia_padre2 = padre2[i + 2]

        potencia1 = random.choice([
            potencia_padre1,
            potencia_padre2
        ])

        potencia2 = random.choice([
            potencia_padre1,
            potencia_padre2
        ])

        # ==================================
        # AGREGAR HIJOS
        # ==================================

        hijo1.extend([
            x1,
            y1,
            potencia1
        ])

        hijo2.extend([
            x2,
            y2,
            potencia2
        ])

    return hijo1, hijo2