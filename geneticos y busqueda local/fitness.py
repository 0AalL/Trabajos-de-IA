# fitness.py

import numpy as np

from configuracion import (
    ILUMINACION_MINIMA,
    PESO_COBERTURA,
    PESO_COSTO,
    POTENCIAS,
    NUM_FOCOS
)

from iluminacion import calcular_iluminacion


def calcular_fitness(individuo):

    # ==========================================
    # CALCULAR ILUMINACIÓN
    # ==========================================

    iluminacion = calcular_iluminacion(
        individuo
    )

    # ==========================================
    # COBERTURA
    # ==========================================

    puntos_buenos = np.sum(
        iluminacion >= ILUMINACION_MINIMA
    )

    puntos_totales = iluminacion.size

    cobertura = (
        puntos_buenos /
        puntos_totales
    )

    # ==========================================
    # COSTO
    # ==========================================

    potencia_total = 0

    for i in range(NUM_FOCOS):

        potencia = individuo[
            i * 3 + 2
        ]

        potencia_total += potencia

    # ==========================================
    # POTENCIA MÁXIMA
    # ==========================================

    potencia_maxima = (
        NUM_FOCOS *
        max(POTENCIAS)
    )

    costo_normalizado = (
        potencia_total /
        potencia_maxima
    )

    # ==========================================
    # FITNESS
    # ==========================================

    fitness = (
        PESO_COBERTURA * cobertura
        +
        PESO_COSTO * (
            1 - costo_normalizado
        )
    )

    return fitness