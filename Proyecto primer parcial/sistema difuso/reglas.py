import pandas as pd

from configuracion import (
    ARCHIVO_REGLAS,
    VARIABLES_ENTRADA,
    CONJUNTOS
)


# =========================================================
# TRADUCCIÓN DE VARIABLES
# =========================================================
#
# Nombres utilizados por el algoritmo genético
#        ↓
# Nombres utilizados por el sistema difuso
#
# =========================================================

MAPEO_VARIABLES = {

    "T_mean": "T_media",

    "RH_mean": "HR_media",

    "Wind_mean": "Viento_medio",

    "PPT_tot": "Precipitacion",

    "FFMC": "FFMC",

    "DMC": "DMC",

    "DC": "DC",

    "KBDI": "KBDI"
}


# =========================================================
# TRADUCCIÓN DE CONJUNTOS
# =========================================================
#
# Las primeras seis variables del sistema difuso
# utilizan nombres en español.
#
# DC y KBDI conservan los nombres en inglés.
#
# =========================================================

MAPEO_CONJUNTOS = {

    "T_media": {
        "low": "bajo",
        "medium": "medio",
        "high": "alto",
        "extreme": "extremo"
    },

    "HR_media": {
        "very_low": "muy_bajo",
        "low": "bajo",
        "medium": "normal",
        "high": "alto",
        "extreme": "alto"
    },

    "Viento_medio": {
        "low": "bajo",
        "medium": "medio",
        "high": "alto",
        "extreme": "extremo"
    },

    "Precipitacion": {
        "low": "bajo",
        "medium": "medio",
        "high": "alto",
        "extreme": "extremo"
    },

    "FFMC": {
        "low": "bajo",
        "medium": "medio",
        "high": "alto",
        "extreme": "extremo"
    },

    "DMC": {
        "low": "bajo",
        "medium": "medio",
        "high": "alto",
        "extreme": "extremo"
    },

    # -----------------------------------------------------
    # DC y KBDI NO SE TRADUCEN
    # -----------------------------------------------------

    "DC": {
        "low": "low",
        "medium": "medium",
        "high": "high",
        "extreme": "extreme"
    },

    "KBDI": {
        "low": "low",
        "medium": "medium",
        "high": "high",
        "extreme": "extreme"
    }
}


# =========================================================
# TRADUCCIÓN DE SALIDA
# =========================================================

MAPEO_SALIDA = {

    "nonexistent": "null",

    "null": "null",

    "low": "low",

    "high": "high",

    "extreme": "extreme"
}


# =========================================================
# NORMALIZAR VARIABLE
# =========================================================

def normalizar_variable(variable):

    variable = variable.strip()

    return MAPEO_VARIABLES.get(
        variable,
        variable
    )


# =========================================================
# NORMALIZAR CONJUNTO
# =========================================================

def normalizar_conjunto(
    variable,
    conjunto
):

    conjunto = conjunto.strip()

    # -----------------------------------------------------
    # NO_USAR no se modifica
    # -----------------------------------------------------

    if conjunto == "NO_USAR":

        return "NO_USAR"

    # -----------------------------------------------------
    # Buscar traducción
    # -----------------------------------------------------

    if variable in MAPEO_CONJUNTOS:

        return MAPEO_CONJUNTOS[
            variable
        ].get(
            conjunto,
            conjunto
        )

    return conjunto


# =========================================================
# NORMALIZAR CONSECUENTE
# =========================================================

def normalizar_consecuente(consecuente):

    consecuente = consecuente.strip()

    return MAPEO_SALIDA.get(
        consecuente,
        consecuente
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
        " THEN ",
        1
    )

    if len(partes) != 2:

        raise ValueError(
            f"Regla inválida: {texto}"
        )

    antecedente = partes[0]

    consecuente = partes[1]

    antecedente = antecedente.replace(
        "IF ",
        "",
        1
    ).strip()

    # =====================================================
    # CONSECUENTE
    # =====================================================

    if "=" in consecuente:

        consecuente = consecuente.split(
            "=",
            1
        )[1].strip()

    consecuente = normalizar_consecuente(
        consecuente
    )

    # =====================================================
    # ANTECEDENTE
    # =====================================================

    condiciones = {}

    if antecedente != "TRUE":

        partes_condiciones = antecedente.split(
            " AND "
        )

        for condicion in partes_condiciones:

            condicion = condicion.strip()

            if "=" not in condicion:

                raise ValueError(
                    f"Condición inválida: {condicion}"
                )

            variable, conjunto = condicion.split(
                "=",
                1
            )

            # -------------------------------------------------
            # Traducir variable
            # -------------------------------------------------

            variable = normalizar_variable(
                variable
            )

            conjunto = normalizar_conjunto(
                variable,
                conjunto
            )

            condiciones[
                variable
            ] = conjunto

    # =====================================================
    # COMPLETAR VARIABLES NO UTILIZADAS
    # =====================================================

    for variable in VARIABLES_ENTRADA:

        if variable not in condiciones:

            condiciones[
                variable
            ] = "NO_USAR"

    # =====================================================
    # VALIDAR CONJUNTOS
    # =====================================================

    for variable, conjunto in condiciones.items():

        if conjunto == "NO_USAR":

            continue

        conjuntos_validos = CONJUNTOS.get(
            variable,
            []
        )

        if conjunto not in conjuntos_validos:

            raise ValueError(
                f"Conjunto inválido en regla: "
                f"{variable}={conjunto}. "
                f"Conjuntos válidos: {conjuntos_validos}"
            )

    # =====================================================
    # RESULTADO
    # =====================================================

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
        f"THEN Area Quemada (Ha)="
        f"{regla['consecuente']}"
    )