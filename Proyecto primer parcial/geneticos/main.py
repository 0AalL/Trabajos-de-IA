import os
import pandas as pd

from configuracion import (
    CARPETA_RESULTADOS,
    ARCHIVO_REGLAS_FINALES
)

from datos import (
    cargar_datos
)

from algoritmo_genetico import (
    ejecutar_algoritmo_genetico,
    convertir_regla_texto
)

from cobertura import (
    seleccionar_reglas_por_cobertura,
    encontrar_combinaciones_faltantes
)


# ============================================================
# GUARDAR REGLAS FINALES
# ============================================================

def guardar_reglas_finales(
    reglas
):

    filas = []

    for numero, regla in enumerate(
        reglas,
        start=1
    ):

        filas.append({

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
        })

    df = pd.DataFrame(
        filas
    )

    df.to_csv(
        ARCHIVO_REGLAS_FINALES,
        index=False
    )


# ============================================================
# MAIN
# ============================================================

def main():

    os.makedirs(
        CARPETA_RESULTADOS,
        exist_ok=True
    )

    print()
    print("=" * 70)
    print(
        "ALGORITMO GENÉTICO PARA GENERACIÓN "
        "DE REGLAS FUZZY"
    )
    print("=" * 70)

    # ========================================================
    # DATOS
    # ========================================================

    df, datos_fuzzificados = cargar_datos()

    print()
    print(
        f"Registros: {len(df)}"
    )

    print(
        "Dataset fuzzificado generado."
    )

    # ========================================================
    # ALGORITMO GENÉTICO
    # ========================================================

    print()
    print("=" * 70)
    print("EVOLUCIÓN")
    print("=" * 70)

    reglas, historial = (
        ejecutar_algoritmo_genetico(
            datos_fuzzificados
        )
    )

    # ========================================================
    # COBERTURA
    # ========================================================

    print()
    print("=" * 70)
    print("COBERTURA DE COMBINACIONES")
    print("=" * 70)

    (
        reglas_finales,
        combinaciones,
        cubiertas
    ) = seleccionar_reglas_por_cobertura(
        reglas
    )

    faltantes = (
        encontrar_combinaciones_faltantes(
            combinaciones,
            cubiertas
        )
    )

    # ========================================================
    # RESULTADOS DE COBERTURA
    # ========================================================

    print()
    print(
        f"Combinaciones posibles: "
        f"{len(combinaciones)}"
    )

    print(
        f"Combinaciones cubiertas: "
        f"{len(cubiertas)}"
    )

    print(
        f"Combinaciones faltantes: "
        f"{len(faltantes)}"
    )

    # --------------------------------------------------------
    # PORCENTAJE DE COBERTURA
    # --------------------------------------------------------

    if combinaciones:

        porcentaje = (
            len(cubiertas)
            /
            len(combinaciones)
            *
            100
        )

    else:

        porcentaje = 0.0

    print(
        f"Porcentaje de cobertura: "
        f"{porcentaje:.2f}%"
    )

    # ========================================================
    # GUARDAR REGLAS
    # ========================================================

    guardar_reglas_finales(
        reglas_finales
    )

    # ========================================================
    # RESUMEN
    # ========================================================

    print()
    print("=" * 70)
    print("RESULTADO")
    print("=" * 70)

    print(
        f"Reglas disponibles para cobertura: "
        f"{len(reglas)}"
    )

    print(
        f"Reglas finales seleccionadas: "
        f"{len(reglas_finales)}"
    )

    # ========================================================
    # ESTADO DE COBERTURA
    # ========================================================

    print()

    if not faltantes:

        print(
            "COBERTURA COMPLETA: "
            "todas las combinaciones están cubiertas."
        )

    else:

        print(
            "ADVERTENCIA: todavía existen "
            f"{len(faltantes)} "
            "combinaciones sin cubrir."
        )

    # ========================================================
    # ARCHIVOS
    # ========================================================

    print()
    print(
        "Archivo última generación:"
    )

    print(
        "resultados/reglas_ultima_generacion.csv"
    )

    print()
    print(
        "Archivo reglas finales:"
    )

    print(
        "resultados/reglas_finales.csv"
    )

    # ========================================================
    # REGLAS FINALES
    # ========================================================

    print()
    print("=" * 70)
    print("REGLAS FINALES")
    print("=" * 70)

    for i, regla in enumerate(
        reglas_finales,
        start=1
    ):

        print()
        print(
            f"Regla {i}"
        )

        print(
            convertir_regla_texto(
                regla["individuo"]
            )
        )

        print(
            f"Support    = "
            f"{regla['support']:.6f}"
        )

        print(
            f"Confidence = "
            f"{regla['confidence']:.6f}"
        )

        print(
            f"Coverage   = "
            f"{regla['coverage']:.6f}"
        )

        print(
            f"Lift       = "
            f"{regla['lift']:.6f}"
        )

        print(
            f"Fitness    = "
            f"{regla['fitness']:.6f}"
        )


if __name__ == "__main__":

    main()