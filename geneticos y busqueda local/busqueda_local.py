# busqueda_local.py

import random
from copy import deepcopy

from individuo import crear_individuo
from fitness import calcular_fitness
from configuracion import (
    NUM_FOCOS,
    NUM_CUADRICULAS,
    POTENCIAS
)


def vecinos(individuo):
    vecs = []

    # Solo 2 focos aleatorios para mover
    indices_focos = random.sample(range(NUM_FOCOS), k=min(2, NUM_FOCOS))

    for i in indices_focos:
        actual = individuo[i * 2]
        usadas = {individuo[j * 2] for j in range(NUM_FOCOS) if j != i}
        disponibles = [c for c in range(1, NUM_CUADRICULAS + 1) if c not in usadas]

        # Solo 3 posiciones candidatas
        for nueva_c in random.sample(disponibles, k=min(3, len(disponibles))):
            if nueva_c != actual:
                v = individuo.copy()
                v[i * 2] = nueva_c
                vecs.append(v)

    # Solo 2 focos aleatorios para potencia
    for i in random.sample(range(NUM_FOCOS), k=min(2, NUM_FOCOS)):
        p_actual = individuo[i * 2 + 1]
        opciones = [p for p in POTENCIAS if p != p_actual]
        for p in random.sample(opciones, k=min(2, len(opciones))):
            v = individuo.copy()
            v[i * 2 + 1] = p
            vecs.append(v)

    return vecs

def hill_climbing(max_iter=300, max_sin_mejora=60):
    actual = crear_individuo()
    f_actual = calcular_fitness(actual)

    mejor = actual.copy()
    f_mejor = f_actual

    sin_mejora = 0
    historial = [f_actual]

    for _ in range(max_iter):
        vecs = vecinos(actual)

        mejor_vecino = None
        f_mejor_vecino = f_actual

        for v in vecs:
            fv = calcular_fitness(v)
            if fv > f_mejor_vecino:
                f_mejor_vecino = fv
                mejor_vecino = v

        if mejor_vecino is None:
            sin_mejora += 1
        else:
            actual = mejor_vecino
            f_actual = f_mejor_vecino
            sin_mejora = 0

            if f_actual > f_mejor:
                mejor = actual.copy()
                f_mejor = f_actual

        historial.append(f_mejor)

        if sin_mejora >= max_sin_mejora:
            break

    return mejor, f_mejor, historial


def busqueda_local_con_reinicios(reinicios=20, max_iter=300, max_sin_mejora=60):
    mejor_global = None
    f_global = float("-inf")
    mejor_historial = []

    for _ in range(reinicios):
        sol, fit, hist = hill_climbing(max_iter=max_iter, max_sin_mejora=max_sin_mejora)
        if fit > f_global:
            mejor_global = sol
            f_global = fit
            mejor_historial = hist

    return mejor_global, f_global, mejor_historial