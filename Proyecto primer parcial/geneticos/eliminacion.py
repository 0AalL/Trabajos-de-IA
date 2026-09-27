from configuracion import TAM_POBLACION


# ============================================================
# ELIMINACIÓN
# ============================================================

def eliminar_peores(
    poblacion,
    hijos
):

    # --------------------------------------------------------
    # Unir población anterior + nuevos hijos
    # --------------------------------------------------------

    candidatos = (
        poblacion
        + hijos
    )

    # --------------------------------------------------------
    # Ordenar por Fitness descendente
    # --------------------------------------------------------

    candidatos.sort(
        key=lambda individuo:
            individuo.fitness.values[0],
        reverse=True
    )

    # --------------------------------------------------------
    # Conservar solamente los mejores
    # --------------------------------------------------------

    nueva_poblacion = candidatos[
        :TAM_POBLACION
    ]

    return nueva_poblacion