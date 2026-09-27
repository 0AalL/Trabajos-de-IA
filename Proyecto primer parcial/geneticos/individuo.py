import random

from deap import base, creator

from configuracion import (
    VARIABLES_ENTRADA,
    VARIABLE_SALIDA,
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

        # ====================================================
        # ANTECEDENTES
        #
        # Se crea un gen por cada variable de entrada.
        #
        # Actualmente:
        #
        # 1. T_mean
        # 2. RH_mean
        # 3. Wind_mean
        # 4. PPT_tot
        # 5. FFMC
        # 6. DMC
        # 7. DC
        # 8. KBDI
        #
        # Cada gen puede tomar uno de los conjuntos fuzzy
        # de su variable o NO_USAR.
        # ====================================================

        for variable in VARIABLES_ENTRADA:

            opciones = (
                CONJUNTOS[variable]
                + [NO_USAR]
            )

            genes.append(
                random.choice(opciones)
            )


        # ====================================================
        # CONSECUENTE
        #
        # La salida es:
        #
        # Area Burned (Ha)
        #
        # Se utiliza VARIABLE_SALIDA para evitar nombres
        # escritos directamente como "incendio".
        # ====================================================

        genes.append(
            random.choice(
                CONJUNTOS[VARIABLE_SALIDA]
            )
        )


        # ====================================================
        # NO PERMITIR REGLA VACÍA
        #
        # Al menos uno de los antecedentes debe utilizarse.
        #
        # El último gen corresponde al consecuente, por eso
        # solamente se revisan genes[:-1].
        # ====================================================

        if any(
            gen != NO_USAR
            for gen in genes[:-1]
        ):

            return creator.Regla(
                genes
            )
