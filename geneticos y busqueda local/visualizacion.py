# visualizacion.py

import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from configuracion import (
    ANCHO,
    LARGO,
    ILUMINACION_MINIMA,
    CARPETA_RESULTADOS,
    NUM_FOCOS
)

from iluminacion import calcular_iluminacion


def visualizar_solucion(individuo):

    # ==========================================
    # CREAR CARPETA
    # ==========================================

    os.makedirs(
        CARPETA_RESULTADOS,
        exist_ok=True
    )

    # ==========================================
    # CALCULAR ILUMINACIÓN
    # ==========================================

    iluminacion = calcular_iluminacion(
        individuo
    )

    # ==========================================
    # CREAR FIGURA
    # ==========================================

    fig, ax = plt.subplots(
        figsize=(10, 8)
    )

    # ==========================================
    # MAPA DE ILUMINACIÓN
    # ==========================================

    x = np.linspace(
        0,
        ANCHO,
        iluminacion.shape[1]
    )

    y = np.linspace(
        0,
        LARGO,
        iluminacion.shape[0]
    )

    X, Y = np.meshgrid(
        x,
        y
    )

    imagen = ax.contourf(
        X,
        Y,
        iluminacion,
        levels=30
    )

    # ==========================================
    # BARRA DE COLOR
    # ==========================================

    barra = fig.colorbar(
        imagen,
        ax=ax
    )

    barra.set_label(
        "Iluminación"
    )

    # ==========================================
    # DIBUJAR LOS FOCOS
    # ==========================================

    for i in range(NUM_FOCOS):

        x_foco = individuo[
            i * 3
        ]

        y_foco = individuo[
            i * 3 + 1
        ]

        potencia = individuo[
            i * 3 + 2
        ]

        # --------------------------------------
        # FOCO APAGADO
        # --------------------------------------

        if potencia == 0:

            ax.scatter(
                x_foco,
                y_foco,
                marker="x",
                s=100,
                label=f"Foco {i + 1}: APAGADO"
            )

        # --------------------------------------
        # FOCO ENCENDIDO
        # --------------------------------------

        else:

            ax.scatter(
                x_foco,
                y_foco,
                marker="o",
                s=100,
                edgecolors="black",
                label=(
                    f"Foco {i + 1}: "
                    f"{potencia} W"
                )
            )

        # --------------------------------------
        # NÚMERO DEL FOCO
        # --------------------------------------

        ax.text(
            x_foco + 0.08,
            y_foco + 0.08,
            str(i + 1),
            fontsize=9
        )

    # ==========================================
    # CONTORNO DE ILUMINACIÓN MÍNIMA
    # ==========================================

    ax.contour(
        X,
        Y,
        iluminacion,
        levels=[
            ILUMINACION_MINIMA
        ],
        linewidths=2
    )

    # ==========================================
    # CONFIGURACIÓN DEL GRÁFICO
    # ==========================================

    ax.set_xlim(
        0,
        ANCHO
    )

    ax.set_ylim(
        0,
        LARGO
    )

    ax.set_xlabel(
        "Posición X (m)"
    )

    ax.set_ylabel(
        "Posición Y (m)"
    )

    ax.set_title(
        "Solución encontrada por el algoritmo genético"
    )

    ax.set_aspect(
        "equal"
    )

    ax.legend(
        loc="upper right",
        fontsize=8
    )

    ax.grid(
        True,
        alpha=0.3
    )

    # ==========================================
    # GUARDAR IMAGEN
    # ==========================================

    ruta = os.path.join(
        CARPETA_RESULTADOS,
        "solucion_final.png"
    )

    plt.savefig(
        ruta,
        dpi=300,
        bbox_inches="tight"
    )

    # ==========================================
    # NO MOSTRAR LA IMAGEN
    # ==========================================

    plt.close(fig)

    return ruta