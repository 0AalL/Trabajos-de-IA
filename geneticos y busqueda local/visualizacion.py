# main.py

from poblacion import crear_poblacion

from fitness import calcular_fitness

from seleccion import seleccionar_padres

from crossover import crossover

from mutacion import mutar

from visualizacion import (
    generar_graficos,
    visualizar_solucion,
    obtener_datos_individuo
)

from iluminacion import (
    cuadricula_a_coordenadas
)

from configuracion import (
    TAM_POBLACION,
    NUM_GENERACIONES,
    NUM_FOCOS
)


# ============================================================
# EJECUCIÓN DEL ALGORITMO GENÉTICO
# ============================================================

def ejecutar():

    print("=" * 60)

    print(
        "ALGORITMO GENÉTICO - "
        "OPTIMIZACIÓN DE ILUMINACIÓN"
    )

    print("=" * 60)

    # ========================================================
    # POBLACIÓN INICIAL
    # ========================================================

    poblacion = crear_poblacion()

    mejor_global = None

    mejor_fitness_global = -1

    # ========================================================
    # HISTORIAL
    # ========================================================

    historial = {

        "generaciones": [],

        "fitness": [],

        "cobertura": [],

        "potencia": [],

        "focos": [],

        "iluminacion_promedio": [],

        "iluminacion_minima": [],

        "iluminacion_maxima": []
    }

    # ========================================================
    # ARCHIVO DE RESULTADOS
    # ========================================================

    archivo = open(
        "resultados_ag.txt",
        "w",
        encoding="utf-8"
    )

    archivo.write(
        "RESULTADOS DEL ALGORITMO GENÉTICO\n"
    )

    archivo.write(
        "=" * 60 +
        "\n\n"
    )

    # ========================================================
    # CICLO PRINCIPAL
    # ========================================================

    for generacion in range(
        1,
        NUM_GENERACIONES + 1
    ):

        # ====================================================
        # EVALUAR POBLACIÓN
        # ====================================================

        fitnesses = [
            calcular_fitness(
                individuo
            )
            for individuo in poblacion
        ]

        # ====================================================
        # SELECCIÓN
        # ====================================================

        padre1, padre2 = (
            seleccionar_padres(
                poblacion,
                fitnesses
            )
        )

        # ====================================================
        # CROSSOVER
        # ====================================================

        hijo1, hijo2 = crossover(
            padre1,
            padre2
        )

        # ====================================================
        # MUTACIÓN
        # ====================================================

        hijo1 = mutar(
            hijo1
        )

        hijo2 = mutar(
            hijo2
        )

        # ====================================================
        # AGREGAR HIJOS
        # ====================================================

        poblacion.append(
            hijo1
        )

        poblacion.append(
            hijo2
        )

        # ====================================================
        # ELIMINACIÓN
        # ====================================================

        while len(poblacion) > TAM_POBLACION:

            fitnesses = [
                calcular_fitness(
                    individuo
                )
                for individuo in poblacion
            ]

            maximo = max(
                fitnesses
            )

            pesos_eliminacion = [

                maximo -
                fitness +
                0.000001

                for fitness in fitnesses
            ]

            total = sum(
                pesos_eliminacion
            )

            probabilidades = [

                peso / total

                for peso in
                pesos_eliminacion
            ]

            # ================================================
            # RULETA INVERSA
            # ================================================

            ruleta = []

            for i, probabilidad in enumerate(
                probabilidades
            ):

                cantidad = round(
                    probabilidad * 100
                )

                for _ in range(
                    cantidad
                ):

                    ruleta.append(
                        i
                    )

            # ================================================
            # GARANTIZAR 100 POSICIONES
            # ================================================

            if len(ruleta) == 0:

                ruleta = list(
                    range(
                        len(poblacion)
                    )
                )

            while len(ruleta) < 100:

                ruleta.append(
                    ruleta[-1]
                )

            while len(ruleta) > 100:

                ruleta.pop()

            import random

            numero = random.randint(
                1,
                100
            )

            indice_eliminar = (
                ruleta[numero - 1]
            )

            poblacion.pop(
                indice_eliminar
            )

        # ====================================================
        # MEJOR INDIVIDUO
        # ====================================================

        fitnesses = [
            calcular_fitness(
                individuo
            )
            for individuo in poblacion
        ]

        mejor_fitness = max(
            fitnesses
        )

        indice_mejor = (
            fitnesses.index(
                mejor_fitness
            )
        )

        mejor_actual = (
            poblacion[
                indice_mejor
            ]
        )

        # ====================================================
        # ACTUALIZAR MEJOR GLOBAL
        # ====================================================

        if (
            mejor_fitness >
            mejor_fitness_global
        ):

            mejor_fitness_global = (
                mejor_fitness
            )

            mejor_global = (
                mejor_actual.copy()
            )

        # ====================================================
        # MÉTRICAS
        # ====================================================

        datos = (
            obtener_datos_individuo(
                mejor_actual
            )
        )

        # ====================================================
        # HISTORIAL
        # ====================================================

        historial[
            "generaciones"
        ].append(
            generacion
        )

        historial[
            "fitness"
        ].append(
            datos["fitness"]
        )

        historial[
            "cobertura"
        ].append(
            datos["cobertura"]
        )

        historial[
            "potencia"
        ].append(
            datos["potencia"]
        )

        historial[
            "focos"
        ].append(
            datos["focos"]
        )

        historial[
            "iluminacion_promedio"
        ].append(
            datos[
                "iluminacion_promedio"
            ]
        )

        historial[
            "iluminacion_minima"
        ].append(
            datos[
                "iluminacion_minima"
            ]
        )

        historial[
            "iluminacion_maxima"
        ].append(
            datos[
                "iluminacion_maxima"
            ]
        )

        # ====================================================
        # TXT
        # ====================================================

        archivo.write(

            f"Generación "
            f"{generacion:03d} | "

            f"Fitness: "
            f"{datos['fitness']:.6f} | "

            f"Cobertura: "
            f"{datos['cobertura']:.2f}% | "

            f"Potencia: "
            f"{datos['potencia']} W | "

            f"Focos: "
            f"{datos['focos']} | "

            f"Iluminación promedio: "
            f"{datos['iluminacion_promedio']:.2f} lux | "

            f"Mínima: "
            f"{datos['iluminacion_minima']:.2f} lux | "

            f"Máxima: "
            f"{datos['iluminacion_maxima']:.2f} lux\n"
        )

        # ====================================================
        # PROGRESO
        # ====================================================

        print(

            f"Generación "
            f"{generacion:03d} | "

            f"Fitness = "
            f"{datos['fitness']:.6f} | "

            f"Cobertura = "
            f"{datos['cobertura']:.2f}% | "

            f"Potencia = "
            f"{datos['potencia']} W"
        )

    # ========================================================
    # RESULTADO FINAL
    # ========================================================

    datos_finales = (
        obtener_datos_individuo(
            mejor_global
        )
    )

    archivo.write(
        "\n"
    )

    archivo.write(
        "=" * 60 +
        "\n"
    )

    archivo.write(
        "MEJOR SOLUCIÓN ENCONTRADA\n"
    )

    archivo.write(
        "=" * 60 +
        "\n\n"
    )

    archivo.write(
        f"Fitness: "
        f"{datos_finales['fitness']:.6f}\n"
    )

    archivo.write(
        f"Cobertura: "
        f"{datos_finales['cobertura']:.2f}%\n"
    )

    archivo.write(
        f"Potencia total: "
        f"{datos_finales['potencia']} W\n"
    )

    archivo.write(
        f"Focos encendidos: "
        f"{datos_finales['focos']}\n"
    )

    archivo.write(
        f"Iluminación promedio: "
        f"{datos_finales['iluminacion_promedio']:.2f} lux\n"
    )

    archivo.write(
        f"Iluminación mínima: "
        f"{datos_finales['iluminacion_minima']:.2f} lux\n"
    )

    archivo.write(
        f"Iluminación máxima: "
        f"{datos_finales['iluminacion_maxima']:.2f} lux\n\n"
    )

    # ========================================================
    # INFORMACIÓN DE LOS FOCOS
    # ========================================================

    archivo.write(
        "FOCOS:\n"
    )

    for i in range(
        NUM_FOCOS
    ):

        cuadricula = (
            mejor_global[
                i * 2
            ]
        )

        potencia = (
            mejor_global[
                i * 2 + 1
            ]
        )

        x, y = (
            cuadricula_a_coordenadas(
                cuadricula
            )
        )

        estado = (
            "ENCENDIDO"
            if potencia > 0
            else "APAGADO"
        )

        archivo.write(

            f"Foco {i + 1}: "

            f"Cuadrícula={cuadricula}, "

            f"Centro=("
            f"{x:.2f}, "
            f"{y:.2f}"
            f"), "

            f"Potencia={potencia} W, "

            f"Estado={estado}\n"
        )

    archivo.close()

    # ========================================================
    # GRÁFICOS
    # ========================================================

    print("\n")

    print("=" * 60)

    print(
        "ANÁLISIS ESTADÍSTICO"
    )

    print("=" * 60)

    generar_graficos(
        historial,
        poblacion
    )

    # ========================================================
    # SOLUCIÓN FINAL
    # ========================================================

    visualizar_solucion(
        mejor_global
    )

    # ========================================================
    # MOSTRAR RESULTADO
    # ========================================================

    print("\n")

    print("=" * 60)

    print(
        "MEJOR SOLUCIÓN ENCONTRADA"
    )

    print("=" * 60)

    print(
        f"Fitness: "
        f"{datos_finales['fitness']:.6f}"
    )

    print(
        f"Cobertura: "
        f"{datos_finales['cobertura']:.2f}%"
    )

    print(
        f"Potencia total: "
        f"{datos_finales['potencia']} W"
    )

    print(
        f"Focos encendidos: "
        f"{datos_finales['focos']}"
    )

    print(
        f"Iluminación promedio: "
        f"{datos_finales['iluminacion_promedio']:.2f} lux"
    )

    print(
        f"Iluminación mínima: "
        f"{datos_finales['iluminacion_minima']:.2f} lux"
    )

    print(
        f"Iluminación máxima: "
        f"{datos_finales['iluminacion_maxima']:.2f} lux"
    )

    print(
        "\nUbicación de los focos:"
    )

    for i in range(
        NUM_FOCOS
    ):

        cuadricula = (
            mejor_global[
                i * 2
            ]
        )

        potencia = (
            mejor_global[
                i * 2 + 1
            ]
        )

        x, y = (
            cuadricula_a_coordenadas(
                cuadricula
            )
        )

        estado = (
            "ENCENDIDO"
            if potencia > 0
            else "APAGADO"
        )

        print(

            f"Foco {i + 1}: "

            f"Cuadrícula {cuadricula} "

            f"→ "

            f"({x:.2f}, {y:.2f}) "

            f"- "

            f"{potencia} W "

            f"- "

            f"{estado}"
        )

    print(
        "\nProceso terminado correctamente."
    )


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    ejecutar()