import pandas as pd
import numpy as np # type: ignore

from configuracion import (
    VARIABLES_ENTRADA,
    VARIABLE_SALIDA,
    CONJUNTOS,
    PARAMETROS_MEMBRESIA,
    ARCHIVO_DATASET,
    ARCHIVO_DATASET_FUZZIFICADO
)

# ============================================================
# TRAPEZOIDAL VECTORIZADO
# ============================================================

def pertenencia_trapezoidal_vec(x, parametros):
    a, b, c, d = parametros
    y = np.zeros_like(x, dtype=float)
    
    # b <= x <= c
    if b <= c:
        y[(x >= b) & (x <= c)] = 1.0
        
    # a < x < b
    if b > a:
        mask = (x > a) & (x < b)
        y[mask] = (x[mask] - a) / (b - a)
    elif a == b:
        y[x == a] = 1.0
        
    # c < x < d
    if d > c:
        mask = (x > c) & (x < d)
        y[mask] = (d - x[mask]) / (d - c)
    elif c == d:
        y[x == d] = 1.0
        
    return y


# ============================================================
# FUZZIFICAR DATASET VECTORIZADO
# ============================================================

def fuzzificar_dataset():
    df = pd.read_csv(ARCHIVO_DATASET)
    df.rename(columns={
        "T_mean": "T_media",
        "RH_mean": "HR_media",
        "Wind_mean": "Viento_medio",
        "PPT_tot": "Precipitacion",
        "Area Burned (Ha)": "Area Quemada (Ha)"
    }, inplace=True)
    
    datos_fuzzificados = {}
    evidencia = {}
    
    variables = VARIABLES_ENTRADA + [VARIABLE_SALIDA]
    
    for variable in variables:
        datos_fuzzificados[variable] = {}
        valores = df[variable].values.astype(float)
        
        # Calcular pertenencia para cada conjunto difuso
        for conjunto in CONJUNTOS[variable]:
            parametros = PARAMETROS_MEMBRESIA[variable][conjunto]
            grados = pertenencia_trapezoidal_vec(valores, parametros)
            datos_fuzzificados[variable][conjunto] = grados
            
        # Determinar el conjunto dominante para la evidencia
        grados_matriz = np.array([datos_fuzzificados[variable][c] for c in CONJUNTOS[variable]])
        indices_max = np.argmax(grados_matriz, axis=0)
        conjuntos = np.array(CONJUNTOS[variable])
        evidencia[variable] = conjuntos[indices_max]
        
    df_evidencia = pd.DataFrame(evidencia)
    df_evidencia.to_csv(ARCHIVO_DATASET_FUZZIFICADO, index=False)
    
    return df, datos_fuzzificados