import random

from deap import base, creator

from configuracion import (
    VARIABLES_ENTRADA,
    CONJUNTOS,
    NO_USAR
)


# ============================================================
# CREAR TIPOS DE DEAP
# ============================================================

if not hasattr(
    creator,
    "FitnessMax"
):

    creator.create(
        "FitnessMax",
        base.Fitness,
        weights=(1.0,)
    )


if not hasattr(
    creator,
    "Regla"
):

    creator.create(
        "Regla",
        list,
        fitness=creator.FitnessMax
    )


# ============================================================
# CREAR INDIVIDUO
# ============================================================

def crear_individuo():

    while True:

        genes = []

        # 7 antecedentes
        for variable in VARIABLES_ENTRADA:

            opciones = (
                CONJUNTOS[variable]
                + [NO_USAR]
            )

            genes.append(
                random.choice(opciones)
            )

        # Consecuente
        genes.append(
            random.choice(
                CONJUNTOS["incendio"]
            )
        )

        # No permitir regla vacía
        if any(
            gen != NO_USAR
            for gen in genes[:-1]
        ):

            return creator.Regla(
                genes
            )