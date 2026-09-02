# iluminacion.py

import numpy as np

from configuracion import (
    ANCHO,
    LARGO,
    A,
    B,
    NUM_FOCOS
)


def calcular_iluminacion(individuo):

    """
    Calcula la iluminación sobre toda
    la superficie de la habitación.

    Las coordenadas de los focos son continuas.
    """

    # ==========================================
    # ESPACIO CONTINUO PARA LA EVALUACIÓN
    # ==========================================

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

    # ==========================================
    # CALCULAR CONTRIBUCIÓN DE CADA FOCO
    # ==========================================

    for i in range(NUM_FOCOS):

        x_foco = individuo[
            i * 3
        ]

        y_foco = individuo[
            i * 3 + 1
        ]

        potencia = individuo[
            i * 3 + 2
        ]

        # ======================================
        # FOCO APAGADO
        # ======================================

        if potencia == 0:
            continue

        # ======================================
        # MODELO GAUSSIANO
        # ======================================

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