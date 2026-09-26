from funciones_membresia import (
    obtener_grado,
    crear_funciones_membresia
)

from configuracion import (
    CONJUNTOS
)


# =========================================================
# CREAR FUNCIONES
# =========================================================

FUNCIONES = crear_funciones_membresia()


# =========================================================
# FUZZIFICAR UNA VARIABLE
# =========================================================

def fuzzificar_variable(
    variable,
    valor
):

    grados = {}

    for conjunto in CONJUNTOS[variable]:

        grados[conjunto] = obtener_grado(
            variable,
            conjunto,
            valor,
            FUNCIONES
        )

    return grados


# =========================================================
# FUZZIFICAR TODAS LAS ENTRADAS
# =========================================================

def fuzzificar_entradas(entradas):

    resultado = {}

    for variable, valor in entradas.items():

        resultado[variable] = (
            fuzzificar_variable(
                variable,
                valor
            )
        )

    return resultado


# =========================================================
# CONJUNTO DOMINANTE
# =========================================================

def obtener_dominante(grados):

    if not grados:
        return None

    return max(
        grados,
        key=grados.get
    )


# =========================================================
# OBTENER DOMINANTES DE TODAS LAS VARIABLES
# =========================================================

def obtener_dominantes(fuzzificados):

    resultado = {}

    for variable, grados in fuzzificados.items():

        resultado[variable] = obtener_dominante(
            grados
        )

    return resultado