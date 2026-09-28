# pyrefly: ignore [missing-import]
import skfuzzy as fuzz

from configuracion import (
    UNIVERSOS,
    PARAMETROS_MEMBRESIA
)


# =========================================================
# FUNCIÓN TRAPEZOIDAL
# =========================================================

def crear_trapezoidal(universo, parametros):

    return fuzz.trapmf(
        universo,
        parametros
    )


# =========================================================
# FUNCIÓN TRIANGULAR
# =========================================================

def crear_triangular(universo, parametros):

    return fuzz.trimf(
        universo,
        parametros
    )


# =========================================================
# CREAR TODAS LAS FUNCIONES DE PERTENENCIA
# =========================================================

def crear_funciones_membresia():

    funciones = {}

    for variable, conjuntos in PARAMETROS_MEMBRESIA.items():

        funciones[variable] = {}

        universo = UNIVERSOS[variable]

        for conjunto, parametros in conjuntos.items():

            # Todas las funciones actuales tienen
            # cuatro parámetros [a, b, c, d],
            # por lo tanto se utiliza trapmf.

            funciones[variable][conjunto] = (
                crear_trapezoidal(
                    universo,
                    parametros
                )
            )

    return funciones


# =========================================================
# OBTENER GRADO DE PERTENENCIA
# =========================================================

def obtener_grado(
    variable,
    conjunto,
    valor,
    funciones
):

    universo = UNIVERSOS[variable]

    funcion = funciones[
        variable
    ][
        conjunto
    ]

    return float(
        fuzz.interp_membership(
            universo,
            funcion,
            valor
        )
    )
