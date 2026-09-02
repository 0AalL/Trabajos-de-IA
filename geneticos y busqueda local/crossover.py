# crossover.py

import random

from configuracion import (
    NUM_CUADRICULAS
)


# ==========================================
# OBTENER CUADRÍCULA DISPONIBLE
# ==========================================

def obtener_cuadricula_disponible(
    cuadriculas_usadas
):

    disponibles = [
        cuadricula
        for cuadricula in range(
            1,
            NUM_CUADRICULAS + 1
        )
        if cuadricula not in cuadriculas_usadas
    ]

    return random.choice(disponibles)


# ==========================================
# CROSSOVER
# ==========================================

def crossover(padre1, padre2):

    hijo1 = []
    hijo2 = []

    cuadriculas_hijo1 = set()
    cuadriculas_hijo2 = set()

    # ======================================
    # RECORRER LOS FOCOS
    # ======================================

    for i in range(0, len(padre1), 2):

        # ==================================
        # CUADRÍCULA DEL PADRE 1
        # ==================================

        cuadricula_padre1 = padre1[i]

        # ==================================
        # CUADRÍCULA DEL PADRE 2
        # ==================================

        cuadricula_padre2 = padre2[i]

        # ==================================
        # ELEGIR CUADRÍCULA PARA HIJO 1
        # ==================================

        if random.random() < 0.5:

            cuadricula1 = cuadricula_padre1

        else:

            cuadricula1 = cuadricula_padre2

        # ==================================
        # EVITAR DUPLICADOS EN HIJO 1
        # ==================================

        if cuadricula1 in cuadriculas_hijo1:

            cuadricula1 = (
                obtener_cuadricula_disponible(
                    cuadriculas_hijo1
                )
            )

        cuadriculas_hijo1.add(
            cuadricula1
        )

        # ==================================
        # ELEGIR CUADRÍCULA PARA HIJO 2
        # ==================================

        if random.random() < 0.5:

            cuadricula2 = cuadricula_padre1

        else:

            cuadricula2 = cuadricula_padre2

        # ==================================
        # EVITAR DUPLICADOS EN HIJO 2
        # ==================================

        if cuadricula2 in cuadriculas_hijo2:

            cuadricula2 = (
                obtener_cuadricula_disponible(
                    cuadriculas_hijo2
                )
            )

        cuadriculas_hijo2.add(
            cuadricula2
        )

        # ==================================
        # POTENCIAS
        # ==================================

        potencia_padre1 = padre1[i + 1]

        potencia_padre2 = padre2[i + 1]

        potencia1 = random.choice([
            potencia_padre1,
            potencia_padre2
        ])

        potencia2 = random.choice([
            potencia_padre1,
            potencia_padre2
        ])

        # ==================================
        # CONSTRUIR HIJO 1
        # ==================================

        hijo1.extend([
            cuadricula1,
            potencia1
        ])

        # ==================================
        # CONSTRUIR HIJO 2
        # ==================================

        hijo2.extend([
            cuadricula2,
            potencia2
        ])

    return hijo1, hijo2