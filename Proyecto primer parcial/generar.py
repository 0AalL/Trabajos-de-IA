import csv
import random


NUM_REGISTROS = 1000

ARCHIVO_SALIDA = "dataset_numerico.csv"

SEMILLA = 42

random.seed(SEMILLA)


# ============================================================
# CALCULAR INCENDIO
# ============================================================

def calcular_incendio(
    temperatura,
    humedad,
    viento,
    precipitacion,
    co2,
    co,
    oxigeno
):

    riesgo = 0.0

    # Temperatura
    if temperatura >= 40:
        riesgo += 25

    elif temperatura >= 34:
        riesgo += 18

    elif temperatura >= 30:
        riesgo += 10

    elif temperatura >= 25:
        riesgo += 5

    # Humedad
    if humedad <= 15:
        riesgo += 20

    elif humedad <= 25:
        riesgo += 15

    elif humedad <= 35:
        riesgo += 10

    elif humedad <= 45:
        riesgo += 5

    # Viento
    if viento >= 80:
        riesgo += 15

    elif viento >= 60:
        riesgo += 12

    elif viento >= 40:
        riesgo += 8

    elif viento >= 30:
        riesgo += 4

    # Precipitación
    if precipitacion <= 1:
        riesgo += 15

    elif precipitacion <= 6.5:
        riesgo += 10

    elif precipitacion <= 12:
        riesgo += 5

    elif precipitacion >= 30:
        riesgo -= 15

    # CO2
    if co2 >= 700:
        riesgo += 10

    elif co2 >= 500:
        riesgo += 7

    elif co2 >= 400:
        riesgo += 4

    # CO
    if co >= 40:
        riesgo += 10

    elif co >= 20:
        riesgo += 7

    elif co >= 10:
        riesgo += 4

    # Oxígeno
    if oxigeno <= 12:
        riesgo += 10

    elif oxigeno <= 15:
        riesgo += 7

    elif oxigeno <= 17:
        riesgo += 4

    # Interacciones
    if temperatura >= 34 and humedad <= 25:
        riesgo += 10

    if temperatura >= 34 and viento >= 60:
        riesgo += 8

    if (
        temperatura >= 34
        and humedad <= 25
        and precipitacion <= 6.5
    ):
        riesgo += 12

    if co >= 20 and co2 >= 500:
        riesgo += 8

    if (
        temperatura >= 40
        and humedad <= 15
        and viento >= 80
    ):
        riesgo += 10

    # Ruido
    riesgo += random.uniform(-5, 5)

    riesgo = max(
        0,
        min(100, riesgo)
    )

    return round(riesgo, 2)


# ============================================================
# GENERAR FILA
# ============================================================

def generar_fila():

    temperatura = round(
        random.uniform(0, 45),
        2
    )

    humedad = round(
        random.uniform(0, 100),
        2
    )

    viento = round(
        random.uniform(0, 100),
        2
    )

    precipitacion = round(
        random.uniform(0, 40),
        2
    )

    co2 = round(
        random.uniform(150, 900),
        2
    )

    co = round(
        random.uniform(0, 50),
        2
    )

    oxigeno = round(
        random.uniform(15, 26),
        2
    )

    incendio = calcular_incendio(
        temperatura,
        humedad,
        viento,
        precipitacion,
        co2,
        co,
        oxigeno
    )

    return [
        temperatura,
        humedad,
        viento,
        precipitacion,
        co2,
        co,
        oxigeno,
        incendio
    ]


# ============================================================
# GENERAR DATASET
# ============================================================

def generar_dataset():

    columnas = [
        "temperatura",
        "humedad",
        "viento",
        "precipitacion",
        "co2",
        "co",
        "oxigeno",
        "incendio"
    ]

    datos = []

    for _ in range(NUM_REGISTROS):

        datos.append(
            generar_fila()
        )

    with open(
        ARCHIVO_SALIDA,
        "w",
        newline="",
        encoding="utf-8"
    ) as archivo:

        escritor = csv.writer(archivo)

        escritor.writerow(columnas)

        escritor.writerows(datos)

    print("=" * 60)
    print("DATASET GENERADO")
    print("=" * 60)

    print(
        f"Archivo: {ARCHIVO_SALIDA}"
    )

    print(
        f"Registros: {NUM_REGISTROS}"
    )


if __name__ == "__main__":

    generar_dataset()