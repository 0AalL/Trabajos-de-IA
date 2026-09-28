import numpy as np # type: ignore
from configuracion import (
    VARIABLES_ENTRADA,
    VARIABLE_SALIDA
)


# ============================================================
# CALCULAR MÉTRICAS VECTORIZADAS
# ============================================================

def calcular_metricas(regla, datos_fuzzificados):
    # La matriz de salida de una variable cualquiera nos da el total de registros (N)
    consecuente_cualquiera = next(iter(datos_fuzzificados[VARIABLE_SALIDA].values()))
    n = len(consecuente_cualquiera)

    # --------------------------------------------------------
    # 1. Grado del antecedente
    # --------------------------------------------------------
    grados_a = []
    num_antecedentes = 0
    
    for i, variable in enumerate(VARIABLES_ENTRADA):
        conjunto = regla[i]
        if conjunto == "NO_USAR":
            continue
            
        num_antecedentes += 1
        grados_a.append(datos_fuzzificados[variable][conjunto])
        
    # Exigir al menos 2 antecedentes para evitar reglas triviales de 1 sola variable
    if num_antecedentes < 2:
        return {
            "support": 0.0,
            "confidence": 0.0,
            "coverage": 0.0,
            "lift": 0.0,
            "fitness": 0.0
        }
        
    # AND difuso = mínimo vectorizado
    grado_a = np.minimum.reduce(grados_a)

    # --------------------------------------------------------
    # 2. Grado del consecuente
    # --------------------------------------------------------
    indice_salida = len(VARIABLES_ENTRADA)
    consecuente = regla[indice_salida]
    grado_b = datos_fuzzificados[VARIABLE_SALIDA][consecuente]

    # --------------------------------------------------------
    # 3. Intersección (A AND B)
    # --------------------------------------------------------
    grado_ab = np.minimum(grado_a, grado_b)

    # --------------------------------------------------------
    # 4. Calcular sumas
    # --------------------------------------------------------
    suma_ab = float(np.sum(grado_ab))
    suma_a = float(np.sum(grado_a))
    suma_b = float(np.sum(grado_b))

    # --------------------------------------------------------
    # 5. Métricas clásicas
    # --------------------------------------------------------
    support = suma_ab / n
    coverage = suma_a / n
    support_b = suma_b / n
    
    confidence = (support / coverage) if coverage > 0 else 0.0
    lift = (confidence / support_b) if support_b > 0 else 0.0

    # --------------------------------------------------------
    # 6. FITNESS (Multiobjetivo y Parsimonia Contextual)
    # --------------------------------------------------------
    # Exigimos un umbral mínimo de cobertura estadística (0.5% del dataset = 100 filas)
    # y que la regla tenga correlación positiva (Lift > 1.05)
    if coverage < 0.005 or lift < 1.05:
        fitness = 0.0001
    else:
        # Parsimonia amigable con 2 y 3 antecedentes (longitud óptima de reglas difusas)
        penalizacion_long = 1.0 if num_antecedentes <= 3 else (1.0 - (num_antecedentes - 3) * 0.1)
        
        # Cobertura relativa a la clase (cuánto de la clase objetivo logra capturar)
        cobertura_clase = support / support_b if support_b > 0 else 0.0
        
        # Fitness balanceado: confianza alta (0.7) y representatividad de clase (0.3)
        fitness = (0.7 * confidence + 0.3 * cobertura_clase) * penalizacion_long

    return {
        "support": support,
        "confidence": confidence,
        "coverage": coverage,
        "lift": lift,
        "fitness": fitness
    }


# ============================================================
# EVALUAR INDIVIDUO
# ============================================================

def evaluar_individuo(individuo, datos_fuzzificados):
    metricas = calcular_metricas(individuo, datos_fuzzificados)
    return (metricas["fitness"],)