
import os
import numpy as np
import matplotlib

# No abrir ventanas de Matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from iluminacion import calcular_iluminacion
from fitness import calcular_fitness
from configuracion import (
    ANCHO,
    LARGO,
    NUM_FOCOS,
    ILUMINACION_MINIMA
)


# ============================================================
# CONFIGURACIÓN DE CARPETAS
# ============================================================

CARPETA_RESULTADOS = "resultados"
CARPETA_GRAFICOS = os.path.join(CARPETA_RESULTADOS, "graficos")


def crear_carpetas():
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
    os.makedirs(CARPETA_GRAFICOS, exist_ok=True)


# ============================================================
# DATOS DE UN INDIVIDUO
# ============================================================

def obtener_datos_individuo(individuo):
    """
    Obtiene las principales métricas de un individuo.
    """

    iluminacion = calcular_iluminacion(individuo)

    cobertura = np.mean(iluminacion >= ILUMINACION_MINIMA)

    potencia_total = sum(
        individuo[i * 3 + 2]
        for i in range(NUM_FOCOS)
    )

    focos_encendidos = sum(
        1
        for i in range(NUM_FOCOS)
        if individuo[i * 3 + 2] > 0
    )

    iluminacion_promedio = np.mean(iluminacion)
    iluminacion_minima = np.min(iluminacion)
    iluminacion_maxima = np.max(iluminacion)

    fitness = calcular_fitness(individuo)

    return {
        "fitness": fitness,
        "cobertura": cobertura * 100,
        "potencia": potencia_total,
        "focos": focos_encendidos,
        "iluminacion_promedio": iluminacion_promedio,
        "iluminacion_minima": iluminacion_minima,
        "iluminacion_maxima": iluminacion_maxima
    }


# ============================================================
# 1. EVOLUCIÓN DEL FITNESS
# ============================================================

def grafico_evolucion_fitness(historial):

    generaciones = historial["generaciones"]
    fitness = historial["fitness"]

    plt.figure(figsize=(10, 6))

    plt.plot(
        generaciones,
        fitness,
        linewidth=2
    )

    plt.xlabel("Generación")
    plt.ylabel("Fitness")
    plt.title("Evolución del fitness durante el algoritmo genético")

    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CARPETA_GRAFICOS,
            "01_evolucion_fitness.png"
        ),
        dpi=300
    )

    plt.close()


# ============================================================
# 2. EVOLUCIÓN DE LA COBERTURA
# ============================================================

def grafico_evolucion_cobertura(historial):

    generaciones = historial["generaciones"]
    cobertura = historial["cobertura"]

    plt.figure(figsize=(10, 6))

    plt.plot(
        generaciones,
        cobertura,
        linewidth=2
    )

    plt.axhline(
        100,
        linestyle="--",
        linewidth=1.5,
        label="Cobertura completa"
    )

    plt.xlabel("Generación")
    plt.ylabel("Cobertura (%)")
    plt.title("Evolución de la cobertura de iluminación")

    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CARPETA_GRAFICOS,
            "02_evolucion_cobertura.png"
        ),
        dpi=300
    )

    plt.close()


# ============================================================
# 3. EVOLUCIÓN DE LA POTENCIA
# ============================================================

def grafico_evolucion_potencia(historial):

    generaciones = historial["generaciones"]
    potencia = historial["potencia"]

    plt.figure(figsize=(10, 6))

    plt.plot(
        generaciones,
        potencia,
        linewidth=2
    )

    plt.xlabel("Generación")
    plt.ylabel("Potencia total (W)")
    plt.title("Evolución de la potencia utilizada")

    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CARPETA_GRAFICOS,
            "03_evolucion_potencia.png"
        ),
        dpi=300
    )

    plt.close()


# ============================================================
# 4. EVOLUCIÓN DE LOS FOCOS ENCENDIDOS
# ============================================================

