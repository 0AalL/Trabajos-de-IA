# pyrefly: ignore [missing-import]
import numpy as np

# ============================================================
# VARIABLES DE ENTRADA
# ============================================================

VARIABLES_ENTRADA = [
    "T_media",
    "HR_media",
    "Viento_medio",
    "Precipitacion",
    "FFMC",
    "DMC",
    "DC",
    "KBDI"
]

VARIABLE_SALIDA = "Area Quemada (Ha)"
NO_USAR = "NO_USAR"

# ============================================================
# CONJUNTOS FUZZY
# ============================================================

CONJUNTOS = {
    "T_media": ["bajo", "medio", "alto", "extremo"],
    "HR_media": ["muy_bajo", "bajo", "normal", "alto"],
    "Viento_medio": ["bajo", "medio", "alto", "extremo"],
    "Precipitacion": ["bajo", "medio", "alto", "extremo"],
    "FFMC": ["bajo", "medio", "alto", "extremo"],
    "DMC": ["bajo", "medio", "alto", "extremo"],
    "DC": ["bajo", "medio", "alto", "extremo"],
    "KBDI": ["bajo", "medio", "alto", "extremo"],
    "Area Quemada (Ha)": ["nulo", "bajo", "alto", "extremo"]
}

# ============================================================
# RANGOS VALIDOS PARA LA INTERFAZ
# ============================================================

RANGOS = {
    "T_media": (-39.24, 39.91),    # Celsius
    "HR_media": (6.248, 99.562),
    "Viento_medio": (0.265, 14.893),
    "Precipitacion": (0.0, 0.1),
    "FFMC": (2.025, 99.955),
    "DMC": (0.0, 260.0),
    "DC": (0.0, 3519.5),
    "KBDI": (0.0, 202.754)
}

# ============================================================
# FUNCIONES DE PERTENENCIA
# ============================================================

PARAMETROS_MEMBRESIA = {
    # T_mean original en Kelvin: 233.903, 276.954, etc. Convertimos restando 273.15
    "T_media": {
        "bajo": [-39.247, -39.247, 3.804, 10.279],
        "medio": [3.804, 10.279, 14.537, 17.251],
        "alto": [14.537, 17.251, 20.450, 22.694],
        "extremo": [20.450, 22.694, 39.911, 39.911]
    },
    "HR_media": {
        "muy_bajo": [6.248, 6.248, 43.596, 54.666],
        "bajo": [43.596, 54.666, 65.821, 74.249],
        "normal": [65.821, 74.249, 80.827, 84.241],
        "alto": [80.827, 84.241, 99.562, 99.562]
    },
    "Viento_medio": {
        "bajo": [0.265, 0.265, 1.544, 2.043],
        "medio": [1.544, 2.043, 2.701, 3.659],
        "alto": [2.701, 3.659, 4.449, 5.204],
        "extremo": [4.449, 5.204, 14.893, 14.893]
    },
    "Precipitacion": {
        "bajo": [0.0, 0.0, 0.0, 0.0002],
        "medio": [0.0, 0.0002, 0.0004, 0.0016],
        "alto": [0.0004, 0.0016, 0.0041, 0.0129],
        "extremo": [0.0041, 0.0129, 0.1, 0.1]
    },
    "FFMC": {
        "bajo": [2.025, 2.025, 64.226, 74.932],
        "medio": [64.226, 74.932, 84.121, 87.291],
        "alto": [84.121, 87.291, 89.555, 91.369],
        "extremo": [89.555, 91.369, 99.955, 99.955]
    },
    "DMC": {
        "bajo": [0.0, 0.0, 5.5, 11.5],
        "medio": [5.5, 11.5, 22.5, 57.0],
        "alto": [22.5, 57.0, 113.25, 143.25],
        "extremo": [113.25, 143.25, 260.0, 260.0]
    },
    "DC": {
        "bajo": [0.0, 0.0, 15.0, 41.135],
        "medio": [15.0, 41.135, 111.458, 308.203],
        "alto": [111.458, 308.203, 508.435, 663.023],
        "extremo": [508.435, 663.023, 3519.5, 3519.5]
    },
    "KBDI": {
        "bajo": [0.0, 0.0, 0.215, 1.555],
        "medio": [0.215, 1.555, 6.453, 55.902],
        "alto": [6.453, 55.902, 118.012, 139.316],
        "extremo": [118.012, 139.316, 202.754, 202.754]
    },
    "Area Quemada (Ha)": {
        "nulo": [0.0, 0.0, 0.01, 0.0310],
        "bajo": [0.01, 0.0310, 1.0118, 19.0426],
        "alto": [1.0118, 19.0426, 169.0587, 564.5370],
        "extremo": [169.0587, 564.5370, 1889779.32, 1889779.32]
    }
}

# ============================================================
# UNIVERSOS
# ============================================================

UNIVERSOS = {
    "T_media": np.arange(-39.247, 39.912, 0.01),
    "HR_media": np.arange(6.248, 99.563, 0.01),
    "Viento_medio": np.arange(0.265, 14.894, 0.01),
    "Precipitacion": np.arange(0.0, 0.1001, 0.0001),
    "FFMC": np.arange(2.025, 99.956, 0.01),
    "DMC": np.arange(0.0, 260.01, 0.1),
    "DC": np.arange(0.0, 3519.51, 1.0),
    "KBDI": np.arange(0.0, 202.7541, 0.1),
    "Area Quemada (Ha)": np.arange(0.0, 1889779.33, 10.0) # Reducida resolución para mejorar RAM/CPU
}

# ============================================================
# ARCHIVO DE REGLAS
# ============================================================

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_REGLAS = os.path.normpath(os.path.join(BASE_DIR, "..", "reglas finales", "reglas_finales.csv"))

