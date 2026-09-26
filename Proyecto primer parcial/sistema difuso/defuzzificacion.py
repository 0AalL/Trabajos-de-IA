import skfuzzy as fuzz


# =========================================================
# DEFUZZIFICACIÓN POR CENTROIDE
# =========================================================

def defuzzificar_centroide(
    universo,
    salida_agregada
):

    area = salida_agregada.sum()

    if area <= 0:

        return 0.0

    resultado = fuzz.defuzz(
        universo,
        salida_agregada,
        "centroid"
    )

    return float(
        resultado
    )


# =========================================================
# CLASIFICAR RESULTADO
# =========================================================

def clasificar_riesgo(
    porcentaje
):

    if porcentaje < 33.334:

        return "NONEXISTENT"

    elif porcentaje < 66.666:

        return "LOW"

    elif porcentaje < 100:

        return "HIGH"

    else:

        return "EXTREME"