def grafico_evolucion_focos(historial):

    generaciones = historial["generaciones"]
    focos = historial["focos"]

    plt.figure(figsize=(10, 6))

    plt.plot(
        generaciones,
        focos,
        linewidth=2
    )

    plt.xlabel("Generación")
    plt.ylabel("Focos encendidos")
    plt.title("Evolución del número de focos encendidos")

    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CARPETA_GRAFICOS,
            "04_evolucion_focos.png"
        ),
        dpi=300
    )

    plt.close()


# ============================================================
# 5. EVOLUCIÓN DE LA ILUMINACIÓN
# ============================================================

def grafico_evolucion_iluminacion(historial):

    generaciones = historial["generaciones"]

    promedio = historial["iluminacion_promedio"]
    minima = historial["iluminacion_minima"]
    maxima = historial["iluminacion_maxima"]

    plt.figure(figsize=(10, 6))

    plt.plot(
        generaciones,
        promedio,
        linewidth=2,
        label="Promedio"
    )

    plt.plot(
        generaciones,
        minima,
        linewidth=2,
        label="Mínima"
    )

    plt.plot(
        generaciones,
        maxima,
        linewidth=2,
        label="Máxima"
    )

    plt.axhline(
        ILUMINACION_MINIMA,
        linestyle="--",
        linewidth=1.5,
        label=f"Umbral mínimo ({ILUMINACION_MINIMA} lux)"
    )

    plt.xlabel("Generación")
    plt.ylabel("Iluminación (lux)")
    plt.title("Evolución de los niveles de iluminación")

    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CARPETA_GRAFICOS,
            "05_evolucion_iluminacion.png"
        ),
        dpi=300
    )

    plt.close()


# ============================================================
# 6. DISTRIBUCIÓN DEL FITNESS
# ============================================================

def grafico_distribucion_fitness(poblacion_final):

    fitnesses = [
        calcular_fitness(individuo)
        for individuo in poblacion_final
    ]

    plt.figure(figsize=(10, 6))

    plt.hist(
        fitnesses,
        bins=15,
        edgecolor="black"
    )

    plt.xlabel("Fitness")
    plt.ylabel("Frecuencia")
    plt.title("Distribución del fitness de la población final")

    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CARPETA_GRAFICOS,
            "06_distribucion_fitness.png"
        ),
        dpi=300
    )

    plt.close()


# ============================================================
# 7. DISTRIBUCIÓN DE LA POTENCIA
# ============================================================

def grafico_distribucion_potencia(poblacion_final):

    potencias = []

    for individuo in poblacion_final:

        potencia = sum(
            individuo[i * 3 + 2]
            for i in range(NUM_FOCOS)
        )

        potencias.append(potencia)

    plt.figure(figsize=(10, 6))

    plt.hist(
        potencias,
        bins=15,
        edgecolor="black"
    )

    plt.xlabel("Potencia total (W)")
    plt.ylabel("Frecuencia")
    plt.title("Distribución de la potencia en la población final")

    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CARPETA_GRAFICOS,
            "07_distribucion_potencia.png"
        ),
        dpi=300
    )

    plt.close()


# ============================================================
# 8. FITNESS VS POTENCIA
# ============================================================

def grafico_fitness_vs_potencia(poblacion_final):

    fitnesses = []
    potencias = []

    for individuo in poblacion_final:

        fitnesses.append(
            calcular_fitness(individuo)
        )

        potencia = sum(
            individuo[i * 3 + 2]
            for i in range(NUM_FOCOS)
        )

        potencias.append(potencia)

    plt.figure(figsize=(10, 6))

    plt.scatter(
        potencias,
        fitnesses,
        alpha=0.7
    )

    plt.xlabel("Potencia total (W)")
    plt.ylabel("Fitness")
    plt.title("Relación entre potencia y fitness")

    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CARPETA_GRAFICOS,
            "08_fitness_vs_potencia.png"
        ),
        dpi=300
    )

    plt.close()


# ============================================================
# 9. FITNESS VS COBERTURA
# ============================================================

