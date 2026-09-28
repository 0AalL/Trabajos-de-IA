import random

# pyrefly: ignore [missing-import]
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

def crear_individuo(
    consecuente_fijo=None
):

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
        # Si se especifica un consecuente fijo (para nichos/
        # multiclase), se utiliza ese valor. Si no, se elige al azar.
        # ====================================================

        if consecuente_fijo is not None:

            genes.append(
                consecuente_fijo
            )

        else:

            genes.append(
                random.choice(
                    CONJUNTOS[VARIABLE_SALIDA]
                )
            )


        # ====================================================
        # NO PERMITIR REGLA TRIVIAL O VACÍA
        #
        # Al menos dos de los antecedentes deben utilizarse
        # para que la regla sea contextual y no degenerada.
        # ====================================================

        if sum(1 for gen in genes[:-1] if gen != NO_USAR) >= 2:

            return creator.Regla(
                genes
            )
