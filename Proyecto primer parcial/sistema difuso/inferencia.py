# pyrefly: ignore [missing-import]
import numpy as np

from configuracion import (
    UNIVERSOS,
    CONJUNTOS
)

from funciones_membresia import (
    obtener_grado,
    crear_funciones_membresia
)


# =========================================================
# FUNCIONES DE PERTENENCIA
# =========================================================

FUNCIONES = crear_funciones_membresia()


# =========================================================
# EVALUAR ANTECEDENTE
# =========================================================

def evaluar_antecedente(
    regla,
    fuzzificados
):

    grados = []

    for variable in fuzzificados:

        conjunto = regla[
            "condiciones"
        ][
            variable
        ]

        # ---------------------------------------------
        # NO_USAR = comodín
        # ---------------------------------------------

        if conjunto == "NO_USAR":

            continue

        grado = fuzzificados[
            variable
        ][
            conjunto
        ]

        grados.append(
            grado
        )

    # ---------------------------------------------
    # Si no hay antecedentes
    # ---------------------------------------------

    if not grados:

        return 0.0

    # ---------------------------------------------
    # AND = MIN
    # ---------------------------------------------

    return min(
        grados
    )


# =========================================================
# EVALUAR REGLAS
# =========================================================

def evaluar_reglas(
    reglas,
    fuzzificados
):

    activaciones = []

    for regla in reglas:

        activacion = evaluar_antecedente(
            regla,
            fuzzificados
        )

        activaciones.append(
            {
                "numero": regla["numero"],

                "regla": regla,

                "activacion": activacion
            }
        )

    return activaciones


# =========================================================
# AGREGAR SALIDAS
# =========================================================

def agregar_salidas(
    reglas,
    activaciones
):

    universo = UNIVERSOS[
        "Area Quemada (Ha)"
    ]

    salida_agregada = np.zeros(
        len(universo)
    )

    for elemento in activaciones:

        activacion = elemento[
            "activacion"
        ]

        regla = elemento[
            "regla"
        ]

        consecuente = regla[
            "consecuente"
        ]

        funcion_salida = FUNCIONES[
            "Area Quemada (Ha)"
        ][
            consecuente
        ]

        # ---------------------------------------------
        # IMPLICACIÓN = MIN
        # ---------------------------------------------

        salida_regla = np.fmin(
            activacion,
            funcion_salida
        )

        # ---------------------------------------------
        # AGREGACIÓN = MAX
        # ---------------------------------------------

        salida_agregada = np.fmax(
            salida_agregada,
            salida_regla
        )

    return universo, salida_agregada