from individuo import crear_individuo

from configuracion import TAM_POBLACION


# ============================================================
# CREAR POBLACIÓN INICIAL
# ============================================================

def crear_poblacion_inicial(consecuente_fijo=None):

    poblacion = []

    for _ in range(
        TAM_POBLACION
    ):

        individuo = crear_individuo(
            consecuente_fijo=consecuente_fijo
        )

        poblacion.append(
            individuo
        )

    return poblacion