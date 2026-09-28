
import random
import pandas as pd

from configuracion import (
    TAM_POBLACION,
    NUM_GENERACIONES,
    SEMILLA,
    ARCHIVO_REGLAS_ULTIMA_GENERACION,
    VARIABLES_ENTRADA,
    VARIABLE_SALIDA,
    CONJUNTOS,
    NO_USAR
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
# EVOLUCIONAR POBLACIÓN PARA UNA CLASE (BÚSQUEDA TABÚ MULTI-INTENTO)
# =========================================================

def evolucionar_poblacion_clase(
    clase_objetivo,
    datos_fuzzificados,
    num_intentos=5,
    gens_por_intento=35
):
    """
    Evoluciona una población especializada en una clase de salida específica.
    Utiliza búsqueda multi-intento con penalización tabú para descubrir múltiples
    reglas diversas y complementarias con al menos 2 antecedentes.
    """

    tabu = set()
    reglas_encontradas = []

    for intento in range(num_intentos):

        poblacion = crear_poblacion_inicial(
            consecuente_fijo=clase_objetivo
        )

        evaluar_poblacion(
            poblacion,
            datos_fuzzificados
        )

        for gen in range(gens_por_intento):

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

            # Reparar si algún hijo mutó a menos de 2 antecedentes
            for h in hijos:

                while sum(1 for g in h[:-1] if g != NO_USAR) < 2:

                    inactivos = [
                        idx for idx, g in enumerate(h[:-1])
                        if g == NO_USAR
                    ]

                    if not inactivos:
                        break

                    idx = random.choice(inactivos)
                    h[idx] = random.choice(
                        CONJUNTOS[VARIABLES_ENTRADA[idx]]
                    )

            evaluar_poblacion(
                hijos,
                datos_fuzzificados
            )

            # Penalización tabú para forzar exploración de nuevas combinaciones
            if tabu:

                for h in hijos:

                    ant = tuple(h[:-1])

                    if ant in tabu:

                        h.fitness.values = (
                            h.fitness.values[0] * 0.05,
                        )

            poblacion = eliminar_peores(
                poblacion,
                hijos
            )

        # Extraer los mejores individuos únicos de este intento
        for individuo in poblacion[:5]:

            ant = tuple(individuo[:-1])
            metricas = calcular_metricas(
                individuo,
                datos_fuzzificados
            )

            if metricas["fitness"] > 0 and ant not in tabu:

                tabu.add(ant)

                reglas_encontradas.append({
                    "individuo": list(individuo),
                    "support": metricas["support"],
                    "confidence": metricas["confidence"],
                    "coverage": metricas["coverage"],
                    "lift": metricas["lift"],
                    "fitness": metricas["fitness"]
                })

    reglas_encontradas.sort(
        key=lambda r: r["fitness"],
        reverse=True
    )

    return reglas_encontradas, {}


# =========================================================
# EJECUTAR ALGORITMO GENÉTICO (MULTICLASE CON NICHOS Y TABÚ)
# =========================================================

def ejecutar_algoritmo_genetico(datos_fuzzificados):
    """
    Ejecuta el Algoritmo Genético Multiclase con Nichos y Búsqueda Tabú.
    Evoluciona independientemente para cada clase de salida (nulo, bajo, alto, extremo)
    extrayendo múltiples reglas contextuales diversas de alta confianza.
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
            num_intentos=5,
            gens_por_intento=35
        )

        historial_global[clase] = historial_clase

        print(f"Reglas únicas encontradas para '{clase}': {len(reglas_clase)}")

        for idx, regla in enumerate(reglas_clase[:5], start=1):

            print(f"  [{idx}] {convertir_regla_texto(regla['individuo'])}")
            print(f"      Confianza = {regla['confidence']:.4f} | Cobertura = {regla['coverage']:.4f} | Fitness = {regla['fitness']:.4f}")

            todas_las_reglas.append(regla)

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
