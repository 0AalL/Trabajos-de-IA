# visualizacion.py

import os
import numpy as np
import matplotlib.pyplot as plt

from configuracion import (
    NUM_FOCOS,
    ILUMINACION_MINIMA,
    CARPETA_RESULTADOS
)

from fitness import calcular_fitness
from iluminacion import (
    calcular_iluminacion,
    cuadricula_a_coordenadas
)


def obtener_datos_individuo(individuo):
    iluminacion = calcular_iluminacion(individuo)

    fitness = calcular_fitness(individuo)
    cobertura = float(np.mean(iluminacion >= ILUMINACION_MINIMA) * 100.0)

    potencia_total = 0
    focos_encendidos = 0

    for i in range(NUM_FOCOS):
        p = individuo[i * 2 + 1]
        potencia_total += p
        if p > 0:
            focos_encendidos += 1

    return {
        "fitness": fitness,
        "cobertura": cobertura,
        "potencia": potencia_total,
        "focos": focos_encendidos,
        "iluminacion_promedio": float(np.mean(iluminacion)),
        "iluminacion_minima": float(np.min(iluminacion)),
        "iluminacion_maxima": float(np.max(iluminacion)),
    }


def generar_graficos(historial, poblacion):
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

    generaciones = historial["generaciones"]

    # 1) Fitness
    plt.figure(figsize=(8, 4))
    plt.plot(generaciones, historial["fitness"], label="Fitness")
    plt.xlabel("Generación")
    plt.ylabel("Fitness")
    plt.title("Evolución del fitness")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_RESULTADOS, "fitness.png"), dpi=120)
    plt.close()

    # 2) Cobertura y potencia
    fig, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(generaciones, historial["cobertura"], color="tab:blue", label="Cobertura (%)")
    ax1.set_xlabel("Generación")
    ax1.set_ylabel("Cobertura (%)", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    ax2 = ax1.twinx()
    ax2.plot(generaciones, historial["potencia"], color="tab:red", label="Potencia (W)")
    ax2.set_ylabel("Potencia (W)", color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")

    plt.title("Cobertura vs Potencia")
    fig.tight_layout()
    plt.savefig(os.path.join(CARPETA_RESULTADOS, "cobertura_potencia.png"), dpi=120)
    plt.close(fig)

    # 3) Estadísticas de iluminación
    plt.figure(figsize=(8, 4))
    plt.plot(generaciones, historial["iluminacion_promedio"], label="Promedio")
    plt.plot(generaciones, historial["iluminacion_minima"], label="Mínima")
    plt.plot(generaciones, historial["iluminacion_maxima"], label="Máxima")
    plt.xlabel("Generación")
    plt.ylabel("Lux")
    plt.title("Evolución de iluminación")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_RESULTADOS, "iluminacion.png"), dpi=120)
    plt.close()


def visualizar_solucion(individuo):
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

    iluminacion = calcular_iluminacion(individuo)

    plt.figure(figsize=(7, 6))
    plt.imshow(iluminacion, origin="lower", aspect="auto", cmap="viridis")
    cbar = plt.colorbar()
    cbar.set_label("Lux")

    # Contorno del umbral mínimo
    plt.contour(
        iluminacion,
        levels=[ILUMINACION_MINIMA],
        colors="white",
        linewidths=1.2
    )

    # Dibujar focos
    for i in range(NUM_FOCOS):
        cuadricula = individuo[i * 2]
        potencia = individuo[i * 2 + 1]
        x, y = cuadricula_a_coordenadas(cuadricula)

        # convertir coordenadas de sala (0..7,0..8) a índices de la imagen
        px = (x / 7.0) * (iluminacion.shape[1] - 1)
        py = (y / 8.0) * (iluminacion.shape[0] - 1)

        if potencia > 0:
            plt.scatter(px, py, c="red", s=40)
            plt.text(px + 1, py + 1, f"{potencia}W", color="white", fontsize=8)
        else:
            plt.scatter(px, py, c="gray", s=20)

    plt.title("Mapa de iluminación - mejor solución")
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_RESULTADOS, "mejor_solucion.png"), dpi=140)
    plt.show()