# individuo.py

import random

from configuracion import (
    POTENCIAS,
    NUM_FOCOS,
    NUM_CUADRICULAS
)


# ==========================================
# OBTENER CUADRÍCULA DISPONIBLE
# ==========================================

def obtener_cuadricula(cuadriculas_usadas):

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
# OBTENER POTENCIA
# ==========================================

def obtener_potencia():

    return random.choice(
        POTENCIAS
    )


# ==========================================
# CREAR INDIVIDUO
# ==========================================

def crear_individuo():

    individuo = []

    cuadriculas_usadas = set()

    for _ in range(NUM_FOCOS):

        cuadricula = obtener_cuadricula(
            cuadriculas_usadas
        )

        cuadriculas_usadas.add(
            cuadricula
        )

        potencia = obtener_potencia()

        individuo.extend([
            cuadricula,
            potencia
        ])

    return individuo