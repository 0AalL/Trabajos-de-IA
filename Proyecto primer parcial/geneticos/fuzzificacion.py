import pandas as pd

from configuracion import (
    VARIABLES_ENTRADA,
    VARIABLE_SALIDA,
    CONJUNTOS,
    PARAMETROS_MEMBRESIA,
    ARCHIVO_DATASET,
    ARCHIVO_DATASET_FUZZIFICADO
)


# ============================================================
# TRAPEZOIDAL
# ============================================================

def pertenencia_trapezoidal(x, parametros):

    a, b, c, d = parametros

    if x < a or x > d:
        return 0.0

    if a == b and x == a:
        return 1.0

    if a < x < b:
        return (x - a) / (b - a)

    if b <= x <= c:
        return 1.0

    if c == d and x == d:
        return 1.0

    if c < x < d:
        return (d - x) / (d - c)

    return 0.0


# ============================================================
# TRIANGULAR
# ============================================================

def pertenencia_triangular(x, parametros):

    a, b, c = parametros

    if x < a or x > c:
        return 0.0

    if x == b:
        return 1.0

    if a == b and x == a:
        return 1.0

    if b == c and x == c:
        return 1.0

    if a < x < b:
        return (x - a) / (b - a)

    if b < x < c:
        return (c - x) / (c - b)

    return 0.0


# ============================================================
# FUZZIFICACIÓN GENERAL
# ============================================================

def fuzzificar_variable(variable, valor):

    resultado = {}

    for conjunto in CONJUNTOS[variable]:

        parametros = PARAMETROS_MEMBRESIA[
            variable
        ][conjunto]

        if variable == "incendio":

            grado = pertenencia_triangular(
                valor,
                parametros
            )

        else:

            grado = pertenencia_trapezoidal(
                valor,
                parametros
            )

        resultado[conjunto] = grado

    return resultado


# ============================================================
# CONJUNTO DOMINANTE
# ============================================================

def conjunto_dominante(grados):

    return max(
        grados,
        key=grados.get
    )


# ============================================================
# FUZZIFICAR FILA
# ============================================================

def fuzzificar_fila(fila):

    grados = {}

    categorias = {}

    variables = (
        VARIABLES_ENTRADA
        + [VARIABLE_SALIDA]
    )

    for variable in variables:

        valor = float(
            fila[variable]
        )

        grados_variable = fuzzificar_variable(
            variable,
            valor
        )

        grados[variable] = grados_variable

        categorias[variable] = conjunto_dominante(
            grados_variable
        )

    return grados, categorias


# ============================================================
# FUZZIFICAR DATASET
# ============================================================

def fuzzificar_dataset():

    df = pd.read_csv(
        ARCHIVO_DATASET
    )

    datos_fuzzificados = []

    evidencia = []

    for _, fila in df.iterrows():

        grados, categorias = fuzzificar_fila(
            fila
        )

        datos_fuzzificados.append(
            grados
        )

        evidencia.append(
            categorias
        )

    df_evidencia = pd.DataFrame(
        evidencia
    )

    df_evidencia.to_csv(
        ARCHIVO_DATASET_FUZZIFICADO,
        index=False
    )

    return (
        df,
        datos_fuzzificados
    )