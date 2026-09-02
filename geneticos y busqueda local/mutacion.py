# mutacion.py

import random

from configuracion import (
    PROB_MUTACION,
    ANCHO,
    LARGO,
    POTENCIAS,
    NUM_FOCOS
)


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


def mutar(individuo):

    individuo = individuo.copy()

    for i in range(NUM_FOCOS):

        # ==================================
        # MUTAR X
        # ==================================

        if experimento_mutacion() == 1:

            individuo[
                i * 3
            ] = random.uniform(
                0,
                ANCHO
            )

        # ==================================
        # MUTAR Y
        # ==================================

        if experimento_mutacion() == 1:

            individuo[
                i * 3 + 1
            ] = random.uniform(
                0,
                LARGO
            )

        # ==================================
        # MUTAR POTENCIA
        # ==================================

        if experimento_mutacion() == 1:

            individuo[
                i * 3 + 2
            ] = random.choice(
                POTENCIAS
            )

    return individuo