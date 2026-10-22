# main.py

import os
import random

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
from iluminacion import cuadricula_a_coordenadas
from configuracion import (
    TAM_POBLACION,
    NUM_GENERACIONES,
    NUM_FOCOS,
    CARPETA_RESULTADOS
)


# ============================================================
# EJECUCIÓN DEL ALGORITMO GENÉTICO
# ============================================================

def ejecutar():

    print("=" * 60)
    print("ALGORITMO GENÉTICO - OPTIMIZACIÓN DE ILUMINACIÓN")
    print("=" * 60)

    # ========================================================
    # PREPARAR CARPETA DE RESULTADOS
    # ========================================================

    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
    ruta_resultados = os.path.join(CARPETA_RESULTADOS, "resultados_ag.txt")

    # ========================================================
    # POBLACIÓN INICIAL
    # ========================================================

    poblacion = crear_poblacion()
    fitnesses = [calcular_fitness(ind) for ind in poblacion]

    mejor_global = None
    mejor_fitness_global = float("-inf")

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

    with open(ruta_resultados, "w", encoding="utf-8") as archivo:

        archivo.write("RESULTADOS DEL ALGORITMO GENÉTICO\n")
        archivo.write("=" * 60 + "\n\n")

        # ====================================================
        # CICLO PRINCIPAL
        # ====================================================

        for generacion in range(1, NUM_GENERACIONES + 1):

            # ================================================
            # SELECCIÓN
            # ================================================

            padre1, padre2 = seleccionar_padres(poblacion, fitnesses)

            # ================================================
            # CROSSOVER + MUTACIÓN
            # ================================================

            hijo1, hijo2 = crossover(padre1, padre2)
            hijo1 = mutar(hijo1)
            hijo2 = mutar(hijo2)

            # ================================================
            # AGREGAR HIJOS + FITNESS
            # ================================================

            poblacion.append(hijo1)
            fitnesses.append(calcular_fitness(hijo1))

            poblacion.append(hijo2)
            fitnesses.append(calcular_fitness(hijo2))

            # ================================================
            # ELIMINACIÓN (RULETA INVERSA, EFICIENTE)
            # ================================================

            while len(poblacion) > TAM_POBLACION:
                maximo = max(fitnesses)

                pesos_eliminacion = [
                    (maximo - f + 1e-6) for f in fitnesses
                ]

                total = sum(pesos_eliminacion)

                if total <= 0:
                    indice_eliminar = random.randrange(len(poblacion))
                else:
                    r = random.random()
                    acumulado = 0.0
                    indice_eliminar = len(poblacion) - 1

                    for i, peso in enumerate(pesos_eliminacion):
                        acumulado += (peso / total)
                        if r <= acumulado:
                            indice_eliminar = i
                            break

                poblacion.pop(indice_eliminar)
                fitnesses.pop(indice_eliminar)

            # ================================================
            # MEJOR INDIVIDUO DE LA GENERACIÓN
            # ================================================

            indice_mejor = max(
                range(len(fitnesses)),
                key=lambda i: fitnesses[i]
            )
            mejor_fitness = fitnesses[indice_mejor]
            mejor_actual = poblacion[indice_mejor]

            # ================================================
            # ACTUALIZAR MEJOR GLOBAL
            # ================================================

            if mejor_fitness > mejor_fitness_global:
                mejor_fitness_global = mejor_fitness
                mejor_global = mejor_actual.copy()

            # ================================================
            # MÉTRICAS
            # ================================================

            datos = obtener_datos_individuo(mejor_actual)

            # ================================================
            # HISTORIAL
            # ================================================

            historial["generaciones"].append(generacion)
            historial["fitness"].append(datos["fitness"])
            historial["cobertura"].append(datos["cobertura"])
            historial["potencia"].append(datos["potencia"])
            historial["focos"].append(datos["focos"])
            historial["iluminacion_promedio"].append(datos["iluminacion_promedio"])
            historial["iluminacion_minima"].append(datos["iluminacion_minima"])
            historial["iluminacion_maxima"].append(datos["iluminacion_maxima"])

            # ================================================
            # TXT
            # ================================================

            archivo.write(
                f"Generación {generacion:03d} | "
                f"Fitness: {datos['fitness']:.6f} | "
                f"Cobertura: {datos['cobertura']:.2f}% | "
                f"Potencia: {datos['potencia']} W | "
                f"Focos: {datos['focos']} | "
                f"Iluminación promedio: {datos['iluminacion_promedio']:.2f} lux | "
                f"Mínima: {datos['iluminacion_minima']:.2f} lux | "
                f"Máxima: {datos['iluminacion_maxima']:.2f} lux\n"
            )

            # ================================================
            # PROGRESO
            # ================================================

            print(
                f"Generación {generacion:03d} | "
                f"Fitness = {datos['fitness']:.6f} | "
                f"Cobertura = {datos['cobertura']:.2f}% | "
                f"Potencia = {datos['potencia']} W"
            )

        # ====================================================
        # RESULTADO FINAL
        # ====================================================

        datos_finales = obtener_datos_individuo(mejor_global)

        archivo.write("\n")
        archivo.write("=" * 60 + "\n")
        archivo.write("MEJOR SOLUCIÓN ENCONTRADA\n")
        archivo.write("=" * 60 + "\n\n")
        archivo.write(f"Fitness: {datos_finales['fitness']:.6f}\n")
        archivo.write(f"Cobertura: {datos_finales['cobertura']:.2f}%\n")
        archivo.write(f"Potencia total: {datos_finales['potencia']} W\n")
        archivo.write(f"Focos encendidos: {datos_finales['focos']}\n")
        archivo.write(f"Iluminación promedio: {datos_finales['iluminacion_promedio']:.2f} lux\n")
        archivo.write(f"Iluminación mínima: {datos_finales['iluminacion_minima']:.2f} lux\n")
        archivo.write(f"Iluminación máxima: {datos_finales['iluminacion_maxima']:.2f} lux\n\n")

        archivo.write("FOCOS:\n")
        for i in range(NUM_FOCOS):
            cuadricula = mejor_global[i * 2]
            potencia = mejor_global[i * 2 + 1]
            x, y = cuadricula_a_coordenadas(cuadricula)
            estado = "ENCENDIDO" if potencia > 0 else "APAGADO"

            archivo.write(
                f"Foco {i + 1}: "
                f"Cuadrícula={cuadricula}, "
                f"Centro=({x:.2f}, {y:.2f}), "
                f"Potencia={potencia} W, "
                f"Estado={estado}\n"
            )

    # ========================================================
    # GRÁFICOS + VISUALIZACIÓN
    # ========================================================

    print("\n" + "=" * 60)
    print("ANÁLISIS ESTADÍSTICO")
    print("=" * 60)

    generar_graficos(historial, poblacion)
    visualizar_solucion(mejor_global)

    # ========================================================
    # MOSTRAR RESULTADO
    # ========================================================

    datos_finales = obtener_datos_individuo(mejor_global)

    print("\n" + "=" * 60)
    print("MEJOR SOLUCIÓN ENCONTRADA")
    print("=" * 60)
    print(f"Fitness: {datos_finales['fitness']:.6f}")
    print(f"Cobertura: {datos_finales['cobertura']:.2f}%")
    print(f"Potencia total: {datos_finales['potencia']} W")
    print(f"Focos encendidos: {datos_finales['focos']}")
    print(f"Iluminación promedio: {datos_finales['iluminacion_promedio']:.2f} lux")
    print(f"Iluminación mínima: {datos_finales['iluminacion_minima']:.2f} lux")
    print(f"Iluminación máxima: {datos_finales['iluminacion_maxima']:.2f} lux")

    print("\nUbicación de los focos:")
    for i in range(NUM_FOCOS):
        cuadricula = mejor_global[i * 2]
        potencia = mejor_global[i * 2 + 1]
        x, y = cuadricula_a_coordenadas(cuadricula)
        estado = "ENCENDIDO" if potencia > 0 else "APAGADO"

        print(
            f"Foco {i + 1}: "
            f"Cuadrícula {cuadricula} → "
            f"({x:.2f}, {y:.2f}) - "
            f"{potencia} W - {estado}"
        )

    print("\nProceso terminado correctamente.")
    print(f"Resultados guardados en: {ruta_resultados}")


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":
    ejecutar()