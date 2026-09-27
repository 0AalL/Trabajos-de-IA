from configuracion import VARIABLES_ENTRADA


# ============================================================
# GRADO DEL ANTECEDENTE
# ============================================================

def grado_antecedente(
    regla,
    fila_grados
):

    grados = []

    for i, variable in enumerate(
        VARIABLES_ENTRADA
    ):

        conjunto = regla[i]

        # NO_USAR = no participa
        if conjunto == "NO_USAR":

            continue

        grado = fila_grados[
            variable
        ].get(
            conjunto,
            0.0
        )

        grados.append(
            grado
        )

    if not grados:

        return 0.0

    # AND fuzzy = mínimo
    return min(
        grados
    )


# ============================================================
# GRADO DEL CONSECUENTE
# ============================================================

def grado_consecuente(
    regla,
    fila_grados
):

    indice = len(
        VARIABLES_ENTRADA
    )

    conjunto = regla[
        indice
    ]

    return fila_grados[
        "incendio"
    ].get(
        conjunto,
        0.0
    )


# ============================================================
# CALCULAR MÉTRICAS
# ============================================================

def calcular_metricas(
    regla,
    datos_fuzzificados
):

    suma_ab = 0.0

    suma_a = 0.0

    suma_b = 0.0

    n = len(
        datos_fuzzificados
    )

    if n == 0:

        return {
            "support": 0.0,
            "confidence": 0.0,
            "coverage": 0.0,
            "lift": 0.0,
            "fitness": 0.0
        }

    for fila_grados in datos_fuzzificados:

        grado_a = grado_antecedente(
            regla,
            fila_grados
        )

        grado_b = grado_consecuente(
            regla,
            fila_grados
        )

        grado_ab = min(
            grado_a,
            grado_b
        )

        suma_ab += grado_ab

        suma_a += grado_a

        suma_b += grado_b

    # --------------------------------------------------------
    # Support
    # --------------------------------------------------------

    support = (
        suma_ab / n
    )

    # --------------------------------------------------------
    # Coverage
    # --------------------------------------------------------

    coverage = (
        suma_a / n
    )

    # --------------------------------------------------------
    # Support del consecuente
    # --------------------------------------------------------

    support_b = (
        suma_b / n
    )

    # --------------------------------------------------------
    # Confidence
    # --------------------------------------------------------

    if coverage > 0:

        confidence = (
            support / coverage
        )

    else:

        confidence = 0.0

    # --------------------------------------------------------
    # Lift
    # --------------------------------------------------------

    if support_b > 0:

        lift = (
            confidence / support_b
        )

    else:

        lift = 0.0

    # --------------------------------------------------------
    # FITNESS
    # --------------------------------------------------------

    fitness = lift

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

def evaluar_individuo(
    individuo,
    datos_fuzzificados
):

    metricas = calcular_metricas(
        individuo,
        datos_fuzzificados
    )

    return (
        metricas["fitness"],
    )