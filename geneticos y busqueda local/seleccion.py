# seleccion.py

import random


def calcular_probabilidades(fitnesses):

    total = sum(fitnesses)

    if total == 0:

        return [
            1 / len(fitnesses)
            for _ in fitnesses
        ]

    return [
        fitness / total
        for fitness in fitnesses
    ]


def crear_ruleta(probabilidades):

    """

    CREA EL VECTOR DE 100 POSICIONES.

    Cada posición contiene el índice del individuo
    que corresponde a ese porcentaje.

    """

    ruleta = []

    acumulado = 0

    for i, probabilidad in enumerate(probabilidades):

        cantidad = round(probabilidad * 100)

        for _ in range(cantidad):

            ruleta.append(i)

    # Garantizar exactamente 100 posiciones

    while len(ruleta) < 100:

        ruleta.append(ruleta[-1])

    while len(ruleta) > 100:

        ruleta.pop()

    return ruleta


def elegir_individuo(probabilidades):

    ruleta = crear_ruleta(probabilidades)

    # ------------------------------------
    # EXPERIMENTO ALEATORIO
    # ------------------------------------

    numero = random.randint(1, 100)

    # ------------------------------------
    # SELECCIÓN
    # ------------------------------------

    posicion = numero - 1

    return ruleta[posicion]


def seleccionar_padres(poblacion, fitnesses):

    probabilidades = calcular_probabilidades(
        fitnesses
    )

    padre1_index = elegir_individuo(
        probabilidades
    )

    padre2_index = elegir_individuo(
        probabilidades
    )

    padre1 = poblacion[padre1_index].copy()

    padre2 = poblacion[padre2_index].copy()

    return padre1, padre2