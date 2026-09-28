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
    reglas,
    min_reglas_por_clase=5
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
    # 1. GARANTIZAR PLURALIDAD Y COMPLETITUD:
    # Asegurar hasta min_reglas_por_clase reglas únicas por
    # cada clase de riesgo para tener una base robusta
    # --------------------------------------------------------

    conteo_por_clase = {}

    for regla in reglas:

        consecuente = regla["individuo"][-1]
        conteo = conteo_por_clase.get(consecuente, 0)

        if conteo < min_reglas_por_clase:

            conteo_por_clase[consecuente] = conteo + 1
            reglas_finales.append(regla)

            nuevas = (
                combinaciones_cubiertas_por_regla(
                    regla["individuo"],
                    combinaciones
                )
            )

            cubiertas.update(
                nuevas
            )

    # --------------------------------------------------------
    # 2. SELECCIÓN AVÁRICA POR COBERTURA:
    # Agregar reglas adicionales que cubran nuevas combinaciones
    # --------------------------------------------------------

    for regla in reglas:

        if regla in reglas_finales:

            continue

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