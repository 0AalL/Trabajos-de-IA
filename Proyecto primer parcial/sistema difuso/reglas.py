import pandas as pd

from configuracion import (
    ARCHIVO_REGLAS,
    VARIABLES_ENTRADA
)


# =========================================================
# CARGAR CSV
# =========================================================

def cargar_reglas():

    df = pd.read_csv(
        ARCHIVO_REGLAS
    )

    reglas = []

    for _, fila in df.iterrows():

        texto = str(
            fila["regla"]
        )

        regla = parsear_regla(
            texto
        )

        regla["numero"] = int(
            fila["numero"]
        )

        regla["support"] = float(
            fila["support"]
        )

        regla["confidence"] = float(
            fila["confidence"]
        )

        regla["coverage"] = float(
            fila["coverage"]
        )

        regla["lift"] = float(
            fila["lift"]
        )

        regla["fitness"] = float(
            fila["fitness"]
        )

        reglas.append(
            regla
        )

    return reglas


# =========================================================
# PARSEAR REGLA
# =========================================================

def parsear_regla(texto):

    partes = texto.split(
        " THEN "
    )

    antecedente = partes[0]

    consecuente = partes[1]

    antecedente = antecedente.replace(
        "IF ",
        ""
    ).strip()

    consecuente = consecuente.replace(
        "Area Quemada (Ha)=",
        ""
    ).strip()

    condiciones = {}

    if antecedente != "TRUE":

        partes_condiciones = antecedente.split(
            " AND "
        )

        for condicion in partes_condiciones:

            variable, conjunto = condicion.split(
                "="
            )

            condiciones[
                variable.strip()
            ] = conjunto.strip()

    for variable in VARIABLES_ENTRADA:

        if variable not in condiciones:

            condiciones[variable] = "NO_USAR"

    return {

        "condiciones": condiciones,

        "consecuente": consecuente
    }


# =========================================================
# TEXTO DE REGLA
# =========================================================

def regla_a_texto(regla):

    condiciones = []

    for variable in VARIABLES_ENTRADA:

        conjunto = regla[
            "condiciones"
        ][
            variable
        ]

        if conjunto != "NO_USAR":

            condiciones.append(
                f"{variable}={conjunto}"
            )

    if condiciones:

        antecedente = " AND ".join(
            condiciones
        )

    else:

        antecedente = "TRUE"

    return (
        f"IF {antecedente} "
        f"THEN Area Quemada (Ha)={regla['consecuente']}"
    )