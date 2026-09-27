
import random
import pandas as pd

from configuracion import (
    TAM_POBLACION,
    NUM_GENERACIONES,
    SEMILLA,
    ARCHIVO_REGLAS_ULTIMA_GENERACION,
    VARIABLES_ENTRADA
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

    El fitness está definido únicamente como el Lift de la regla.
    """

    for individuo in poblacion:
        individuo.fitness.values = evaluar_individuo(
            individuo,
            datos_fuzzificados
        )


# =========================================================
# EJECUTAR ALGORITMO GENÉTICO
# =========================================================

def ejecutar_algoritmo_genetico(datos_fuzzificados):

    # -----------------------------------------------------
    # 1. CREAR POBLACIÓN INICIAL
    # -----------------------------------------------------

    poblacion = crear_poblacion_inicial()

    # Evaluar población inicial
    evaluar_poblacion(
        poblacion,
        datos_fuzzificados
    )

    # Historial para guardar la evolución
    historial = {
        "generaciones": [],
        "fitness": [],
        "fitness_promedio": []
    }

    # -----------------------------------------------------
    # 2. EVOLUCIÓN
    # -----------------------------------------------------

    for generacion in range(NUM_GENERACIONES):

        # -------------------------------------------------
        # SELECCIÓN
        # -------------------------------------------------

        padres = seleccionar_padres(
            poblacion
        )

        # -------------------------------------------------
        # CROSSOVER
        # -------------------------------------------------

        hijos = realizar_crossover(
            padres
        )

        # -------------------------------------------------
        # MUTACIÓN
        # -------------------------------------------------

        hijos = realizar_mutacion(
            hijos
        )

        # -------------------------------------------------
        # EVALUACIÓN DE LOS HIJOS
        # -------------------------------------------------

        evaluar_poblacion(
            hijos,
            datos_fuzzificados
        )

        # -------------------------------------------------
        # ELIMINACIÓN
        # -------------------------------------------------
        #
        # Se juntan:
        #
        #   población actual + hijos
        #
        # y se conservan los mejores individuos.
        #
        # Esto corresponde a una estrategia (μ + λ).
        # -------------------------------------------------

        poblacion = eliminar_peores(
            poblacion,
            hijos
        )

        # -------------------------------------------------
        # CALCULAR ESTADÍSTICAS
        # -------------------------------------------------

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

        # -------------------------------------------------
        # GUARDAR HISTORIAL
        # -------------------------------------------------

        historial["generaciones"].append(
            generacion + 1
        )

        historial["fitness"].append(
            mejor_fitness
        )

        historial["fitness_promedio"].append(
            promedio_fitness
        )

        # -------------------------------------------------
        # MOSTRAR PROGRESO
        # -------------------------------------------------

        print(
            f"Generación "
            f"{generacion + 1:03d}/{NUM_GENERACIONES} "
            f"| Mejor Fitness = {mejor_fitness:.6f} "
            f"| Fitness Promedio = {promedio_fitness:.6f}"
        )

    # =====================================================
    # 3. OBTENER REGLAS DE LA ÚLTIMA GENERACIÓN
    # =====================================================

    reglas = []

    for individuo in poblacion:

        # Calcular nuevamente todas las métricas
        metricas = calcular_metricas(
            individuo,
            datos_fuzzificados
        )

        regla = {
            "individuo": list(individuo),

            "support": metricas["support"],

            "confidence": metricas["confidence"],

            "coverage": metricas["coverage"],

            "lift": metricas["lift"],

            "fitness": metricas["fitness"]
        }

        reglas.append(
            regla
        )

    # =====================================================
    # 4. ORDENAR REGLAS POR FITNESS
    # =====================================================
    #
    # Como:
    #
    #     Fitness = Lift
    #
    # ordenar por fitness equivale a ordenar por Lift.
    # =====================================================

    reglas.sort(
        key=lambda regla: regla["fitness"],
        reverse=True
    )

    # =====================================================
    # 5. GUARDAR REGLAS DE LA ÚLTIMA GENERACIÓN
    # =====================================================

    filas = []

    for numero, regla in enumerate(
        reglas,
        start=1
    ):

        filas.append(
            {
                "numero": numero,

                "regla": convertir_regla_texto(
                    regla["individuo"]
                ),

                "support": regla["support"],

                "confidence": regla["confidence"],

                "coverage": regla["coverage"],

                "lift": regla["lift"],

                "fitness": regla["fitness"]
            }
        )

    df_reglas = pd.DataFrame(
        filas
    )

    df_reglas.to_csv(
        ARCHIVO_REGLAS_ULTIMA_GENERACION,
        index=False
    )

    # =====================================================
    # 6. RETORNAR RESULTADOS
    # =====================================================

    return reglas, historial


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
    # a la variable de salida incendio.
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
        f"THEN incendio={consecuente}"
    )
