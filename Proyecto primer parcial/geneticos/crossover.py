import random
import copy

from configuracion import PROB_CRUCE


# ============================================================
# CROSSOVER DE DOS PADRES
# ============================================================

def crossover(
    padre1,
    padre2,
    consecuente_fijo=None
):

    hijo1 = copy.deepcopy(
        padre1
    )

    hijo2 = copy.deepcopy(
        padre2
    )

    if random.random() < PROB_CRUCE:

        punto = random.randint(
            1,
            len(padre1) - 1
        )

        hijo1[punto:], hijo2[punto:] = (
            hijo2[punto:],
            hijo1[punto:]
        )

    if consecuente_fijo is not None:
        hijo1[-1] = consecuente_fijo
        hijo2[-1] = consecuente_fijo

    # El fitness anterior ya no es válido
    if hijo1.fitness.valid:

        del hijo1.fitness.values

    if hijo2.fitness.valid:

        del hijo2.fitness.values

    return hijo1, hijo2


# ============================================================
# CROSSOVER DE TODA LA POBLACIÓN
# ============================================================

def realizar_crossover(
    padres,
    consecuente_fijo=None
):

    hijos = []

    for i in range(
        0,
        len(padres),
        2
    ):

        padre1 = padres[i]

        if i + 1 < len(padres):

            padre2 = padres[i + 1]

        else:

            padre2 = padres[0]

        hijo1, hijo2 = crossover(
            padre1,
            padre2,
            consecuente_fijo=consecuente_fijo
        )

        hijos.append(
            hijo1
        )

        hijos.append(
            hijo2
        )

    return hijos