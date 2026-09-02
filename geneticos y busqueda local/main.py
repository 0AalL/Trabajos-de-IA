
# main.py

import random

from poblacion import crear_poblacion
from fitness import calcular_fitness
from seleccion import seleccionar_padres
from crossover import crossover
from mutacion import mutar
from visualizacion import visualizar_solucion

from configuracion import (
    TAM_POBLACION,
    NUM_GENERACIONES,
    NUM_FOCOS
)


def ejecutar():

    # =====================================
    # 1. CREAR POBLACIÓN INICIAL
    # =====================================

    poblacion = crear_poblacion()

    mejor_global = None
    mejor_fitness = -1

    # =====================================
    # ARCHIVO DE RESULTADOS
    # =====================================

    archivo = open(
        "resultados_ag.txt",
        "w",
        encoding="utf-8"
    )

    archivo.write("=" * 70 + "\n")
    archivo.write(
        "RESULTADOS DEL ALGORITMO GENÉTICO\n"
    )
    archivo.write("=" * 70 + "\n\n")

    archivo.write(
        f"Tamaño de población: {TAM_POBLACION}\n"
    )

    archivo.write(
        f"Número de generaciones: {NUM_GENERACIONES}\n"
    )

    archivo.write(
        f"Número de focos: {NUM_FOCOS}\n"
    )

    archivo.write(
        "Espacio de búsqueda: continuo\n"
    )

    archivo.write(
        "Potencia 0 W = foco apagado\n"
    )

    archivo.write("\n")

    archivo.write("=" * 70 + "\n")
    archivo.write(
        "EVOLUCIÓN DE LAS GENERACIONES\n"
    )
    archivo.write("=" * 70 + "\n\n")

    # =====================================
    # GENERACIONES
    # =====================================

    for generacion in range(
        NUM_GENERACIONES
    ):

        # =================================
        # 2. CALCULAR FITNESS
        # =================================

        fitnesses = [
            calcular_fitness(individuo)
            for individuo in poblacion
        ]

        # =================================
        # 3. GUARDAR MEJOR SOLUCIÓN
        # =================================

        mejor_actual = max(
            fitnesses
        )

        indice_mejor = fitnesses.index(
            mejor_actual
        )

        if mejor_actual > mejor_fitness:

            mejor_fitness = (
                mejor_actual
            )

            mejor_global = (
                poblacion[indice_mejor].copy()
            )

        # =================================
        # 4. SELECCIONAR DOS PADRES
        # =================================

        padre1, padre2 = seleccionar_padres(
            poblacion,
            fitnesses
        )

        # =================================
        # 5. CROSSOVER
        # =================================

        hijo1, hijo2 = crossover(
            padre1,
            padre2
        )

        # =================================
        # 6. MUTACIÓN
        # =================================

        hijo1 = mutar(
            hijo1
        )

        hijo2 = mutar(
            hijo2
        )

        # =================================
        # 7. AGREGAR HIJOS
        # =================================

        poblacion.append(
            hijo1
        )

        poblacion.append(
            hijo2
        )

        # =================================
        # 8. CALCULAR FITNESS NUEVAMENTE
        # =================================

        fitnesses = [
            calcular_fitness(individuo)
            for individuo in poblacion
        ]

        # =================================
        # 9. ELIMINAR INDIVIDUOS
        # =================================
        #
        # Mientras la población supere
        # el tamaño establecido, se elimina
        # un individuo.
        #
        # Los individuos con menor fitness
        # tienen mayor probabilidad de ser
        # eliminados.
        # =================================

        while len(poblacion) > TAM_POBLACION:

            # ---------------------------------
            # CALCULAR FITNESS
            # ---------------------------------

            fitnesses = [
                calcular_fitness(individuo)
                for individuo in poblacion
            ]

            # ---------------------------------
            # FITNESS MÁXIMO
            # ---------------------------------

            maximo = max(
                fitnesses
            )

            # ---------------------------------
            # PESOS DE ELIMINACIÓN
            # ---------------------------------
            #
            # Cuanto menor sea el fitness,
            # mayor será el peso.
            # ---------------------------------

            pesos_eliminacion = [

                maximo - fitness + 0.000001

                for fitness in fitnesses
            ]

            # ---------------------------------
            # SUMA DE PESOS
            # ---------------------------------

            total = sum(
                pesos_eliminacion
            )

            # ---------------------------------
            # PROBABILIDADES
            # ---------------------------------

            probabilidades = [

                peso / total

                for peso in pesos_eliminacion
            ]

            # ---------------------------------
            # CREAR RULETA DE 100 POSICIONES
            # ---------------------------------

            ruleta = []

            for i, probabilidad in enumerate(
                probabilidades
            ):

                cantidad = round(
                    probabilidad * 100
                )

                for _ in range(cantidad):

                    ruleta.append(
                        i
                    )

            # ---------------------------------
            # AJUSTAR A EXACTAMENTE 100
            # ---------------------------------

            while len(ruleta) < 100:

                ruleta.append(
                    ruleta[-1]
                )

            while len(ruleta) > 100:

                ruleta.pop()

            # ---------------------------------
            # EXPERIMENTO ALEATORIO
            # ---------------------------------

            numero = random.randint(
                1,
                100
            )

            indice_eliminar = (
                ruleta[numero - 1]
            )

            # ---------------------------------
            # ELIMINAR INDIVIDUO
            # ---------------------------------

            poblacion.pop(
                indice_eliminar
            )

        # =================================
        # 10. GUARDAR RESULTADO
        # =================================

        linea = (
            f"Generación "
            f"{generacion + 1:3d} | "
            f"Fitness actual: "
            f"{mejor_actual:.6f} | "
            f"Mejor global: "
            f"{mejor_fitness:.6f}\n"
        )

        print(
            linea.strip()
        )

        archivo.write(
            linea
        )

    # =====================================
    # RESULTADO FINAL
    # =====================================

    archivo.write("\n")

    archivo.write("=" * 70 + "\n")
    archivo.write(
        "MEJOR SOLUCIÓN ENCONTRADA\n"
    )
    archivo.write("=" * 70 + "\n\n")

    print(
        "\n" + "=" * 60
    )

    print(
        "MEJOR SOLUCIÓN"
    )

    print(
        "=" * 60
    )

    # =====================================
    # MOSTRAR Y GUARDAR LOS FOCOS
    # =====================================

    for i in range(NUM_FOCOS):

        x = mejor_global[
            i * 3
        ]

        y = mejor_global[
            i * 3 + 1
        ]

        potencia = mejor_global[
            i * 3 + 2
        ]

        # ---------------------------------
        # DETERMINAR ESTADO
        # ---------------------------------

        if potencia == 0:

            estado = "APAGADO"

        else:

            estado = "ENCENDIDO"

        # ---------------------------------
        # TEXTO DEL FOCO
        # ---------------------------------

        texto = (
            f"Foco {i + 1}: "
            f"x={x:.4f} m | "
            f"y={y:.4f} m | "
            f"potencia={potencia} W | "
            f"{estado}\n"
        )

        print(
            texto.strip()
        )

        archivo.write(
            texto
        )

    # =====================================
    # FITNESS FINAL
    # =====================================

    archivo.write(
        f"\nFitness final = "
        f"{mejor_fitness:.6f}\n"
    )

    print(
        f"\nFitness = "
        f"{mejor_fitness:.6f}"
    )

    # =====================================
    # GENERAR VISUALIZACIÓN
    # =====================================

    print(
        "\nGenerando visualización..."
    )

    ruta_imagen = visualizar_solucion(
        mejor_global
    )

    archivo.write(
        f"\nVisualización guardada en: "
        f"{ruta_imagen}\n"
    )

    print(
        "\nLa visualización fue guardada en:"
    )

    print(
        ruta_imagen
    )

    # =====================================
    # FINALIZAR ARCHIVO
    # =====================================

    archivo.write("\n")

    archivo.write("=" * 70 + "\n")
    archivo.write(
        "FIN DEL EXPERIMENTO\n"
    )
    archivo.write("=" * 70 + "\n")

    archivo.close()

    print(
        "\nLos resultados fueron guardados en:"
    )

    print(
        "resultados_ag.txt"
    )


# ==========================================
# EJECUTAR PROGRAMA
# ==========================================

if __name__ == "__main__":

    ejecutar()
