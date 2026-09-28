import random

from configuracion import (
    VARIABLES_ENTRADA,
    VARIABLE_SALIDA,
    CONJUNTOS,
    NO_USAR,
    PROB_MUTACION
)


# ============================================================
# MUTACIÓN DE UN INDIVIDUO
# ============================================================

def mutar_individuo(
    individuo,
    consecuente_fijo=None
):

    # --------------------------------------------------------
    # Genes de entrada
    # --------------------------------------------------------

    for i, variable in enumerate(
        VARIABLES_ENTRADA
    ):

        if random.random() < PROB_MUTACION:

            opciones = (
                CONJUNTOS[variable]
                + [NO_USAR]
            )

            individuo[i] = random.choice(
                opciones
            )

    # --------------------------------------------------------
    # Consecuente
    # --------------------------------------------------------

    indice_salida = len(
        VARIABLES_ENTRADA
    )

    if consecuente_fijo is not None:

        individuo[indice_salida] = consecuente_fijo

    elif random.random() < PROB_MUTACION:

        individuo[indice_salida] = random.choice(
            CONJUNTOS[VARIABLE_SALIDA]
        )

    # --------------------------------------------------------
    # Evitar antecedente completamente vacío
    # --------------------------------------------------------

    if all(
        gen == NO_USAR
        for gen in individuo[:-1]
    ):

        indice = random.randrange(
            len(VARIABLES_ENTRADA)
        )

        variable = VARIABLES_ENTRADA[
            indice
        ]

        individuo[indice] = random.choice(
            CONJUNTOS[variable]
        )

    # --------------------------------------------------------
    # Invalidar fitness
    # --------------------------------------------------------

    if individuo.fitness.valid:

        del individuo.fitness.values

    return individuo


# ============================================================
# MUTACIÓN DE LOS HIJOS
# ============================================================

def realizar_mutacion(
    hijos,
    consecuente_fijo=None
):

    for hijo in hijos:

        mutar_individuo(
            hijo,
            consecuente_fijo=consecuente_fijo
        )

    return hijos
