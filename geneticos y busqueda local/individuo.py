# individuo.py

import random

from configuracion import (
    ANCHO,
    LARGO,
    POTENCIAS,
    NUM_FOCOS
)


# ==========================================
# GENERAR COORDENADA X
# ==========================================

def obtener_x():

    return random.uniform(
        0,
        ANCHO
    )


# ==========================================
# GENERAR COORDENADA Y
# ==========================================

def obtener_y():

    return random.uniform(
        0,
        LARGO
    )


# ==========================================
# GENERAR POTENCIA
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

    for _ in range(NUM_FOCOS):

        x = obtener_x()

        y = obtener_y()

        potencia = obtener_potencia()

        individuo.extend([
            x,
            y,
            potencia
        ])

    return individuo