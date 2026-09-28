from itertools import product

from configuracion import (
    VARIABLES_ENTRADA,
    CONJUNTOS,
    NO_USAR
)


# ============================================================
# GENERAR COMBINACIONES
# ============================================================

def generar_combinaciones_entrada():

    listas = []

    for variable in VARIABLES_ENTRADA:

        listas.append(
            CONJUNTOS[variable]
        )

    return list(
        product(*listas)
    )


# ============================================================
# COMPROBAR COBERTURA
# ============================================================

def regla_cubre_combinacion(
    regla,
    combinacion
):

    for i in range(
        len(VARIABLES_ENTRADA)
    ):

        gen = regla[i]

        # ----------------------------------------------------
        # NO_USAR = COMODÍN
        # ----------------------------------------------------

        if gen == NO_USAR:

            continue

        # ----------------------------------------------------
        # La condición debe coincidir
        # ----------------------------------------------------

        if gen != combinacion[i]:

            return False

    return True


# ============================================================
# COMBINACIONES CUBIERTAS POR REGLA
# ============================================================

def combinaciones_cubiertas_por_regla(
    regla,
    combinaciones
):

    cubiertas = set()

    for indice, combinacion in enumerate(
        combinaciones
    ):

        if regla_cubre_combinacion(
            regla,
            combinacion
        ):

            cubiertas.add(
                indice
            )

    return cubiertas


# ============================================================
# SELECCIÓN POR COBERTURA
# ============================================================

def seleccionar_reglas_por_cobertura(
    reglas
):

    # --------------------------------------------------------
    # Generar todas las combinaciones
    # --------------------------------------------------------

    combinaciones = (
        generar_combinaciones_entrada()
    )

    todas = set(
        range(
            len(combinaciones)
        )
    )

    cubiertas = set()

    reglas_finales = []

    # --------------------------------------------------------
    # IMPORTANTE
    #
    # reglas viene ordenado desde algoritmo_genetico.py:
    #
    #   1. última generación
    #   2. generación anterior
    #   3. generación anterior
    #   ...
    #
    # Por tanto, aquí simplemente seguimos recorriendo
    # hasta conseguir cobertura completa.
    # --------------------------------------------------------

    for regla in reglas:

        nuevas = (
            combinaciones_cubiertas_por_regla(
                regla["individuo"],
                combinaciones
            )
        )

        # ----------------------------------------------------
        # Solo nos interesan las combinaciones que todavía
        # no estaban cubiertas.
        # ----------------------------------------------------

        nuevas = (
            nuevas - cubiertas
        )

        # ----------------------------------------------------
        # Si la regla aporta cobertura nueva, se conserva.
        # ----------------------------------------------------

        if nuevas:

            reglas_finales.append(
                regla
            )

            cubiertas.update(
                nuevas
            )

        # ----------------------------------------------------
        # Si ya cubrimos todo, terminamos.
        # ----------------------------------------------------

        if cubiertas == todas:

            break

    # --------------------------------------------------------
    # Faltantes
    # --------------------------------------------------------

    faltantes = (
        todas - cubiertas
    )

    return (
        reglas_finales,
        combinaciones,
        cubiertas
    )


# ============================================================
# FALTANTES
# ============================================================

def encontrar_combinaciones_faltantes(
    combinaciones,
    cubiertas
):

    todas = set(
        range(
            len(combinaciones)
        )
    )

    faltantes = (
        todas - cubiertas
    )

    return [
        combinaciones[i]
        for i in faltantes
    ]