# iluminacion.py

import numpy as np

from configuracion import (
    ANCHO,
    LARGO,
    A,
    B,
    NUM_FOCOS,
    NUM_COLUMNAS
)


# ==========================================
# CUADRÍCULA → COORDENADAS
# ==========================================

def cuadricula_a_coordenadas(cuadricula):

    # Convertir a índice empezando desde 0

    indice = cuadricula - 1

    # Obtener columna

    columna = (
        indice %
        NUM_COLUMNAS
    )

    # Obtener fila

    fila = (
        indice //
        NUM_COLUMNAS
    )

    # Centro de la cuadrícula

    x = columna + 0.5

    y = fila + 0.5

    return x, y


# ==========================================
# CALCULAR ILUMINACIÓN
# ==========================================

def calcular_iluminacion(individuo):

    # ======================================
    # MALLA DE EVALUACIÓN
    # ======================================

    x = np.linspace(
        0,
        ANCHO,
        140
    )

    y = np.linspace(
        0,
        LARGO,
        160
    )

    X, Y = np.meshgrid(
        x,
        y
    )

    iluminacion = np.zeros_like(
        X,
        dtype=float
    )

    # ======================================
    # CALCULAR CADA FOCO
    # ======================================

    for i in range(NUM_FOCOS):

        cuadricula = individuo[
            i * 2
        ]

        potencia = individuo[
            i * 2 + 1
        ]

        # Obtener centro de la cuadrícula

        x_foco, y_foco = (
            cuadricula_a_coordenadas(
                cuadricula
            )
        )

        # ==================================
        # FOCO APAGADO
        # ==================================

        if potencia == 0:

            continue

        # ==================================
        # MODELO GAUSSIANO
        # ==================================

        iluminacion += (
            potencia *
            np.exp(
                -(
                    ((X - x_foco) ** 2)
                    / (A ** 2)
                    +
                    ((Y - y_foco) ** 2)
                    / (B ** 2)
                )
            )
        )

    return iluminacion