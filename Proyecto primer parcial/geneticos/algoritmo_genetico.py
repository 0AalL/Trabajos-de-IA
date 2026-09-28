
import random
import pandas as pd

from configuracion import (
    TAM_POBLACION,
    NUM_GENERACIONES,
    SEMILLA,
    ARCHIVO_REGLAS_ULTIMA_GENERACION,
    VARIABLES_ENTRADA,
    VARIABLE_SALIDA,
    CONJUNTOS
)

from poblacion_inicial import crear_poblacion_inicial
from seleccion_padres import seleccionar_padres
from crossover import realizar_crossover
from mutacion import realizar_mutacion
from eliminacion import eliminar_peores
from fitness import evaluar_individuo, calcular_metricas


# =========================================================
# SEMILLA
# =========================================================

random.seed(SEMILLA)


# =========================================================
# EVALUAR POBLACIÓN
# =========================================================

def evaluar_poblacion(poblacion, datos_fuzzificados):
    """
    Calcula el fitness de todos los individuos de una población.
    """

    for individuo in poblacion:
        individuo.fitness.values = evaluar_individuo(
            individuo,
            datos_fuzzificados
        )


# =========================================================
# EVOLUCIONAR POBLACIÓN PARA UNA CLASE (NICHO ESPECÍFICO)
# =========================================================

def evolucionar_poblacion_clase(
    clase_objetivo,
    datos_fuzzificados,
    num_generaciones=NUM_GENERACIONES
):
    """
    Evoluciona una población especializada en una clase de salida específica.
    Garantiza que la clase objetivo no sea canibalizada por clases mayoritarias.
    """

    poblacion = crear_poblacion_inicial(
        consecuente_fijo=clase_objetivo
    )

    evaluar_poblacion(
        poblacion,
        datos_fuzzificados
    )

    historial = {
        "generaciones": [],
        "fitness": [],
        "fitness_promedio": []
    }

    for generacion in range(num_generaciones):

        padres = seleccionar_padres(
            poblacion
        )

        hijos = realizar_crossover(
            padres,
            consecuente_fijo=clase_objetivo
        )

        hijos = realizar_mutacion(
            hijos,
            consecuente_fijo=clase_objetivo
        )

        evaluar_poblacion(
            hijos,
            datos_fuzzificados
        )

        poblacion = eliminar_peores(
            poblacion,
            hijos
        )

        fitnesses = [
            individuo.fitness.values[0]
            for individuo in poblacion
        ]

        mejor_fitness = max(
            fitnesses
        )

        promedio_fitness = (
            sum(fitnesses) / len(fitnesses)
        )

        historial["generaciones"].append(
            generacion + 1
        )

        historial["fitness"].append(
            mejor_fitness
        )

        historial["fitness_promedio"].append(
            promedio_fitness
        )

        if (generacion + 1) % 25 == 0 or generacion == 0 or (generacion + 1) == num_generaciones:
            print(
                f"[{clase_objetivo.upper():^7}] Gen {generacion + 1:03d}/{num_generaciones} "
                f"| Mejor Fitness = {mejor_fitness:.6f} "
                f"| Promedio = {promedio_fitness:.6f}"
            )

    # Extraer reglas únicas encontradas en la población final
    reglas = []
    reglas_vistas = set()

    for individuo in poblacion:

        ant = tuple(individuo[:-1])

        if ant in reglas_vistas:

            continue

        reglas_vistas.add(ant)

        metricas = calcular_metricas(
            individuo,
            datos_fuzzificados
        )

        reglas.append({
            "individuo": list(individuo),
            "support": metricas["support"],
            "confidence": metricas["confidence"],
            "coverage": metricas["coverage"],
            "lift": metricas["lift"],
            "fitness": metricas["fitness"]
        })

    reglas.sort(
        key=lambda r: r["fitness"],
        reverse=True
    )

    return reglas, historial


# =========================================================
# EJECUTAR ALGORITMO GENÉTICO (MULTICLASE CON NICHOS)
# =========================================================

def ejecutar_algoritmo_genetico(datos_fuzzificados):
    """
    Ejecuta el Algoritmo Genético Multiclase con Nichos.
    Evoluciona independientemente para cada clase de salida (nulo, bajo, alto, extremo)
    para evitar la exclusión competitiva y garantizar la completitud del sistema difuso.
    """

    clases = CONJUNTOS[VARIABLE_SALIDA]
    todas_las_reglas = []
    historial_global = {}

    for clase in clases:

        print()
        print("=" * 60)
        print(f"EVOLUCIÓN DE NICHO PARA CLASE DE RIESGO: {clase.upper()}")
        print("=" * 60)

        reglas_clase, historial_clase = evolucionar_poblacion_clase(
            clase,
            datos_fuzzificados,
            num_generaciones=NUM_GENERACIONES
        )

        historial_global[clase] = historial_clase

        print(f"Reglas únicas encontradas para '{clase}': {len(reglas_clase)}")

        if reglas_clase:

            mejor = reglas_clase[0]
            print(f"-> Mejor regla: {convertir_regla_texto(mejor['individuo'])}")
            print(f"   Confianza = {mejor['confidence']:.4f} | Cobertura = {mejor['coverage']:.4f} | Fitness = {mejor['fitness']:.4f}")

            # Guardamos las mejores reglas de esta clase (hasta 5 mejores)
            todas_las_reglas.extend(reglas_clase[:5])

    # Ordenar por fitness descendente
    todas_las_reglas.sort(
        key=lambda regla: regla["fitness"],
        reverse=True
    )

    # Guardar en archivo reglas_ultima_generacion.csv
    filas = []

    for numero, regla in enumerate(todas_las_reglas, start=1):

        filas.append({
            "numero": numero,
            "regla": convertir_regla_texto(regla["individuo"]),
            "support": regla["support"],
            "confidence": regla["confidence"],
            "coverage": regla["coverage"],
            "lift": regla["lift"],
            "fitness": regla["fitness"]
        })

    df_reglas = pd.DataFrame(filas)
    df_reglas.to_csv(
        ARCHIVO_REGLAS_ULTIMA_GENERACION,
        index=False
    )

    return todas_las_reglas, historial_global


# =========================================================
# CONVERTIR REGLA A TEXTO
# =========================================================

def convertir_regla_texto(regla):

    condiciones = []

    # -----------------------------------------------------
    # RECORRER LAS VARIABLES DE ENTRADA
    # -----------------------------------------------------

    for i, variable in enumerate(
        VARIABLES_ENTRADA
    ):

        conjunto = regla[i]

        # Si no es NO_USAR, se agrega la condición
        if conjunto != "NO_USAR":

            condiciones.append(
                f"{variable}={conjunto}"
            )

    # -----------------------------------------------------
    # CONSTRUIR ANTECEDENTE
    # -----------------------------------------------------

    if condiciones:

        antecedente = " AND ".join(
            condiciones
        )

    else:

        antecedente = "TRUE"

    # -----------------------------------------------------
    # OBTENER CONSECUENTE
    # -----------------------------------------------------
    #
    # La última posición del individuo corresponde
    # a la variable de salida.
    # -----------------------------------------------------

    indice_salida = len(
        VARIABLES_ENTRADA
    )

    consecuente = regla[
        indice_salida
    ]

    # -----------------------------------------------------
    # CONSTRUIR REGLA COMPLETA
    # -----------------------------------------------------

    return (
        f"IF {antecedente} "
        f"THEN {VARIABLE_SALIDA}={consecuente}"
    )
