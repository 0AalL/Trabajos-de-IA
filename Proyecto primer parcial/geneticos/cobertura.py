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

        # Comodín
        if gen == NO_USAR:

            continue

        if gen != combinacion[i]:

            return False

    return True


# ============================================================
# COMBINACIONES CUBIERTAS
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
    # 1. GARANTIZAR COMPLETITUD:
    # Asegurar al menos la mejor regla de cada clase de salida
    # --------------------------------------------------------

    clases_vistas = set()

    for regla in reglas:

        consecuente = regla["individuo"][-1]

        if consecuente not in clases_vistas:

            clases_vistas.add(
                consecuente
            )

            reglas_finales.append(
                regla
            )

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

        nuevas = nuevas - cubiertas

        if nuevas:

            reglas_finales.append(
                regla
            )

            cubiertas.update(
                nuevas
            )

        if cubiertas == todas:

            break

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