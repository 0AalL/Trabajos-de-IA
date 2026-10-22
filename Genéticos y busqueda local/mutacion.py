# mutacion.py

import random

from configuracion import (
    PROB_MUTACION,
    POTENCIAS,
    NUM_FOCOS,
    NUM_CUADRICULAS
)


# ==========================================
# EXPERIMENTO DE MUTACIÓN
# ==========================================

def experimento_mutacion():

    numero = random.randint(
        1,
        100
    )

    limite = round(
        PROB_MUTACION * 100
    )

    if numero <= limite:

        return 1

    return 0


# ==========================================
# MUTAR INDIVIDUO
# ==========================================

def mutar(individuo):

    individuo = individuo.copy()

    # ======================================
    # RECORRER LOS FOCOS
    # ======================================

    for i in range(NUM_FOCOS):

        # ==================================
        # MUTAR CUADRÍCULA
        # ==================================

        if experimento_mutacion() == 1:

            cuadriculas_usadas = {
                individuo[j * 2]
                for j in range(NUM_FOCOS)
                if j != i
            }

            disponibles = [
                cuadricula
                for cuadricula in range(
                    1,
                    NUM_CUADRICULAS + 1
                )
                if cuadricula
                not in cuadriculas_usadas
            ]

            if disponibles:

                individuo[i * 2] = (
                    random.choice(
                        disponibles
                    )
                )

        # ==================================
        # MUTAR POTENCIA
        # ==================================

        if experimento_mutacion() == 1:

            individuo[i * 2 + 1] = (
                random.choice(
                    POTENCIAS
                )
            )

    return individuo