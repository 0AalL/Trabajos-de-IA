import random
import pandas as pd

from configuracion import (
    TAM_POBLACION,
    NUM_GENERACIONES,
    SEMILLA,
    ARCHIVO_REGLAS_ULTIMA_GENERACION,
    VARIABLES_ENTRADA,
    VARIABLE_SALIDA
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

def evaluar_poblacion(
    poblacion,
    datos_fuzzificados
):

    for individuo in poblacion:

        individuo.fitness.values = evaluar_individuo(
            individuo,
            datos_fuzzificados
        )


# =========================================================
# CONVERTIR POBLACIÓN A REGLAS
# =========================================================

def convertir_poblacion_a_reglas(
    poblacion,
    datos_fuzzificados
):

    reglas = []

    for individuo in poblacion:

        metricas = calcular_metricas(
            individuo,
            datos_fuzzificados
        )

        regla = {

            "individuo":
                list(individuo),

            "support":
                metricas["support"],

            "confidence":
                metricas["confidence"],

            "coverage":
                metricas["coverage"],

            "lift":
                metricas["lift"],

            "fitness":
                metricas["fitness"]
        }

        reglas.append(
            regla
        )

    return reglas


# =========================================================
# ELIMINAR REGLAS DUPLICADAS
# =========================================================

def eliminar_reglas_duplicadas(
    reglas
):

    unicas = {}

    for regla in reglas:

        clave = tuple(
            regla["individuo"]
        )

        # Si no existe, se guarda.
        if clave not in unicas:

            unicas[clave] = regla

        else:

            # Si ya existe, conservar la de mayor fitness.
            if (
                regla["fitness"]
                >
                unicas[clave]["fitness"]
            ):

                unicas[clave] = regla

    return list(
        unicas.values()
    )


# =========================================================
# EJECUTAR ALGORITMO GENÉTICO
# =========================================================

def ejecutar_algoritmo_genetico(
    datos_fuzzificados
):

    # -----------------------------------------------------
    # 1. CREAR POBLACIÓN INICIAL
    # -----------------------------------------------------

    poblacion = crear_poblacion_inicial()

    evaluar_poblacion(
        poblacion,
        datos_fuzzificados
    )

    # -----------------------------------------------------
    # NÚMERO DE HIJOS
    # -----------------------------------------------------
    #
    # La mitad de la población.
    #
    # Si TAM_POBLACION = 100:
    #
    #     numero_hijos = 50
    #
    # -----------------------------------------------------

    numero_hijos = TAM_POBLACION // 2

    # -----------------------------------------------------
    # GUARDAR LAS REGLAS DE CADA GENERACIÓN
    # -----------------------------------------------------
    #
    # Se guarda cada generación por separado.
    #
    # Esto permite que cobertura.py utilice primero
    # la última generación y después generaciones
    # anteriores si hace falta.
    #
    # -----------------------------------------------------

    historial_reglas = []

    # Población inicial
    reglas_iniciales = convertir_poblacion_a_reglas(
        poblacion,
        datos_fuzzificados
    )

    historial_reglas.append(
        reglas_iniciales
    )

    # -----------------------------------------------------
    # HISTORIAL
    # -----------------------------------------------------

    historial = {
        "generaciones": [],
        "fitness": [],
        "fitness_promedio": []
    }

    # =====================================================
    # 2. EVOLUCIÓN
    # =====================================================

    for generacion in range(
        NUM_GENERACIONES
    ):

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
        # LIMITAR HIJOS
        # -------------------------------------------------

        hijos = hijos[
            :numero_hijos
        ]

        # -------------------------------------------------
        # MUTACIÓN
        # -------------------------------------------------

        hijos = realizar_mutacion(
            hijos
        )

        # -------------------------------------------------
        # EVALUAR HIJOS
        # -------------------------------------------------

        evaluar_poblacion(
            hijos,
            datos_fuzzificados
        )

        # -------------------------------------------------
        # ELIMINACIÓN
        # -------------------------------------------------

        poblacion = eliminar_peores(
            poblacion,
            hijos
        )

        # -------------------------------------------------
        # CONVERTIR LA NUEVA POBLACIÓN A REGLAS
        # -------------------------------------------------

        reglas_generacion = (
            convertir_poblacion_a_reglas(
                poblacion,
                datos_fuzzificados
            )
        )

        # -------------------------------------------------
        # GUARDAR GENERACIÓN
        # -------------------------------------------------

        historial_reglas.append(
            reglas_generacion
        )

        # -------------------------------------------------
        # ESTADÍSTICAS
        # -------------------------------------------------

        fitnesses = [

            individuo.fitness.values[0]

            for individuo in poblacion
        ]

        mejor_fitness = max(
            fitnesses
        )

        promedio_fitness = (
            sum(fitnesses)
            /
            len(fitnesses)
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

        # -------------------------------------------------
        # MOSTRAR PROGRESO
        # -------------------------------------------------

        print(
            f"Generación "
            f"{generacion + 1:03d}/"
            f"{NUM_GENERACIONES} "
            f"| Mejor Fitness = "
            f"{mejor_fitness:.6f} "
            f"| Fitness Promedio = "
            f"{promedio_fitness:.6f}"
        )

    # =====================================================
    # 3. REGLAS DE LA ÚLTIMA GENERACIÓN
    # =====================================================

    reglas_ultima_generacion = (
        historial_reglas[-1]
    )

    reglas_ultima_generacion = (
        eliminar_reglas_duplicadas(
            reglas_ultima_generacion
        )
    )

    reglas_ultima_generacion.sort(
        key=lambda regla:
            regla["fitness"],
        reverse=True
    )

    # =====================================================
    # 4. CREAR BANCO DE REGLAS
    # =====================================================
    #
    # IMPORTANTE:
    #
    # Primero se agregan las reglas de la última
    # generación.
    #
    # Después se agregan las generaciones anteriores,
    # comenzando por la más reciente.
    #
    # De esta forma cobertura.py intenta cubrir todo
    # primero con la última generación.
    #
    # =====================================================

    banco_reglas = []

    for reglas_generacion in reversed(
        historial_reglas
    ):

        banco_reglas.extend(
            reglas_generacion
        )

    # -----------------------------------------------------
    # Eliminar duplicados conservando el primero.
    #
    # Como se recorrieron las generaciones desde la
    # última hacia atrás, se conserva primero la versión
    # perteneciente a la generación más reciente.
    # -----------------------------------------------------

    banco_reglas = (
        eliminar_reglas_duplicadas(
            banco_reglas
        )
    )

    # -----------------------------------------------------
    # Ordenar:
    #
    # 1. Prioridad por generación ya está representada
    #    por el orden original.
    #
    # 2. Dentro de ese banco, se prioriza fitness.
    #
    # Para garantizar que las reglas de la última
    # generación tengan prioridad, se construye el banco
    # nuevamente por bloques.
    # -----------------------------------------------------

    reglas_ordenadas = []

    utilizadas = set()

    for reglas_generacion in reversed(
        historial_reglas
    ):

        reglas_generacion = sorted(
            reglas_generacion,
            key=lambda regla:
                regla["fitness"],
            reverse=True
        )

        for regla in reglas_generacion:

            clave = tuple(
                regla["individuo"]
            )

            if clave not in utilizadas:

                utilizadas.add(
                    clave
                )

                reglas_ordenadas.append(
                    regla
                )

    # =====================================================
    # 5. GUARDAR ÚLTIMA GENERACIÓN
    # =====================================================

    filas = []

    for numero, regla in enumerate(
        reglas_ultima_generacion,
        start=1
    ):

        filas.append(
            {
                "numero":
                    numero,

                "regla":
                    convertir_regla_texto(
                        regla["individuo"]
                    ),

                "support":
                    regla["support"],

                "confidence":
                    regla["confidence"],

                "coverage":
                    regla["coverage"],

                "lift":
                    regla["lift"],

                "fitness":
                    regla["fitness"]
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
    # 6. RETORNAR
    # =====================================================
    #
    # reglas_ordenadas:
    #     Todas las reglas disponibles para cobertura.
    #
    # historial:
    #     Estadísticas del algoritmo.
    #
    # =====================================================

    return (
        reglas_ordenadas,
        historial
    )


# =========================================================
# CONVERTIR REGLA A TEXTO
# =========================================================

def convertir_regla_texto(
    regla
):

    condiciones = []

    # -----------------------------------------------------
    # VARIABLES DE ENTRADA
    # -----------------------------------------------------

    for i, variable in enumerate(
        VARIABLES_ENTRADA
    ):

        conjunto = regla[i]

        if conjunto != "NO_USAR":

            condiciones.append(
                f"{variable}={conjunto}"
            )

    # -----------------------------------------------------
    # ANTECEDENTE
    # -----------------------------------------------------

    if condiciones:

        antecedente = " AND ".join(
            condiciones
        )

    else:

        antecedente = "TRUE"

    # -----------------------------------------------------
    # CONSECUENTE
    # -----------------------------------------------------

    indice_salida = len(
        VARIABLES_ENTRADA
    )

    consecuente = regla[
        indice_salida
    ]

    # -----------------------------------------------------
    # REGLA COMPLETA
    # -----------------------------------------------------

    return (
        f"IF {antecedente} "
        f"THEN {VARIABLE_SALIDA}="
        f"{consecuente}"
    )