import random

from configuracion import TAM_TORNEO


# ============================================================
# SELECCIÓN DE UN PADRE
# ============================================================

def seleccionar_padre(
    poblacion
):

    participantes = random.sample(
        poblacion,
        TAM_TORNEO
    )

    mejor = max(
        participantes,
        key=lambda individuo:
            individuo.fitness.values[0]
    )

    return mejor


# ============================================================
# SELECCIÓN DE PADRES
# ============================================================

def seleccionar_padres(
    poblacion
):

    padres = []

    for _ in range(
        len(poblacion)
    ):

        padre = seleccionar_padre(
            poblacion
        )

        padres.append(
            padre
        )

    return padres