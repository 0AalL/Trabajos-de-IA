import numpy as np
import os


# ============================================================
# VARIABLES DE ENTRADA
# ============================================================

VARIABLES_ENTRADA = [
    "temperatura",
    "humedad",
    "viento",
    "precipitacion",
    "co2",
    "co",
    "oxigeno"
]

VARIABLE_SALIDA = "incendio"


# ============================================================
# CONJUNTOS FUZZY
# ============================================================

CONJUNTOS = {

    "temperatura": [
        "low",
        "medium",
        "high",
        "extreme"
    ],

    "humedad": [
        "very_low",
        "low",
        "normal",
        "high"
    ],

    "viento": [
        "low",
        "medium",
        "high",
        "extreme"
    ],

    "precipitacion": [
        "low",
        "medium",
        "high",
        "extreme"
    ],

    "co2": [
        "low",
        "normal",
        "high",
        "extreme"
    ],

    "co": [
        "normal",
        "medium",
        "high",
        "extreme"
    ],

    "oxigeno": [
        "very_low",
        "low",
        "normal",
        "high"
    ],

    "incendio": [
        "nonexistent",
        "low",
        "high",
        "extreme"
    ]
}


# ============================================================
# NO USAR
# ============================================================

NO_USAR = "NO_USAR"


# ============================================================
# FUNCIONES DE PERTENENCIA
# ============================================================

PARAMETROS_MEMBRESIA = {

    "temperatura": {

        "low": [0, 0, 25, 30],

        "medium": [25, 30, 34, 37],

        "high": [34, 37, 41, 45],

        "extreme": [41, 45, 100, 100]
    },

    "humedad": {

        "very_low": [0, 0, 15, 25],

        "low": [15, 25, 35, 45],

        "normal": [35, 45, 57.5, 70],

        "high": [57.5, 70, 100, 100]
    },

    "viento": {

        "low": [0, 0, 10, 30],

        "medium": [10, 30, 40, 60],

        "high": [40, 60, 80, 100],

        "extreme": [80, 100, 240, 240]
    },

    "precipitacion": {

        "low": [0, 0, 0, 6.5],

        "medium": [0, 6.5, 12, 16],

        "high": [12, 16, 30, 40],

        "extreme": [30, 40, 100, 100]
    },

    "co2": {

        "low": [0, 0, 150, 250],

        "normal": [150, 250, 400, 500],

        "high": [400, 500, 700, 900],

        "extreme": [700, 900, 1000, 1000]
    },

    "co": {

        "normal": [0, 0, 0, 10],

        "medium": [0, 10, 12, 20],

        "high": [12, 20, 40, 50],

        "extreme": [40, 50, 100, 100]
    },

    "oxigeno": {

        "very_low": [0, 0, 12, 15],

        "low": [12, 15, 17, 20],

        "normal": [17, 20, 23, 26],

        "high": [23, 26, 30, 30]
    },

    "incendio": {

        "nonexistent": [0, 0, 33.334],

        "low": [0, 33.334, 66.666],

        "high": [33.334, 66.666, 100],

        "extreme": [66.666, 100, 100]
    }
}


# ============================================================
# UNIVERSOS
# ============================================================

UNIVERSOS = {

    "temperatura": np.arange(0, 101, 1),

    "humedad": np.arange(0, 101, 1),

    "viento": np.arange(0, 241, 1),

    "precipitacion": np.arange(0, 101, 1),

    "co2": np.arange(0, 1001, 1),

    "co": np.arange(0, 101, 1),

    "oxigeno": np.arange(0, 31, 1),

    "incendio": np.arange(0, 101, 1)
}


# ============================================================
# ALGORITMO GENÉTICO
# ============================================================

TAM_POBLACION = 100

NUM_GENERACIONES = 200

PROB_CRUCE = 0.80

PROB_MUTACION = 0.10

TAM_TORNEO = 3

SEMILLA = 42


# ============================================================
# ARCHIVOS
# ============================================================

ARCHIVO_DATASET = "dataset_numerico.csv"

CARPETA_RESULTADOS = "resultados"

ARCHIVO_DATASET_FUZZIFICADO = os.path.join(
    CARPETA_RESULTADOS,
    "dataset_fuzzificado.csv"
)

ARCHIVO_REGLAS_ULTIMA_GENERACION = os.path.join(
    CARPETA_RESULTADOS,
    "reglas_ultima_generacion.csv"
)

ARCHIVO_REGLAS_FINALES = os.path.join(
    CARPETA_RESULTADOS,
    "reglas_finales.csv"
)