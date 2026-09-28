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

    if porcentaje < 5.0:

        return "NULO"

    elif porcentaje < 50.0:

        return "BAJO"

    elif porcentaje < 1000.0:

        return "ALTO"

    else:

        return "EXTREMO"