def grafico_fitness_vs_cobertura(poblacion_final):

    fitnesses = []
    coberturas = []

    for individuo in poblacion_final:

        datos = obtener_datos_individuo(individuo)

        fitnesses.append(datos["fitness"])
        coberturas.append(datos["cobertura"])

    plt.figure(figsize=(10, 6))

    plt.scatter(
        coberturas,
        fitnesses,
        alpha=0.7
    )

    plt.xlabel("Cobertura (%)")
    plt.ylabel("Fitness")
    plt.title("Relación entre cobertura y fitness")

    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CARPETA_GRAFICOS,
            "09_fitness_vs_cobertura.png"
        ),
        dpi=300
    )

    plt.close()


# ============================================================
# 10. COBERTURA VS POTENCIA
# ============================================================

def grafico_cobertura_vs_potencia(poblacion_final):

    potencias = []
    coberturas = []

    for individuo in poblacion_final:

        datos = obtener_datos_individuo(individuo)

        potencias.append(datos["potencia"])
        coberturas.append(datos["cobertura"])

    plt.figure(figsize=(10, 6))

    plt.scatter(
        potencias,
        coberturas,
        alpha=0.7
    )

    plt.xlabel("Potencia total (W)")
    plt.ylabel("Cobertura (%)")
    plt.title("Relación entre potencia y cobertura")

    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CARPETA_GRAFICOS,
            "10_cobertura_vs_potencia.png"
        ),
        dpi=300
    )

    plt.close()


# ============================================================
# GENERAR TODOS LOS GRÁFICOS
# ============================================================

def generar_graficos(historial, poblacion_final):

    crear_carpetas()

    print("\nGenerando gráficos estadísticos...")

    grafico_evolucion_fitness(historial)

    print("  [1/10] Evolución del fitness")

    grafico_evolucion_cobertura(historial)

    print("  [2/10] Evolución de la cobertura")

    grafico_evolucion_potencia(historial)

    print("  [3/10] Evolución de la potencia")

    grafico_evolucion_focos(historial)

    print("  [4/10] Evolución de los focos")

    grafico_evolucion_iluminacion(historial)

    print("  [5/10] Evolución de la iluminación")

    grafico_distribucion_fitness(poblacion_final)

    print("  [6/10] Distribución del fitness")

    grafico_distribucion_potencia(poblacion_final)

    print("  [7/10] Distribución de potencia")

    grafico_fitness_vs_potencia(poblacion_final)

    print("  [8/10] Fitness vs potencia")

    grafico_fitness_vs_cobertura(poblacion_final)

    print("  [9/10] Fitness vs cobertura")

    grafico_cobertura_vs_potencia(poblacion_final)

    print("  [10/10] Cobertura vs potencia")

    print("\nTodos los gráficos fueron guardados en:")

    print(
        os.path.abspath(CARPETA_GRAFICOS)
    )


# ============================================================
# VISUALIZACIÓN DE LA SOLUCIÓN FINAL
# ============================================================

def visualizar_solucion(individuo):

    crear_carpetas()

    # Importación local para evitar problemas circulares
    from iluminacion import generar_mapa_iluminacion

    mapa = generar_mapa_iluminacion(individuo)

    plt.figure(figsize=(10, 8))

    plt.imshow(
        mapa,
        origin="lower",
        extent=[0, ANCHO, 0, LARGO],
        aspect="equal"
    )

    plt.colorbar(
        label="Iluminación (lux)"
    )

    # Dibujar los focos
    for i in range(NUM_FOCOS):

        x = individuo[i * 3]
        y = individuo[i * 3 + 1]
        potencia = individuo[i * 3 + 2]

        if potencia > 0:

            plt.scatter(
                x,
                y,
                s=100,
                edgecolors="black",
                linewidths=1.5
            )

            plt.text(
                x,
                y,
                f" F{i + 1}\n {potencia} W",
                fontsize=9
            )

    plt.xlabel("Ancho (m)")
    plt.ylabel("Largo (m)")
    plt.title("Distribución espacial de la solución final")

    plt.tight_layout()

    ruta = os.path.join(
        CARPETA_RESULTADOS,
        "solucion_final.png"
    )

    plt.savefig(
        ruta,
        dpi=300
    )

    plt.close()

    print(
        f"Imagen de la solución final guardada en: {ruta}"
    )
