import random


# ============================================================
# SELECCIÓN POR RULETA PROPORCIONAL AL FITNESS (HOLLAND 1975)
# ============================================================

def seleccionar_padre(
    poblacion
):
    """
    Selecciona un único progenitor mediante Ruleta Proporcional al Fitness.
    """
    return seleccionar_padres(poblacion)[0]


# ============================================================
# SELECCIÓN DE PADRES (FITNESS PROPORTIONATE SELECTION)
# ============================================================

def seleccionar_padres(
    poblacion
):
 
    # --------------------------------------------------------
    # 1. Extraer fitness no negativo de cada individuo
    # --------------------------------------------------------
    pesos = [
        max(0.0, float(individuo.fitness.values[0]))
        if (individuo.fitness.valid and individuo.fitness.values)
        else 0.0
        for individuo in poblacion
    ]

    suma_pesos = sum(pesos)

    # --------------------------------------------------------
    # 2. Salvaguarda de degeneración o fitness nulo
    # --------------------------------------------------------
    # Si la suma es 0 (ej. generación inicial sin evaluar o todos
    # con fitness nulo), la ruleta asigna pesos iguales (equiprobable)
    if suma_pesos <= 0.0:
        pesos = [1.0] * len(poblacion)

    # --------------------------------------------------------
    # 3. Muestreo probabilístico acumulativo (Ruleta)
    # --------------------------------------------------------
    # random.choices implementa internamente la ruleta acumulativa
    # mediante partición de intervalos en O(N) o bisección O(k log N)
    padres = random.choices(
        poblacion,
        weights=pesos,
        k=len(poblacion)
    )

    return padres
