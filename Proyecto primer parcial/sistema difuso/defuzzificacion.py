# pyrefly: ignore [missing-import]
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

    if porcentaje < 0.02:

        return "NONEXISTENT"

    elif porcentaje < 10.0:

        return "LOW"

    elif porcentaje < 366.0:

        return "HIGH"

    else:

        return "EXTREME"